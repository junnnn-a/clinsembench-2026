#!/usr/bin/env python
"""
8_analyze_factorial.py — main analysis of the factorial set.

Inputs
  --pairs   pairs file with cells (identity, P0, C0, P1, C1, P2, C2)  e.g. data/pairs/pilot_iu_all.csv
  --scores  one or more directories with per-metric CSVs (uid + score columns); judges use the same format

Penalty: D = s(identity) - s(cell) per target (orientation fixed so that higher score = closer to reference).

Conditions (each compares C vs P *within the same target*):
  controlled_S0  C0 vs P0      controlled_S1  C1 vs P1      controlled_S2  C2 vs P2
  confound_v1    C0 vs P1      confound_reevalmed  C0 vs P2
Statistics per metric x condition:
  paired_acc  = mean over targets of 1[D(C) > D(P)] (+0.5 for ties)
  auroc       = AUROC of D over the two cells (item level)
  gap         = mean D(C) - mean D(P)
  CI          = report-cluster bootstrap (95%)
Decomposition (z-scored D within metric):
  meaning_effect = mean z(D(C0)) - mean z(D(P0))
  surface_S1     = mean z(D(P1)) - mean z(D(P0))      surface_S2 = mean z(D(P2)) - mean z(D(P0))
  interaction_S2 = [D(C2)-D(P2)] - [D(C0)-D(P0)]
Outputs: {out}/summary_by_condition.csv, per_type.csv, decomposition.csv, penalties_long.csv, REPORT.md
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

ORIENT_LOWER_BETTER = {"radcliq", "radgraph_radcliq"}          # score is an error/distance
CONDITIONS = {"controlled_S0": ("C0", "P0"), "controlled_S1": ("C1", "P1"), "controlled_S2": ("C2", "P2"),
              "confound_v1": ("C0", "P1"), "confound_reevalmed": ("C0", "P2")}


def load_scores(dirs):
    """Files with the same basename in different dirs (e.g. scores_S0S1/green.csv, scores_S2/green.csv)
    are stacked row-wise; different metrics are joined column-wise on uid."""
    by_name = {}
    for d in dirs:
        for f in sorted(Path(d).glob("*.csv")):
            df = pd.read_csv(f)
            if "uid" not in df.columns:
                continue
            cols = [c for c in df.columns if c != "uid" and pd.api.types.is_numeric_dtype(df[c])
                    and not c.endswith(("__conf", "__label")) and not c.startswith("crimson_")]
            by_name.setdefault(f.name, []).append(df[["uid"] + cols])
    parts = [pd.concat(v, ignore_index=True).drop_duplicates("uid").set_index("uid") for v in by_name.values()]
    S = pd.concat(parts, axis=1)
    S = S.loc[:, ~S.columns.duplicated()]
    return S


def cluster_boot(vals_by_report, stat_fn, n_boot=1000, seed=0):
    rng = np.random.default_rng(seed)
    keys = list(vals_by_report)
    out = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(keys), size=len(keys))
        arr = np.concatenate([vals_by_report[keys[i]] for i in pick])
        out.append(stat_fn(arr))
    return float(np.nanpercentile(out, 2.5)), float(np.nanpercentile(out, 97.5))


def paired_stat(arr):          # arr: n x 2  (D_C, D_P)
    d = arr[:, 0] - arr[:, 1]
    return float(np.mean((d > 0) + 0.5 * (d == 0)))


def auc_stat(arr):
    y = np.r_[np.ones(len(arr)), np.zeros(len(arr))]
    s = np.r_[arr[:, 0], arr[:, 1]]
    ok = np.isfinite(s)
    return float(roc_auc_score(y[ok], s[ok])) if ok.sum() > 2 else np.nan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--scores", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n_boot", type=int, default=1000)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    pairs = pd.read_csv(args.pairs)
    S = load_scores(args.scores)
    metrics = list(S.columns)
    df = pairs.merge(S, left_on="uid", right_index=True, how="left")
    for m in metrics:
        if m in ORIENT_LOWER_BETTER:
            df[m] = -df[m]
    # identity baseline per target
    idn = df[df.cell == "identity"].set_index("target_id")[metrics]
    cand = df[df.cell != "identity"].copy()
    for m in metrics:
        cand[f"{m}__D"] = cand.target_id.map(idn[m]) - cand[m]
    cand.to_csv(out / "penalties_long.csv", index=False)

    # wide: one row per target, columns D_{metric}_{cell}
    wide = cand.pivot_table(index=["target_id", "report_id", "edit_type", "subtype", "section"],
                            columns="cell", values=[f"{m}__D" for m in metrics]).reset_index()
    wide.columns = ["__".join([c for c in col if c]) if isinstance(col, tuple) else col for col in wide.columns]
    # ---- summary by condition
    rows, per_type = [], []
    for m in metrics:
        for cond, (cc, pc) in CONDITIONS.items():
            ccol, pcol = f"{m}__D__{cc}", f"{m}__D__{pc}"
            if ccol not in wide or pcol not in wide:
                continue
            w = wide.dropna(subset=[ccol, pcol])
            if w.empty:
                continue
            arr = w[[ccol, pcol]].to_numpy(float)
            groups = {k: g[[ccol, pcol]].to_numpy(float) for k, g in w.groupby("report_id")}
            pa = paired_stat(arr)
            lo, hi = cluster_boot(groups, paired_stat, args.n_boot)
            au = auc_stat(arr)
            alo, ahi = cluster_boot(groups, auc_stat, args.n_boot)
            rows.append({"metric": m, "condition": cond, "n_targets": len(w), "paired_acc": pa, "pa_ci_lo": lo, "pa_ci_hi": hi,
                         "auroc": au, "auc_ci_lo": alo, "auc_ci_hi": ahi,
                         "mean_D_C": float(arr[:, 0].mean()), "mean_D_P": float(arr[:, 1].mean()), "gap": float((arr[:, 0] - arr[:, 1]).mean())})
            for et, g in w.groupby("edit_type"):
                a = g[[ccol, pcol]].to_numpy(float)
                per_type.append({"metric": m, "condition": cond, "edit_type": et, "n": len(g),
                                 "paired_acc": paired_stat(a), "auroc": auc_stat(a), "gap": float((a[:, 0] - a[:, 1]).mean())})
    summ = pd.DataFrame(rows)
    pt = pd.DataFrame(per_type)
    summ.to_csv(out / "summary_by_condition.csv", index=False)
    pt.to_csv(out / "per_type.csv", index=False)

    # ---- decomposition on z-scored penalties
    dec = []
    for m in metrics:
        cols = {c: f"{m}__D__{c}" for c in ["P0", "C0", "P1", "C1", "P2", "C2"] if f"{m}__D__{c}" in wide}
        allD = cand[f"{m}__D"].dropna()
        mu, sd = allD.mean(), allD.std(ddof=0) or 1.0
        z = {c: (wide[col] - mu) / sd for c, col in cols.items()}
        r = {"metric": m, "sd_D": sd}
        if "P0" in z and "C0" in z:
            r["meaning_effect_S0"] = float((z["C0"] - z["P0"]).mean())
        if "P1" in z:
            r["surface_S1"] = float((z["P1"] - z["P0"]).mean())
        if "P2" in z:
            r["surface_S2"] = float((z["P2"] - z["P0"]).mean())
        if "C2" in z and "P2" in z:
            r["meaning_effect_S2"] = float((z["C2"] - z["P2"]).mean())
            r["interaction_S2"] = r["meaning_effect_S2"] - r["meaning_effect_S0"]
        if "C1" in z and "P1" in z:
            r["meaning_effect_S1"] = float((z["C1"] - z["P1"]).mean())
        dec.append(r)
    dec = pd.DataFrame(dec)
    dec.to_csv(out / "decomposition.csv", index=False)

    # ---- report
    def md(df, f=3):
        d = df.copy()
        for c in d.columns:
            if pd.api.types.is_float_dtype(d[c]):
                d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.{f}f}")
        cols = [str(c) for c in d.columns]
        return "\n".join(["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"] +
                         ["| " + " | ".join(map(str, r)) + " |" for r in d.itertuples(index=False)])
    rep = [f"# Factorial analysis — {args.pairs}\n", "## Paired accuracy by condition\n",
           md(summ.pivot(index="metric", columns="condition", values="paired_acc").reset_index()), "",
           "## AUROC by condition\n", md(summ.pivot(index="metric", columns="condition", values="auroc").reset_index()), "",
           "## Decomposition (z-scored penalties)\n", md(dec), ""]
    for cond in CONDITIONS:
        sub = pt[pt.condition == cond]
        if sub.empty:
            continue
        rep += [f"## Per-type paired accuracy — {cond}\n", md(sub.pivot(index="metric", columns="edit_type", values="paired_acc").reset_index()), ""]
    (out / "REPORT.md").write_text("\n".join(rep))
    print("\n".join(rep))


if __name__ == "__main__":
    main()
