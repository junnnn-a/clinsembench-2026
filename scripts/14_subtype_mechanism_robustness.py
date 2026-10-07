#!/usr/bin/env python
"""
14_subtype_mechanism_robustness.py — follow-up analyses on the full factorial set.

 (1) subtype breakdown (dose-response): paired accuracy per edit_type x subtype in controlled S0 / S2
     (severity adjacent vs extreme, measurement value vs unit(10x), uncertainty/negation direction).
 (2) robustness of the controlled-S0/S2 paired accuracy to
        - dropping targets whose P lexicon is flagged for expert review
        - keeping only shape-identical P/C pairs (shape_sign == equal)
        - section (findings vs impression)
 (3) mechanism (E8) with CRIMSON's error categories: for each edit type, which category count rises in the
     C0 candidate relative to identity, and which rises (wrongly) in P0.
 (4) error-enumeration judges: mean number of listed errors per cell (surface dose-response).

Inputs: data/pairs/full_{corpus}_all.csv, full_{corpus}_targets.csv, results/2_full_{corpus}/analysis/penalties_long.csv,
        results/2_full_{corpus}/scores/crimson.csv, results/2_full_{corpus}/judges/*__errors.csv
Outputs: results/2_full_{corpus}/analysis/{subtype.csv, robustness.csv, crimson_categories.csv, error_counts.csv, FOLLOWUP.md}
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

NEW = Path(__file__).resolve().parent.parent
CONDS = {"controlled_S0": ("C0", "P0"), "controlled_S2": ("C2", "P2"), "confound_v1": ("C0", "P1"), "confound_reevalmed": ("C0", "P2")}
MAIN = ["jaccard", "bertscore_distilbert", "bertscore_deberta_mnli", "radgraph", "ratescore", "radcliq", "f1chexbert", "srrbert", "green",
        "crimson", "llama31_8b__rubric", "gemma3_27b__rubric", "qwen3_32b__rubric", "gptoss_20b__rubric"]


def md(df, f=3):
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.{f}f}")
    cols = [str(c) for c in d.columns]
    return "\n".join(["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"] +
                     ["| " + " | ".join(map(str, r)) + " |" for r in d.itertuples(index=False)])


def pa(w, m, cc, pc):
    a, b = w.get(f"{m}__D__{cc}"), w.get(f"{m}__D__{pc}")
    if a is None or b is None:
        return np.nan
    d = (a - b).dropna()
    return float(((d > 0) + 0.5 * (d == 0)).mean()) if len(d) else np.nan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    args = ap.parse_args()
    c = args.corpus
    adir = NEW / f"results/2_full_{c}/analysis"
    pen = pd.read_csv(adir / "penalties_long.csv")
    tg = pd.read_csv(NEW / f"data/pairs/full_{c}_targets.csv")
    metrics = [m for m in MAIN if f"{m}__D" in pen.columns]
    wide = pen.pivot_table(index="target_id", columns="cell", values=[f"{m}__D" for m in metrics])
    wide.columns = [f"{a}__{b}" for a, b in wide.columns]
    wide = wide.reset_index().merge(tg[["target_id", "edit_type", "subtype", "pattern", "section", "shape_sign", "needs_expert_review", "target_negated"]], on="target_id")

    # ---- (1) subtype
    rows = []
    for (et, st), g in wide.groupby(["edit_type", "subtype"]):
        for cond in ["controlled_S0", "controlled_S2"]:
            r = {"edit_type": et, "subtype": st, "condition": cond, "n": len(g)}
            r.update({m: pa(g, m, *CONDS[cond]) for m in metrics})
            rows.append(r)
    sub = pd.DataFrame(rows)
    sub.to_csv(adir / "subtype.csv", index=False)

    # ---- (2) robustness
    rows = []
    filters = {"all": wide, "exclude_expert_flagged_P": wide[~wide.needs_expert_review], "shape_equal_only": wide[wide.shape_sign == "equal"],
               "findings_only": wide[wide.section == "findings"], "impression_only": wide[wide.section == "impression"]}
    for name, w in filters.items():
        for cond in ["controlled_S0", "controlled_S2", "confound_v1", "confound_reevalmed"]:
            r = {"subset": name, "condition": cond, "n": len(w)}
            r.update({m: pa(w, m, *CONDS[cond]) for m in metrics})
            rows.append(r)
    rob = pd.DataFrame(rows)
    rob.to_csv(adir / "robustness.csv", index=False)

    # ---- (3) CRIMSON categories
    cr = pd.read_csv(NEW / f"results/2_full_{c}/scores/crimson.csv")
    cats = [x for x in cr.columns if x.startswith("crimson_") and x not in ("crimson_raw", "crimson_parse_error") and pd.api.types.is_numeric_dtype(cr[x])]
    pairs = pd.read_csv(NEW / f"data/pairs/full_{c}_all.csv")[["uid", "target_id", "cell", "edit_type"]]
    d = pairs.merge(cr[["uid"] + cats], on="uid")
    idn = d[d.cell == "identity"].set_index("target_id")[cats]
    out = []
    for cell in ["P0", "C0", "P2", "C2"]:
        s = d[d.cell == cell].set_index("target_id")
        delta = (s[cats] - idn.reindex(s.index)[cats]).clip(lower=0)
        delta["edit_type"] = s.edit_type
        g = delta.groupby("edit_type")[cats].mean().reset_index()
        g.insert(0, "cell", cell)
        out.append(g)
    cc = pd.concat(out, ignore_index=True)
    cc.columns = [x.replace("crimson_", "") for x in cc.columns]
    cc.to_csv(adir / "crimson_categories.csv", index=False)

    # ---- (4) error-enumeration judges: number of listed errors per cell
    ec = []
    for f in sorted((NEW / f"results/2_full_{c}/judges").glob("*__errors.csv")):
        j = pd.read_csv(f)
        col = f.stem
        dd = pairs.merge(j[["uid", f"{col}__conf"]], on="uid")
        r = dd.groupby("cell")[f"{col}__conf"].mean().to_dict()
        ec.append({"judge": col, **{k: r.get(k, np.nan) for k in ["identity", "P0", "P1", "P2", "C0", "C1", "C2"]}})
    ec = pd.DataFrame(ec)
    ec.to_csv(adir / "error_counts.csv", index=False)

    show = ["jaccard", "bertscore_deberta_mnli", "radcliq", "ratescore", "green", "crimson", "gemma3_27b__rubric", "qwen3_32b__rubric", "gptoss_20b__rubric"]
    show = [m for m in show if m in metrics]
    rep = [f"# Follow-up analyses — full {c.upper()}\n", "## 1. Subtype paired accuracy (controlled S0)\n",
           md(sub[sub.condition == "controlled_S0"][["edit_type", "subtype", "n"] + show]), "",
           "## 1b. Subtype paired accuracy (controlled S2)\n", md(sub[sub.condition == "controlled_S2"][["edit_type", "subtype", "n"] + show]), "",
           "## 2. Robustness (paired accuracy)\n", md(rob[["subset", "condition", "n"] + show]), "",
           "## 3. CRIMSON error categories: mean increase over identity, by edit type and cell\n", md(cc, 2), "",
           "## 4. Error-enumeration prompt: mean number of listed discrepancies per cell\n", md(ec, 2) if len(ec) else "(no errors-prompt judges)", ""]
    (adir / "FOLLOWUP.md").write_text("\n".join(rep))
    print("\n".join(rep))


if __name__ == "__main__":
    main()
