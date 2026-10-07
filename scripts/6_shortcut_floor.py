#!/usr/bin/env python
"""
6_shortcut_floor.py — meaning-blind (surface-only) classifier for each comparison condition.

Features computed from (reference, candidate) only: Jaccard drop, token-F1 drop, difflib ratio,
character-level ratio, #edited tokens, length ratio, |length diff|, bag-changed flag, #numbers changed.
Model: logistic regression, 5-fold GroupKFold by report. Report AUROC per condition plus the
single-feature AUROCs. Target: 0.45–0.55 in the controlled conditions (docs/3 §5.3).

Conditions
  controlled_S0 : C0 vs P0        controlled_S1 : C1 vs P1       controlled_S2 : C2 vs P2
  confound_v1   : C0 vs P1        confound_reevalmed : C0 vs P2
  pooled        : all C vs all P
"""
from __future__ import annotations

import argparse
import difflib
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

NEW = Path(__file__).resolve().parent.parent
TOKEN_RE = re.compile(r"\b\w+\b")
NUM_RE = re.compile(r"\d+(?:\.\d+)?")

CONDITIONS = {
    "controlled_S0": ("C0", "P0"), "controlled_S1": ("C1", "P1"), "controlled_S2": ("C2", "P2"),
    "confound_v1": ("C0", "P1"), "confound_reevalmed": ("C0", "P2"),
}


def toks(t):
    return TOKEN_RE.findall(re.sub(r"[^a-z0-9. ]+", " ", str(t).lower()))


def token_f1(r, h):
    a, b = Counter(toks(r)), Counter(toks(h))
    inter = sum((a & b).values())
    if not inter:
        return 0.0
    p, rc = inter / sum(b.values()), inter / sum(a.values())
    return 2 * p * rc / (p + rc)


def jaccard(r, h):
    a, b = set(toks(r)), set(toks(h))
    return len(a & b) / len(a | b) if a | b else 1.0


def features(r, h):
    rt, ht = str(r).split(), str(h).split()
    sm = difflib.SequenceMatcher(a=rt, b=ht, autojunk=False)
    et = sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal")
    return {
        "jaccard_drop": 1 - jaccard(r, h),
        "tokenf1_drop": 1 - token_f1(r, h),
        "seq_ratio_drop": 1 - sm.ratio(),
        "char_ratio_drop": 1 - difflib.SequenceMatcher(a=str(r), b=str(h), autojunk=False).ratio(),
        "edit_tokens": et,
        "edit_frac": et / max(1, len(rt)),
        "len_ratio": len(ht) / max(1, len(rt)),
        "abs_len_diff": abs(len(ht) - len(rt)),
        "bag_changed": float(Counter(toks(r)) != Counter(toks(h))),
        "numbers_changed": float(sorted(NUM_RE.findall(str(r))) != sorted(NUM_RE.findall(str(h)))),
    }


def cv_auc(X, y, groups, seed=0):
    if len(np.unique(y)) < 2:
        return np.nan
    gkf = GroupKFold(n_splits=5)
    pred = np.zeros(len(y))
    for tr, te in gkf.split(X, y, groups):
        clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=1.0))
        clf.fit(X[tr], y[tr])
        pred[te] = clf.predict_proba(X[te])[:, 1]
    return roc_auc_score(y, pred)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs_csv", required=True)
    ap.add_argument("--out_csv", required=True)
    args = ap.parse_args()
    df = pd.read_csv(args.pairs_csv)
    df = df[df.cell != "identity"].copy()
    F = pd.DataFrame([features(r, h) for r, h in zip(df.reference, df.candidate)])
    df = pd.concat([df.reset_index(drop=True), F], axis=1)
    feat_cols = list(F.columns)
    rows = []
    conds = dict(CONDITIONS)
    conds["pooled"] = (tuple(c for c in df.cell.unique() if c.startswith("C")), tuple(c for c in df.cell.unique() if c.startswith("P")))
    for name, (cc, pc) in conds.items():
        cc = (cc,) if isinstance(cc, str) else cc
        pc = (pc,) if isinstance(pc, str) else pc
        sub = df[df.cell.isin(cc + pc)]
        if sub.empty or sub.is_changed.nunique() < 2:
            continue
        y = sub.is_changed.to_numpy()
        row = {"condition": name, "n": len(sub), "n_changed": int(y.sum()),
               "surface_only_LR_auroc": cv_auc(sub[feat_cols].to_numpy(), y, sub.report_id.to_numpy())}
        for f in feat_cols:
            row[f"auc:{f}"] = roc_auc_score(y, sub[f]) if sub[f].nunique() > 1 else np.nan
        rows.append(row)
        for et, g in sub.groupby("edit_type"):
            if g.is_changed.nunique() < 2:
                continue
            rows.append({"condition": f"{name}/{et}", "n": len(g), "n_changed": int(g.is_changed.sum()),
                         "surface_only_LR_auroc": cv_auc(g[feat_cols].to_numpy(), g.is_changed.to_numpy(), g.report_id.to_numpy())})
    out = pd.DataFrame(rows)
    Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out_csv, index=False)
    pd.set_option("display.width", 250)
    print(out[["condition", "n", "n_changed", "surface_only_LR_auroc"] + [c for c in out.columns if c.startswith("auc:")]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
