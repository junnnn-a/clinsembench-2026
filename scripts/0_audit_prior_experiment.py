#!/usr/bin/env python
"""
0_audit_prior_experiment.py

READ-ONLY audit of the ARR-May ClinSemBench experiment directory.
Nothing is written to the old directory; all outputs go to --out_dir
inside the ARR-October experiment directory.

Audits
  A. Trivial lexical baselines on the *same* subset200 used for Table 3
     (pooled AUROC + per-type AUROC) -> is the benchmark solvable by bag-of-words?
  B. Edit-magnitude confound (token edit distance per perturbation type,
     correlation of each metric's penalty with edit size,
     changed-type x benign-type AUROC matrix).
  C. Rule-quality heuristics (ungrammatical / ambiguous / off-spec edits).
  D. Section provenance (findings/impression fallback in prepare()).
  E. Human-annotation structure (single vs. triple annotated, per-annotator).
  F. Report-clustered bootstrap CI vs. the candidate-level CI used in the paper.

The fast-metric functions below are copied from
  2_ClinSevBench/ClinSevBench_v2/scripts/clinsev_pipeline.py (ARR-May version)
so that the numbers are computed with the identical definitions.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

OLD = Path("/home/irteam/junah-data-1/2_ClinSevBench/ClinSevBench_v2")

BENIGN = ["benign_format", "benign_sentence_order", "benign_paraphrase_rule"]
CHANGED = [
    "negation_flip", "laterality_flip", "finding_deletion", "false_finding_insertion",
    "measurement_flip", "severity_flip", "uncertainty_flip", "anatomy_region_flip",
    "temporal_comparison_flip",
]
PAPER_METRICS = ["green", "ratescore", "radgraph", "temporal", "f1chexbert", "bertscore"]

# ---------------------------------------------------------------------------
# copied from clinsev_pipeline.py (ARR-May)
# ---------------------------------------------------------------------------
TOKEN_RE = re.compile(r"\b\w+\b")
NEGATION_PAT = re.compile(r"\b(no|without|negative for|no evidence of|absent|not)\b", flags=re.I)


def clean_text(text: str) -> str:
    text = str(text or "").replace("\r", "\n")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    return text.strip()


def split_sentences(text: str):
    parts = re.split(r"(?<=[.!?])\s+", clean_text(text))
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) <= 1:
        parts = [p.strip() for p in re.split(r"\s*;\s*", clean_text(text)) if p.strip()]
    return parts


def norm(text):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\. ]+", " ", str(text or "").lower())).strip()


def toks(text):
    return TOKEN_RE.findall(norm(text))


def token_f1(ref, hyp):
    r, h = Counter(toks(ref)), Counter(toks(hyp))
    if not r and not h:
        return 1.0
    if not r or not h:
        return 0.0
    inter = sum((r & h).values())
    if inter == 0:
        return 0.0
    p, rec = inter / sum(h.values()), inter / sum(r.values())
    return 2 * p * rec / (p + rec)


def jaccard(ref, hyp):
    r, h = set(toks(ref)), set(toks(hyp))
    return 1.0 if not r and not h else (0.0 if not r or not h else len(r & h) / len(r | h))


# ---------------------------------------------------------------------------
# new helpers
# ---------------------------------------------------------------------------
def ws_tokens(text):
    return str(text).split()


def token_edit_ops(ref, hyp):
    """Number of whitespace tokens inserted/deleted/replaced (difflib opcodes)."""
    a, b = ws_tokens(ref), ws_tokens(hyp)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    n = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            n += max(i2 - i1, j2 - j1)
    return n


def seq_ratio(ref, hyp):
    """Order-sensitive token similarity (difflib ratio)."""
    return difflib.SequenceMatcher(a=ws_tokens(ref), b=ws_tokens(hyp), autojunk=False).ratio()


def safe_auc(y, s):
    y = np.asarray(y)
    s = np.asarray(s, dtype=float)
    ok = np.isfinite(s)
    y, s = y[ok], s[ok]
    if len(np.unique(y)) < 2:
        return np.nan
    return float(roc_auc_score(y, s))


def cluster_bootstrap_auc(df, ycol, scol, cluster="report_id", n_boot=1000, seed=0):
    rng = np.random.default_rng(seed)
    groups = {k: g[[ycol, scol]].to_numpy() for k, g in df.groupby(cluster)}
    keys = list(groups)
    vals = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(keys), size=len(keys))
        arr = np.concatenate([groups[keys[i]] for i in pick])
        if len(np.unique(arr[:, 0])) < 2:
            continue
        vals.append(roc_auc_score(arr[:, 0], arr[:, 1]))
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def md_table(df, floatfmt=3):
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.{floatfmt}f}")
    cols = [str(c) for c in d.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in d.iterrows():
        lines.append("| " + " | ".join(str(v) for v in r.tolist()) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# A + B
# ---------------------------------------------------------------------------
def load_subset200(section):
    p = OLD / f"results/analysis/radeval_{section}_clean_subset200_broad/scored_with_drops.csv"
    df = pd.read_csv(p)
    cand = df[df.perturbation_type != "identity"].copy()
    cand["is_changed"] = (~cand.perturbation_type.isin(BENIGN)).astype(int)
    # trivial baselines; identity score is 1.0 for all of them by construction
    cand["token_f1__drop"] = [1 - token_f1(r, c) for r, c in zip(cand.reference, cand.candidate)]
    cand["jaccard__drop"] = [1 - jaccard(r, c) for r, c in zip(cand.reference, cand.candidate)]
    cand["seqratio__drop"] = [1 - seq_ratio(r, c) for r, c in zip(cand.reference, cand.candidate)]
    cand["edit_tokens"] = [token_edit_ops(r, c) for r, c in zip(cand.reference, cand.candidate)]
    cand["ref_len"] = cand.reference.map(lambda x: len(ws_tokens(x)))
    cand["len_diff"] = cand.candidate.map(lambda x: len(ws_tokens(x))) - cand.ref_len
    # "bag changed?" = does the multiset of alphanumeric tokens differ at all
    cand["bow_changed__drop"] = (cand["token_f1__drop"] > 1e-12).astype(float)
    # negative edit size: "smaller edit => more likely meaning-changing"
    cand["neg_edit_tokens__drop"] = -cand["edit_tokens"].astype(float)
    return cand


def audit_A_B(out_dir, n_boot):
    all_metrics = PAPER_METRICS + ["token_f1", "jaccard", "seqratio", "bow_changed", "neg_edit_tokens"]
    pooled_rows, pertype_rows, matrix_rows, edit_rows, corr_rows = [], [], [], [], []
    for section in ["impression", "findings"]:
        cand = load_subset200(section)
        cand.to_csv(out_dir / f"A_subset200_{section}_with_trivial_baselines.csv", index=False)
        for m in all_metrics:
            col = f"{m}__drop"
            sub = cand.dropna(subset=[col])
            auc = safe_auc(sub.is_changed, sub[col])
            lo, hi = cluster_bootstrap_auc(sub, "is_changed", col, n_boot=n_boot)
            pooled_rows.append({"section": section, "metric": m, "n": len(sub), "auroc": auc,
                                "cluster_ci_low": lo, "cluster_ci_high": hi})
            ben = sub[sub.is_changed == 0]
            for t in CHANGED:
                ch = sub[sub.perturbation_type == t]
                both = pd.concat([ben, ch])
                pertype_rows.append({"section": section, "metric": m, "changed_type": t,
                                     "auroc_vs_pooled_benign": safe_auc(both.is_changed, both[col])})
                for b in BENIGN:
                    bb = pd.concat([sub[sub.perturbation_type == b], ch])
                    matrix_rows.append({"section": section, "metric": m, "changed_type": t, "benign_type": b,
                                        "auroc": safe_auc(bb.is_changed, bb[col])})
            # pooled changed vs each single benign type
            for b in BENIGN:
                bb = pd.concat([sub[sub.perturbation_type == b], sub[sub.is_changed == 1]])
                matrix_rows.append({"section": section, "metric": m, "changed_type": "ALL_CHANGED",
                                    "benign_type": b, "auroc": safe_auc(bb.is_changed, bb[col])})
            if m in PAPER_METRICS:
                s = sub[[col, "edit_tokens"]].corr(method="spearman").iloc[0, 1]
                corr_rows.append({"section": section, "metric": m, "spearman_penalty_vs_edit_tokens": s})
        g = cand.groupby("perturbation_type").agg(
            n=("edit_tokens", "size"),
            edit_tokens_mean=("edit_tokens", "mean"),
            edit_tokens_median=("edit_tokens", "median"),
            len_diff_mean=("len_diff", "mean"),
            ref_len_mean=("ref_len", "mean"),
            token_f1_drop_mean=("token_f1__drop", "mean"),
            bow_unchanged_rate=("bow_changed__drop", lambda x: float((x == 0).mean())),
        ).reset_index()
        g.insert(0, "section", section)
        edit_rows.append(g)

    pooled = pd.DataFrame(pooled_rows)
    pertype = pd.DataFrame(pertype_rows)
    matrix = pd.DataFrame(matrix_rows)
    edits = pd.concat(edit_rows, ignore_index=True)
    corr = pd.DataFrame(corr_rows)
    pooled.to_csv(out_dir / "A_pooled_auroc_with_trivial_baselines.csv", index=False)
    pertype.to_csv(out_dir / "A_per_type_auroc_with_trivial_baselines.csv", index=False)
    matrix.to_csv(out_dir / "B_changed_x_benign_auroc_matrix.csv", index=False)
    edits.to_csv(out_dir / "B_edit_magnitude_by_type.csv", index=False)
    corr.to_csv(out_dir / "B_penalty_vs_edit_size_spearman.csv", index=False)
    return pooled, pertype, matrix, edits, corr


# ---------------------------------------------------------------------------
# C. rule quality heuristics on the full clean 5k pair sets
# ---------------------------------------------------------------------------
def audit_C(out_dir):
    rows, examples = [], []
    for section in ["impression", "findings"]:
        df = pd.read_csv(OLD / f"data/minpairs/pairs_{section}_5000_seed0_clean.csv")
        sub200 = pd.read_csv(OLD / f"data/minpairs/pairs_{section}_clean_metric_subset_200.csv")
        for name, d in [("full_clean_5k", df), ("subset200", sub200)]:
            def add(ptype, flag_name, mask, base):
                n = int(len(base))
                k = int(mask.sum())
                rows.append({"section": section, "split": name, "perturbation_type": ptype,
                             "issue": flag_name, "n_type": n, "n_flagged": k,
                             "rate": k / n if n else np.nan})
                if name == "subset200" and k:
                    ex = base[mask].head(3)
                    for _, r in ex.iterrows():
                        examples.append({"section": section, "perturbation_type": ptype, "issue": flag_name,
                                         "edit_detail": r.edit_detail,
                                         "reference": r.reference[:400], "candidate": r.candidate[:400]})

            ident = d[d.perturbation_type == "identity"]
            # reference-level issues
            sents = ident.reference.map(split_sentences)
            dup = sents.map(lambda s: len(s) >= 2 and len(set(x.lower() for x in s)) < len(s))
            add("identity", "reference_has_duplicated_sentence", dup, ident)
            add("identity", "reference_has_numbered_list", ident.reference.str.contains(r"(?:^|\s)\d\.\s", regex=True), ident)
            add("identity", "reference_has_abbrev_split_risk(Dr./a.m./p.m.)",
                ident.reference.str.contains(r"\bDr\.|\b[ap]\.m\.", regex=True), ident)
            add("identity", "reference_word_count<=5", ident.reference.map(lambda x: len(ws_tokens(x)) <= 5), ident)

            g = d[d.perturbation_type == "negation_flip"]
            add("negation_flip", "direction=present->negated(insert 'no')", g.edit_detail.str.startswith("present->"), g)
            add("negation_flip", "direction=negated->present", g.edit_detail.str.startswith("negated->"), g)
            ins = g[g.edit_detail.str.startswith("present->")]
            # inserted "no X" is preceded by a modifier/determiner/conjunction -> ungrammatical noun phrase
            def bad_no(r):
                f = re.sub(r"^present->|_negated$", "", r.edit_detail)
                m = re.search(r"(\S+)\s+no\s+" + re.escape(f), r.candidate, flags=re.I)
                if not m:
                    return False
                prev = m.group(1).lower().strip(",.;:")
                return prev not in {"", "is", "are", "with", "shows", "show", "demonstrates", "and"} and not prev.endswith(".")
            add("negation_flip", "inserted 'no' lands mid-phrase (e.g. 'left no pleural effusion')",
                ins.apply(bad_no, axis=1) if len(ins) else pd.Series([], dtype=bool), ins)
            def neg_elsewhere(r):
                f = re.sub(r"^present->|_negated$", "", r.edit_detail)
                for s in split_sentences(r.reference):
                    if re.search(r"\b" + re.escape(f) + r"\b", s, flags=re.I):
                        return NEGATION_PAT.search(s) is not None
                return False
            add("negation_flip", "'present' finding sits in a sentence that already has a negation cue",
                ins.apply(neg_elsewhere, axis=1) if len(ins) else pd.Series([], dtype=bool), ins)
            neg2pos = g[g.edit_detail.str.startswith("negated->")]
            add("negation_flip", "negated->present leaves coordinated remainder ('X is present or Y')",
                neg2pos.candidate.str.contains(r"is present\s+(?:or|and|,)", regex=True, flags=re.I), neg2pos)

            g = d[d.perturbation_type == "laterality_flip"]
            add("laterality_flip", "source=bilateral (paper says bilateral is skipped)", g.edit_detail.str.startswith("bilateral"), g)
            add("laterality_flip", "reference mentions BOTH left and right (first-match flip may create contradiction)",
                g.reference.str.contains(r"\bleft\b", flags=re.I, regex=True) & g.reference.str.contains(r"\bright\b", flags=re.I, regex=True), g)
            add("laterality_flip", "flipped token is non-anatomical candidate ('right heart', 'left in place', 'right IJ/PICC' device)",
                g.apply(lambda r: bool(re.search(r"\b(?:left|right)\s+(?:heart|atri|ventric|IJ|internal jugular|subclavian|PICC|picc|chest tube|pigtail|port|pacemaker|pacer|sided)", r.reference, flags=re.I)), axis=1), g)

            g = d[d.perturbation_type == "measurement_flip"]
            add("measurement_flip", "unit swap only (cm<->mm); numeric value never edited",
                g.edit_detail.str.contains(r"cm->.*mm|mm->.*cm", regex=True), g)

            g = d[d.perturbation_type == "uncertainty_flip"]
            add("uncertainty_flip", "direction=asserted->possible (insert 'possible')", g.edit_detail.str.startswith("asserted->"), g)
            add("uncertainty_flip", "direction=hedged->definite", ~g.edit_detail.str.startswith("asserted->"), g)

            g = d[d.perturbation_type == "benign_format"]
            add("benign_format", "prefix 'Report impression:' (single-sentence refs; also used for FINDINGS section)",
                g.candidate.str.startswith("Report impression:"), g)
            add("benign_format", "bullets break numbered list ('- 1. - ...')",
                g.candidate.str.contains(r"-\s\d\s?\.\s-", regex=True), g)

            g = d[d.perturbation_type == "benign_sentence_order"]
            add("benign_sentence_order", "reference has discourse connective (However/Otherwise/This/These/Also ...) -> order-dependent",
                g.reference.str.contains(r"(?:^|\.\s)(?:However|Otherwise|This|These|It|Again|Also|Additionally|Alternatively|In addition|Given)\b", regex=True), g)
            add("benign_sentence_order", "reference has numbered list", g.reference.str.contains(r"(?:^|\s)\d\.\s", regex=True), g)

            g = d[d.perturbation_type == "finding_deletion"]
            add("finding_deletion", "whole section replaced by 'No acute cardiopulmonary abnormality.'",
                g.candidate.str.strip().eq("No acute cardiopulmonary abnormality."), g)

            g = d[d.perturbation_type == "false_finding_insertion"]
            add("false_finding_insertion", "reference lacks terminal period before appended sentence",
                g.reference.map(lambda x: not str(x).rstrip().endswith((".", "!", "?"))), g)
            add("false_finding_insertion", "inserted sentence carries laterality/severity/size (multi-factor, not minimal)",
                pd.Series(True, index=g.index), g)

            g = d[d.perturbation_type == "temporal_comparison_flip"]
            add("temporal_comparison_flip", "detail=stable/unchanged->increased", g.edit_detail.str.contains(r"^(?:stable|unchanged)->", regex=True), g)
            add("temporal_comparison_flip", "flipped word describes device/position ('tube|catheter|line|lead ... unchanged')",
                g.reference.str.contains(r"(?:tube|catheter|line|lead|leads|device|devices|position|wires|hardware)[^.]{0,60}\b(?:unchanged|stable)\b", regex=True, flags=re.I)
                & g.edit_detail.str.contains(r"^(?:stable|unchanged)->", regex=True), g)

            g = d[d.perturbation_type == "severity_flip"]
            add("severity_flip", "polarity flip (small/trace/mild/minimal <-> large/severe), not an adjacent grade",
                g.edit_detail.isin(["small->large", "trace->large", "mild->severe", "minimal->severe", "severe->mild", "large->small", "marked->mild"]), g)

    out = pd.DataFrame(rows)
    out.to_csv(out_dir / "C_rule_quality_heuristics.csv", index=False)
    pd.DataFrame(examples).to_csv(out_dir / "C_rule_quality_examples.csv", index=False)
    return out, pd.DataFrame(examples)


# ---------------------------------------------------------------------------
# D. section provenance
# ---------------------------------------------------------------------------
def audit_D(out_dir):
    rep = pd.read_csv(OLD / "data/processed/reports_mimic_txt_dir.csv")
    rep["has_impression_header"] = rep.text.str.contains(r"\bIMPRESSION\s*:", regex=True, flags=re.I)
    rep["has_findings_header"] = rep.text.str.contains(r"\bFINDINGS\s*:", regex=True, flags=re.I)
    rep["findings_eq_impression"] = rep.findings.fillna("") == rep.impression.fillna("")
    rep["impression_eq_fulltext"] = rep.impression.fillna("") == rep.text.fillna("")
    rows = [{
        "scope": "all_prepared_reports", "n": len(rep),
        "has_IMPRESSION_header": rep.has_impression_header.mean(),
        "has_FINDINGS_header": rep.has_findings_header.mean(),
        "has_both_headers": (rep.has_impression_header & rep.has_findings_header).mean(),
        "findings_text==impression_text": rep.findings_eq_impression.mean(),
        "impression_text==full_text": rep.impression_eq_fulltext.mean(),
    }]
    key = rep.set_index("report_id")
    overlap_rows = []
    for split in ["5000_seed0_clean", "clean_metric_subset_200"]:
        ids = {}
        for section in ["impression", "findings"]:
            p = OLD / f"data/minpairs/pairs_{section}_{split}.csv"
            d = pd.read_csv(p)
            ident = d[d.perturbation_type == "identity"].drop_duplicates("report_id")
            ids[section] = ident
            k = key.loc[ident.report_id]
            hdr = "has_impression_header" if section == "impression" else "has_findings_header"
            rows.append({
                "scope": f"{section}:{split}", "n": len(ident),
                "has_IMPRESSION_header": k.has_impression_header.mean(),
                "has_FINDINGS_header": k.has_findings_header.mean(),
                "has_both_headers": (k.has_impression_header & k.has_findings_header).mean(),
                "findings_text==impression_text": k.findings_eq_impression.mean(),
                "impression_text==full_text": k.impression_eq_fulltext.mean(),
                "reference_is_true_section(header present & sections differ)":
                    float((k[hdr] & ~k.findings_eq_impression).mean()),
            })
        a, b = ids["impression"], ids["findings"]
        common = set(a.report_id) & set(b.report_id)
        ma = a.set_index("report_id").reference
        mb = b.set_index("report_id").reference
        same = sum(ma[i] == mb[i] for i in common)
        overlap_rows.append({"split": split, "n_impression_reports": len(a), "n_findings_reports": len(b),
                             "reports_in_both": len(common), "identical_reference_text_in_both": int(same),
                             "identical_reference_any_report": len(set(ma.values) & set(mb.values))})
    out = pd.DataFrame(rows)
    ov = pd.DataFrame(overlap_rows)
    out.to_csv(out_dir / "D_section_provenance.csv", index=False)
    ov.to_csv(out_dir / "D_impression_findings_overlap.csv", index=False)
    return out, ov


# ---------------------------------------------------------------------------
# E. human annotation structure
# ---------------------------------------------------------------------------
def audit_E(out_dir):
    L = pd.read_csv(OLD / "results/meaning_annotation_480_filled/all_annotations_long.csv")
    I = pd.read_csv(OLD / "results/meaning_annotation_480_filled/annotations_item_level.csv")
    L["match_rule"] = L.meaning_preserved_norm == L.rule_meaning_preserved
    I["match_rule"] = I.human_meaning_preserved == I.rule_meaning_preserved
    per_ann = L.groupby("annotator").agg(
        n=("match_rule", "size"), match_rule=("match_rule", "mean"),
        yes=("meaning_preserved_norm", lambda x: (x == "yes").mean()),
        no=("meaning_preserved_norm", lambda x: (x == "no").mean()),
        uncertain=("meaning_preserved_norm", lambda x: (x == "uncertain").mean()),
        comment_rate=("comments", lambda x: x.notna().mean()),
    ).reset_index()
    by_n = I.groupby("n_labels").agg(
        n_items=("match_rule", "size"),
        match_rule_incl_uncertain=("match_rule", "mean"),
        uncertain_rate=("human_meaning_preserved", lambda x: (x == "uncertain").mean()),
    ).reset_index()
    ann_type = L.groupby(["perturbation_type", "annotator"]).match_rule.mean().unstack().reset_index()
    single = I[I.n_labels == 1]
    single_by_type = single.groupby("perturbation_type").match_rule.agg(["size", "mean"]).reset_index()
    per_ann.to_csv(out_dir / "E_per_annotator.csv", index=False)
    by_n.to_csv(out_dir / "E_single_vs_triple.csv", index=False)
    ann_type.to_csv(out_dir / "E_annotator_x_type_match.csv", index=False)
    single_by_type.to_csv(out_dir / "E_single_annotated_by_type.csv", index=False)
    top_comments = L.comments.dropna().value_counts().head(30).reset_index()
    top_comments.columns = ["comment", "count"]
    top_comments.to_csv(out_dir / "E_top_comments.csv", index=False)
    return per_ann, by_n, ann_type, single_by_type, top_comments


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", default="/home/irteam/junah-data-1/ARR_10/2_ClimSemBench/results/0_audit")
    ap.add_argument("--n_boot", type=int, default=1000)
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 40)
    pd.set_option("display.max_colwidth", 120)

    report = ["# 0_audit — automatic audit of the ARR-May experiment\n"]

    pooled, pertype, matrix, edits, corr = audit_A_B(out_dir, args.n_boot)
    report += ["## A. Pooled AUROC incl. trivial baselines (subset200, same rows as paper Table 3)\n",
               md_table(pooled.pivot(index="metric", columns="section", values="auroc")
                        .sort_values("impression", ascending=False).reset_index()), "",
               "### cluster(report)-bootstrap 95% CI\n", md_table(pooled), ""]
    wide = pertype.assign(v=pertype.auroc_vs_pooled_benign).pivot_table(
        index=["section", "changed_type"], columns="metric", values="v").reset_index()
    report += ["## A2. Per-type AUROC (changed type vs pooled benign)\n", md_table(wide), ""]
    mm = matrix[matrix.changed_type == "ALL_CHANGED"].pivot_table(
        index=["section", "metric"], columns="benign_type", values="auroc").reset_index()
    report += ["## B. AUROC of ALL changed vs. each single benign type\n", md_table(mm), "",
               "## B2. Edit magnitude by perturbation type\n", md_table(edits, 2), "",
               "## B3. Spearman(metric penalty, #edited tokens)\n", md_table(corr), ""]

    qual, ex = audit_C(out_dir)
    report += ["## C. Rule-quality heuristics\n", md_table(qual), ""]

    prov, ov = audit_D(out_dir)
    report += ["## D. Section provenance\n", md_table(prov), "", md_table(ov), ""]

    per_ann, by_n, ann_type, single_by_type, top_comments = audit_E(out_dir)
    report += ["## E. Human annotation structure\n", md_table(per_ann), "", md_table(by_n), "",
               md_table(ann_type, 2), "", md_table(single_by_type), "", md_table(top_comments), ""]

    (out_dir / "AUDIT_REPORT.md").write_text("\n".join(report))
    print("\n".join(report))
    print("[wrote]", out_dir / "AUDIT_REPORT.md")


if __name__ == "__main__":
    main()
