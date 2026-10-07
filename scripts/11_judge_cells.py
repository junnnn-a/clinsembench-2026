#!/usr/bin/env python
"""
11_judge_cells.py — per-cell behaviour of LLM judges (rubric prompt): how often is each cell called CHANGED?

  TPR = P(CHANGED | C cell)      FPR = P(CHANGED | P cell)      identity false alarm = P(CHANGED | identity)
Reported per judge x cell, and per judge x edit type x cell. Report-cluster bootstrap CI for the pooled rates.
For the "errors" prompt, CHANGED := error_count >= 1.

Outputs: {out}/judge_cells.csv, judge_cells_by_type.csv, JUDGES.md
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

CELLS = ["identity", "P0", "P1", "P2", "C0", "C1", "C2"]


def md(df, f=3):
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.{f}f}")
    cols = [str(c) for c in d.columns]
    return "\n".join(["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"] +
                     ["| " + " | ".join(map(str, r)) + " |" for r in d.itertuples(index=False)])


def boot(df, col, n_boot, seed=0):
    rng = np.random.default_rng(seed)
    g = {k: v[col].to_numpy(float) for k, v in df.groupby("report_id")}
    keys = list(g)
    vals = [np.concatenate([g[keys[i]] for i in rng.integers(0, len(keys), len(keys))]).mean() for _ in range(n_boot)]
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--judges", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n_boot", type=int, default=500)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    pairs = pd.read_csv(args.pairs)
    rows, by_type = [], []
    for f in sorted(Path(args.judges).glob("*.csv")):
        j = pd.read_csv(f)
        col = f.stem
        lab = f"{col}__label"
        if lab not in j:
            continue
        d = pairs.merge(j[["uid", col, lab, f"{col}__conf"]], on="uid")
        if col.endswith("__errors"):
            d["called_changed"] = (d[f"{col}__conf"] >= 1).astype(float)
        else:
            d["called_changed"] = (d[lab] == "CHANGED").astype(float)
        d["unparsed"] = (d[lab] == "UNPARSED").astype(float)
        for cell in CELLS:
            s = d[d.cell == cell]
            if s.empty:
                continue
            lo, hi = boot(s, "called_changed", args.n_boot)
            rows.append({"judge": col, "cell": cell, "n": len(s), "rate_changed": s.called_changed.mean(), "ci_lo": lo, "ci_hi": hi,
                         "unparsed": s.unparsed.mean()})
            for et, g in s.groupby("edit_type"):
                by_type.append({"judge": col, "cell": cell, "edit_type": et, "n": len(g), "rate_changed": g.called_changed.mean()})
    R, T = pd.DataFrame(rows), pd.DataFrame(by_type)
    R.to_csv(out / "judge_cells.csv", index=False)
    T.to_csv(out / "judge_cells_by_type.csv", index=False)
    rep = ["# LLM judges — rate of CHANGED verdicts per cell\n",
           "P cells and identity should be 0 (false alarms); C cells should be 1 (detections).\n",
           md(R.pivot(index="judge", columns="cell", values="rate_changed")[[c for c in CELLS if c in R.cell.unique()]].reset_index()), ""]
    for cell in ["P0", "P1", "P2", "C0", "C2"]:
        s = T[T.cell == cell]
        if s.empty:
            continue
        rep += [f"## {cell} by edit type ({'false-alarm' if cell.startswith('P') else 'detection'} rate)\n",
                md(s.pivot(index="judge", columns="edit_type", values="rate_changed").reset_index(), 2), ""]
    (out / "JUDGES.md").write_text("\n".join(rep))
    print("\n".join(rep))


if __name__ == "__main__":
    main()
