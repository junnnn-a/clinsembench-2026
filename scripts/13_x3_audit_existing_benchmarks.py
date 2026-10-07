#!/usr/bin/env python
"""
13_x3_audit_existing_benchmarks.py — X3: can the labels of existing perturbation benchmarks be predicted
from surface features alone?

  (a) ClinSemBench v1 (ARR May): subset200 impression/findings (rule labels) and the 480-pair human-validated
      set (human majority labels) — READ-ONLY from the old directory.
  (b) our factorial set (full IU / MIMIC): the same classifier in the confounded vs controlled conditions.
  (c) ReEvalMed: published per-metric means on clinically significant vs insignificant pairs (their Table;
      numbers copied into docs/3 §1.3). Only the direction of surface metrics can be analysed without the data.

The surface-only classifier is the one of 6_shortcut_floor.py (same features, logistic regression,
5-fold GroupKFold by report).  Output: results/3_x3_audit/table3.csv + TABLE3.md
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

NEW = Path(__file__).resolve().parent.parent
OLD = Path("/home/irteam/junah-data-1/2_ClinSevBench/ClinSevBench_v2")
spec = importlib.util.spec_from_file_location("floor", NEW / "scripts/6_shortcut_floor.py")
F = importlib.util.module_from_spec(spec); spec.loader.exec_module(F)
BENIGN = {"benign_format", "benign_sentence_order", "benign_paraphrase_rule"}


def surface_table(df, label_col, group_col):
    feats = pd.DataFrame([F.features(r, h) for r, h in zip(df.reference, df.candidate)])
    y = df[label_col].to_numpy().astype(int)
    X = feats.to_numpy()
    lr = F.cv_auc(X, y, df[group_col].to_numpy())
    single = {c: roc_auc_score(y, feats[c]) for c in feats.columns if feats[c].nunique() > 1}
    best = max(single, key=lambda k: abs(single[k] - 0.5))
    return lr, single.get("jaccard_drop", np.nan), single.get("edit_tokens", np.nan), best, single[best]


def main():
    out = NEW / "results/3_x3_audit"
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    # ---- (a) v1
    for sec in ["impression", "findings"]:
        d = pd.read_csv(OLD / f"data/minpairs/pairs_{sec}_clean_metric_subset_200.csv")
        d = d[d.perturbation_type != "identity"].copy()
        d["y"] = (~d.perturbation_type.isin(BENIGN)).astype(int)
        lr, jac, et, best, bv = surface_table(d, "y", "report_id")
        rows.append({"benchmark": f"ClinSemBench v1 ({sec}, rule labels)", "n": len(d), "surface_only_LR_auroc": lr,
                     "jaccard_drop_auroc": jac, "edit_tokens_auroc": et, "strongest_single_feature": f"{best}={bv:.3f}",
                     "direction": "larger surface change => benign" if et < 0.5 else "larger surface change => changed"})
    h = pd.read_csv(OLD / "results/analysis/annotation480_human_majority_auroc/annotation_metric_candidates_with_labels.csv")
    h = h.dropna(subset=["human_is_changed"]).copy()
    lr, jac, et, best, bv = surface_table(h, "human_is_changed", "report_id")
    rows.append({"benchmark": "ClinSemBench v1 (480-pair set, human labels)", "n": len(h), "surface_only_LR_auroc": lr,
                 "jaccard_drop_auroc": jac, "edit_tokens_auroc": et, "strongest_single_feature": f"{best}={bv:.3f}",
                 "direction": "larger surface change => benign" if et < 0.5 else "larger surface change => changed"})
    # ---- (b) ours
    for corpus in ["iu", "mimic"]:
        p = NEW / f"data/pairs/full_{corpus}_all.csv"
        if not p.exists():
            continue
        d = pd.read_csv(p)
        for name, (cc, pc) in {"confound v1-type (C0 vs P1)": ("C0", "P1"), "confound ReEvalMed-type (C0 vs P2)": ("C0", "P2"),
                               "controlled S0 (C0 vs P0)": ("C0", "P0"), "controlled S2 (C2 vs P2)": ("C2", "P2")}.items():
            s = d[d.cell.isin([cc, pc])]
            lr, jac, et, best, bv = surface_table(s, "is_changed", "report_id")
            rows.append({"benchmark": f"factorial {corpus.upper()} — {name}", "n": len(s), "surface_only_LR_auroc": lr,
                         "jaccard_drop_auroc": jac, "edit_tokens_auroc": et, "strongest_single_feature": f"{best}={bv:.3f}",
                         "direction": ("≈ none" if abs(et - 0.5) < 0.05 and abs(jac - 0.5) < 0.1 else
                                       "larger surface change => benign" if et < 0.5 else "larger surface change => changed")})
    T = pd.DataFrame(rows)
    T.to_csv(out / "table3.csv", index=False)

    # ---- (c) ReEvalMed published means (score on significant-error pairs vs insignificant-rewrite pairs, 0-100)
    R = pd.DataFrame([("BLEU", 78.48, 41.89), ("ROUGE-L", 87.90, 65.95), ("RadGraph", 81.35, 58.56), ("BERT-F1", 97.31, 92.99),
                      ("GREEN", 74.30, 74.76)], columns=["metric", "mean_score_significant_error_pairs", "mean_score_insignificant_pairs"])
    R["score_gap(sig - insig)"] = R.mean_score_significant_error_pairs - R.mean_score_insignificant_pairs
    R["rewards_the_erroneous_candidate"] = R["score_gap(sig - insig)"] > 0
    R.to_csv(out / "reevalmed_published_means.csv", index=False)

    def md(df, f=3):
        d = df.copy()
        for c in d.columns:
            if pd.api.types.is_float_dtype(d[c]):
                d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.{f}f}")
        cols = [str(c) for c in d.columns]
        return "\n".join(["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"] +
                         ["| " + " | ".join(map(str, r)) + " |" for r in d.itertuples(index=False)])
    txt = ["# X3 — surface-only predictability of benchmark labels\n", md(T), "",
           "## ReEvalMed (published per-metric means; data not available locally)\n", md(R, 2), ""]
    (out / "TABLE3.md").write_text("\n".join(txt))
    print("\n".join(txt))


if __name__ == "__main__":
    main()
