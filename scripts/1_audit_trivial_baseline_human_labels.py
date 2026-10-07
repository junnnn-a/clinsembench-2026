#!/usr/bin/env python
"""
1_audit_trivial_baseline_human_labels.py
READ-ONLY. Trivial lexical baselines on the 480-pair human-validated set
(same 467 non-UNCERTAIN items as paper Table 3, human-label column).
Outputs -> results/0_audit/F_*.csv
"""
import importlib.util, sys
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("audit0", HERE / "0_audit_prior_experiment.py")
a0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(a0)

OUT = HERE.parent / "results/0_audit"
c = pd.read_csv(a0.OLD / "results/analysis/annotation480_human_majority_auroc/annotation_metric_candidates_with_labels.csv")
c["token_f1_penalty"] = [1 - a0.token_f1(r, h) for r, h in zip(c.reference, c.candidate)]
c["jaccard_penalty"] = [1 - a0.jaccard(r, h) for r, h in zip(c.reference, c.candidate)]
c["bow_changed_penalty"] = (c.token_f1_penalty > 1e-12).astype(float)
c["neg_edit_tokens_penalty"] = [-a0.token_edit_ops(r, h) for r, h in zip(c.reference, c.candidate)]
for m in a0.PAPER_METRICS:
    c[f"{m}_penalty"] = c[f"{m}_identity"] - c[m]
rows = []
for label, ycol in [("human_majority(n=467)", "human_is_changed"), ("rule(n=480)", "rule_is_changed")]:
    s = c.dropna(subset=[ycol])
    for m in a0.PAPER_METRICS + ["jaccard", "token_f1", "bow_changed", "neg_edit_tokens"]:
        ss = s.dropna(subset=[f"{m}_penalty"])
        rows.append({"label_source": label, "metric": m, "n": len(ss),
                     "auroc": roc_auc_score(ss[ycol].astype(int), ss[f"{m}_penalty"])})
out = pd.DataFrame(rows)
out.to_csv(OUT / "F_trivial_baselines_on_human_labels.csv", index=False)
print(out.pivot(index="metric", columns="label_source", values="auroc").sort_values("human_majority(n=467)", ascending=False).round(3).to_string())
