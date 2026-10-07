#!/usr/bin/env python
"""
23_external_validity.py — does a metric's score on OUR comparisons predict its agreement with radiologists? (10/7 review, "so what")

Human reference: RaTE-Eval (public, CC-BY-4.0)
  Task 1: 2,216 sentence pairs (441 test + 1,775 train) with radiologist error counts (normalised by number of findings)
  Task 2: 370 test paragraph pairs with a 0-5 radiologist score
Step 1 (--build): write data/pairs/full_rate1_all.csv / full_rate2_all.csv in the pipeline format; score with
        `bash scripts/run_set.sh rate1` and `NO_LLM=1 bash scripts/run_set.sh rate2`.
Step 2 (--analyze): Kendall tau of every metric / judge with the human rating; then, ACROSS metrics, the rank correlation
        between that tau and the metric's paired accuracy under Ctrl-0, Ctrl-2, Conf-R, Conf-P and its fixed-surface monotonicity tau.
        The question: which of our columns orders metrics the way radiologists do?

Output: results/4_external_validity/{human_tau.csv, across_metrics.csv, EXTERNAL.md}
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, spearmanr

NEW = Path(__file__).resolve().parent.parent
B = NEW / "data/external/RaTE-Eval"
OUT = NEW / "results/4_external_validity"


def build():
    rows, key = [], []
    for split in ["test", "train"]:
        d = pd.read_csv(B / f"Task1_sentence_rate/rate_{split}.csv").dropna(subset=["normalized"])
        for i, r in enumerate(d.itertuples()):
            uid = f"rate1_{split}_{i}"
            rows.append(dict(uid=uid, target_id=uid, corpus="rate1", report_id=uid, section="sentence", edit_type="rate1", subtype=split, pattern="", edit_detail="",
                             target_idx=0, needs_expert_review=False, cell="X", surface_layer="X", is_changed=0, reference=r.gt_report, candidate=r.similar_report))
            key.append(dict(uid=uid, split=split, human=r.normalized, human_higher_is_better=False, modality=r.file_name))
    pd.DataFrame(rows).to_csv(NEW / "data/pairs/full_rate1_all.csv", index=False)
    n1 = len(rows)
    rows2 = []
    d = pd.read_csv(B / "Task2_paragraph_rate/rate_test.csv")
    d["Score"] = pd.to_numeric(d.Score, errors="coerce")
    d = d.dropna(subset=["Score"])
    for i, r in enumerate(d.itertuples()):
        uid = f"rate2_test_{i}"
        rows2.append(dict(uid=uid, target_id=uid, corpus="rate2", report_id=uid, section="paragraph", edit_type="rate2", subtype="test", pattern="", edit_detail="",
                          target_idx=0, needs_expert_review=False, cell="X", surface_layer="X", is_changed=0, reference=r.gt_report, candidate=r.similar_report))
        key.append(dict(uid=uid, split="test", human=r.Score, human_higher_is_better=True, modality=r.type))
    pd.DataFrame(rows2).to_csv(NEW / "data/pairs/full_rate2_all.csv", index=False)
    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(key).to_csv(OUT / "human_key.csv", index=False)
    print(f"rate1: {n1} pairs, rate2: {len(rows2)} pairs")


def load_scores(tag):
    spec = importlib.util.spec_from_file_location("ext", NEW / "scripts/14_extended_analysis.py")
    EXT = importlib.util.module_from_spec(spec); spec.loader.exec_module(EXT)
    base = NEW / f"results/2_full_{tag}"
    parts = []
    for d in ["scores", "judges"]:
        for f in sorted((base / d).glob("*.csv")):
            df = pd.read_csv(f)
            cols = [c for c in df.columns if c != "uid" and pd.api.types.is_numeric_dtype(df[c]) and not c.endswith(("__conf", "__label")) and not c.startswith("crimson_")]
            parts.append(df[["uid"] + cols].drop_duplicates("uid").set_index("uid"))
    S = pd.concat(parts, axis=1)
    for c in S.columns:
        if c in EXT.ORIENT_LOWER_BETTER:
            S[c] = -S[c]                                  # orient every scorer as "higher = closer to the reference"
    return S.reset_index()


def analyze(n_boot=1000):
    key = pd.read_csv(OUT / "human_key.csv")
    rows = []
    for tag, sub, name in [("rate1", "test", "Task 1 (sentence)"), ("rate2", "test", "Task 2 (paragraph)")]:
        if not (NEW / f"results/2_full_{tag}/scores").exists():
            continue
        sc = load_scores(tag).merge(key, on="uid")
        if sub:
            sc = sc[sc.split == sub]
        for m in [c for c in sc.columns if c not in key.columns]:
            v = sc[[m, "human"]].apply(pd.to_numeric, errors="coerce").dropna()
            if len(v) < 50 or v[m].nunique() < 2:
                continue
            sign = 1 if bool(sc.human_higher_is_better.iloc[0]) else -1
            rows.append({"set": name, "metric": m, "n": len(v), "human_tau": sign * kendalltau(v[m], v.human).correlation})
    H = pd.DataFrame(rows)
    H.to_csv(OUT / "human_tau.csv", index=False)
    # our columns (mean of IU and MIMIC) and the fixed-surface monotonicity tau
    S = pd.concat([pd.read_csv(NEW / f"results/2_full_{c}/analysis/summary_by_condition.csv") for c in ["iu", "mimic"]])
    ours = S.groupby(["metric", "condition"]).paired_acc.mean().unstack()
    ours = ours.rename(columns={"controlled_S0": "Ctrl-0", "controlled_S1": "Ctrl-1", "controlled_S2": "Ctrl-2", "confound_v1": "Conf-R", "confound_reevalmed": "Conf-P"})
    mono = pd.read_csv(NEW / "results/2_full_mimicmono/analysis/monotonicity.csv").set_index("metric")
    ours["mono tau (fixed surface)"] = mono.kendall_tau
    ours["mono growing-surface step"] = mono["uncontrolled_K2>K1"]
    rows, rng = [], np.random.default_rng(0)
    for name, h in H.groupby("set"):
        h = h.set_index("metric").human_tau
        for col in ["Conf-R", "Conf-P", "Ctrl-0", "Ctrl-1", "Ctrl-2", "mono growing-surface step", "mono tau (fixed surface)"]:
            for subset, keep in [("all scorers", lambda m: True), ("metrics only (no LLM judges)", lambda m: "__" not in m)]:
                d = pd.concat([h, ours[col]], axis=1, keys=["human", "ours"]).dropna()
                d = d[[keep(m) for m in d.index]]
                if len(d) < 6:
                    continue
                rho = spearmanr(d.human, d.ours).correlation
                perm = np.array([spearmanr(d.human, rng.permutation(d.ours.to_numpy())).correlation for _ in range(5000)])
                boot = []
                for _ in range(2000):
                    i = rng.integers(0, len(d), len(d))
                    if d.ours.iloc[i].nunique() > 2:
                        boot.append(spearmanr(d.human.iloc[i], d.ours.iloc[i]).correlation)
                rows.append({"human set": name, "scorers": subset, "our column": col, "n_scorers": len(d), "spearman": rho,
                             "ci_lo": np.nanpercentile(boot, 2.5), "ci_hi": np.nanpercentile(boot, 97.5), "perm_p": float((np.abs(perm) >= abs(rho)).mean())})
    X = pd.DataFrame(rows)
    X.to_csv(OUT / "across_metrics.csv", index=False)
    T = H.pivot(index="metric", columns="set", values="human_tau").join(ours[["Conf-R", "Conf-P", "Ctrl-0", "Ctrl-2", "mono tau (fixed surface)"]]).reset_index()
    T.to_csv(OUT / "per_metric.csv", index=False)
    spec = importlib.util.spec_from_file_location("ext", NEW / "scripts/14_extended_analysis.py")
    EXT = importlib.util.module_from_spec(spec); spec.loader.exec_module(EXT)
    txt = ["# External validity: do our columns order scorers the way radiologists do? (RaTE-Eval Tasks 1-2)\n",
           "## Per scorer: Kendall tau with radiologist ratings, and our paired accuracies (mean of IU and MIMIC)\n", EXT.md(T), "",
           "## Across scorers: Spearman correlation between human tau and each of our columns\n", EXT.md(X), ""]
    (OUT / "EXTERNAL.md").write_text("\n".join(txt))
    print("\n".join(txt))
    return H, X


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--analyze", action="store_true")
    a = ap.parse_args()
    if a.build:
        build()
    if a.analyze:
        analyze()
