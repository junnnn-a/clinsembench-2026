#!/usr/bin/env python
"""
18_analyze_monotonicity.py — X1c: monotonicity at fixed surface (data from 16_generate_monotonicity.py).

Cells per target (all relative to the same reference):
    M0 = 3 meaning-preserving edits, M1 = 1 changing + 2 preserving, M2 = 2 + 1, M3 = 3 changing   (same 3 edit sites)
    K1 = 1 changing edit only, K2 = 2 changing edits only                                         (uncontrolled ladder)
Penalty D = s(identity) - s(cell), orientation fixed (higher score = closer).

Per metric:
  step accuracies   P[D(M1)>D(M0)], P[D(M2)>D(M1)], P[D(M3)>D(M2)]   (ties 0.5)
  strict_monotone   share of targets with D(M0) < D(M1) < D(M2) < D(M3)
  weak_monotone     share with D(M0) <= D(M1) <= D(M2) <= D(M3) and D(M3) > D(M0)
  kendall_tau       mean within-target Kendall tau between #flips (0..3) and D
  mean z(D) per cell
  benign_over_error P[D(M0) > D(K1)]: three harmless edits penalised MORE than one real error
  uncontrolled ladder: step accuracies K1 > identity(0), K2 > K1, M3 > K2 — the usual "more errors, more edits" test
CIs: report-cluster bootstrap.  Output: results/2_full_<tag>/analysis/monotonicity.csv, MONO.md
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

NEW = Path(__file__).resolve().parent.parent
LOWER_BETTER = {"radcliq"}


def md(df, f=3):
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.{f}f}")
    cols = [str(c) for c in d.columns]
    return "\n".join(["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"] +
                     ["| " + " | ".join(map(str, r)) + " |" for r in d.itertuples(index=False)])


def step(a, b):
    d = a - b
    d = d[np.isfinite(d)]
    return float(np.mean((d > 0) + 0.5 * (d == 0))) if len(d) else np.nan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="mimicmono")
    ap.add_argument("--n_boot", type=int, default=1000)
    args = ap.parse_args()
    base = NEW / f"results/2_full_{args.tag}"
    pairs = pd.read_csv(NEW / f"data/pairs/full_{args.tag}_all.csv")
    parts = []
    for d in ["scores", "judges"]:
        for f in sorted((base / d).glob("*.csv")):
            df = pd.read_csv(f)
            cols = [c for c in df.columns if c != "uid" and pd.api.types.is_numeric_dtype(df[c])
                    and not c.endswith(("__conf", "__label")) and not c.startswith("crimson_")]
            parts.append(df[["uid"] + cols].drop_duplicates("uid").set_index("uid"))
    S = pd.concat(parts, axis=1)
    metrics = list(S.columns)
    df = pairs.merge(S, left_on="uid", right_index=True, how="left")
    for m in metrics:
        if m in LOWER_BETTER:
            df[m] = -df[m]
    idn = df[df.cell == "identity"].set_index("target_id")[metrics]
    cand = df[df.cell != "identity"].copy()
    for m in metrics:
        cand[m] = cand.target_id.map(idn[m]) - cand[m]
    rng = np.random.default_rng(0)
    rows = []
    for m in metrics:
        w = cand.pivot_table(index=["target_id", "report_id"], columns="cell", values=m).reset_index()
        sd = np.nanstd(cand[m].to_numpy(float)) or 1.0
        M = w[["M0", "M1", "M2", "M3"]].to_numpy(float)
        ok = np.isfinite(M).all(axis=1)
        strict = (np.diff(M, axis=1) > 0).all(axis=1)
        weak = (np.diff(M, axis=1) >= 0).all(axis=1) & (M[:, 3] > M[:, 0])
        taus = []
        for r in M[ok]:
            t = kendalltau([0, 1, 2, 3], r).correlation
            taus.append(0.0 if np.isnan(t) else t)
        r = {"metric": m, "n": int(ok.sum()),
             "step_M1>M0": step(w.M1.to_numpy(float), w.M0.to_numpy(float)),
             "step_M2>M1": step(w.M2.to_numpy(float), w.M1.to_numpy(float)),
             "step_M3>M2": step(w.M3.to_numpy(float), w.M2.to_numpy(float)),
             "strict_monotone": float(strict[ok].mean()), "weak_monotone": float(weak[ok].mean()),
             "kendall_tau": float(np.mean(taus)),
             "benign_over_error_M0>K1": step(w.M0.to_numpy(float), w.K1.to_numpy(float)),
             "uncontrolled_K2>K1": step(w.K2.to_numpy(float), w.K1.to_numpy(float)),
             "uncontrolled_M3>K2": step(w.M3.to_numpy(float), w.K2.to_numpy(float))}
        for c in ["M0", "M1", "M2", "M3", "K1", "K2"]:
            r[f"z_{c}"] = float(np.nanmean(w[c])) / sd
        # cluster bootstrap for tau and strict
        groups = [g.index.to_numpy() for _, g in w[ok].reset_index(drop=True).groupby("report_id")]
        Mo, ta, st = M[ok], np.array(taus), strict[ok]
        bt, bs = [], []
        for _ in range(args.n_boot):
            idx = np.concatenate([groups[i] for i in rng.integers(0, len(groups), len(groups))])
            bt.append(ta[idx].mean()); bs.append(st[idx].mean())
        r["tau_lo"], r["tau_hi"] = np.percentile(bt, [2.5, 97.5])
        r["strict_lo"], r["strict_hi"] = np.percentile(bs, [2.5, 97.5])
        rows.append(r)
    R = pd.DataFrame(rows).sort_values("kendall_tau", ascending=False)
    out = base / "analysis"
    out.mkdir(parents=True, exist_ok=True)
    R.to_csv(out / "monotonicity.csv", index=False)
    txt = [f"# Monotonicity at fixed surface — {args.tag} (n={int(R.n.max())} targets)\n",
           "## Controlled ladder (3 edit sites in every cell; only the number of meaning-changing edits varies)\n",
           md(R[["metric", "step_M1>M0", "step_M2>M1", "step_M3>M2", "strict_monotone", "weak_monotone", "kendall_tau", "tau_lo", "tau_hi"]]), "",
           "## Mean standardised penalty per cell\n", md(R[["metric", "z_M0", "z_M1", "z_M2", "z_M3", "z_K1", "z_K2"]], 2), "",
           "## Three harmless edits vs one real error, and the uncontrolled ladder\n",
           md(R[["metric", "benign_over_error_M0>K1", "uncontrolled_K2>K1", "uncontrolled_M3>K2"]]), ""]
    (out / "MONO.md").write_text("\n".join(txt))
    print("\n".join(txt))


if __name__ == "__main__":
    main()
