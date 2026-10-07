#!/usr/bin/env python
"""
20_make_paper_tables.py — every number in the paper comes from here (LaTeX tables + a macro file of inline numbers).

Reads results/2_full_*/{analysis,extended}, results/3_x3_audit, data/pairs/*targets.csv
Writes docs/paper/tables/*.tex and docs/paper/tables/numbers.tex (\\newcommand macros used in the running text).
Run: /opt/conda/envs/clinsev/bin/python scripts/20_make_paper_tables.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

NEW = Path(__file__).resolve().parent.parent
OUT = NEW / "docs/paper/tables"
OUT.mkdir(parents=True, exist_ok=True)
R = NEW / "results"

NAMES = {
    "jaccard": "Jaccard", "token_f1": "Token F1", "bleu": "BLEU", "rougeL": "ROUGE-L",
    "bertscore_distilbert": "BERTScore (DistilBERT)", "bertscore_roberta_large": "BERTScore (RoBERTa-L)",
    "bertscore_deberta_mnli": "BERTScore (DeBERTa-MNLI)", "f1chexbert": "F1CheXbert", "temporal": "Temporal F1",
    "srrbert": "SRR-BERT", "radgraph": "RadGraph F1", "ratescore": "RaTEScore", "radcliq": "RadCliQ-v1",
    "green": "GREEN", "crimson": "CRIMSON",
    "llama31_8b__rubric": "Llama-3.1-8B", "gemma3_27b__rubric": "Gemma-3-27B", "qwen3_32b__rubric": "Qwen3-32B",
    "qwen3_32b_think__rubric": "Qwen3-32B (thinking)", "gptoss_20b__rubric": "gpt-oss-20b", "gptoss_120b__rubric": "gpt-oss-120b",
}
GROUPS = [("Meaning-blind baselines", ["jaccard", "token_f1"]),
          ("Lexical / embedding", ["bleu", "rougeL", "bertscore_distilbert", "bertscore_roberta_large", "bertscore_deberta_mnli"]),
          ("Clinical, non-LLM", ["f1chexbert", "temporal", "srrbert", "radgraph", "ratescore", "radcliq"]),
          ("LLM-based metrics", ["green", "crimson"]),
          ("LLM judges (rubric prompt)", ["llama31_8b__rubric", "gemma3_27b__rubric", "qwen3_32b__rubric", "qwen3_32b_think__rubric", "gptoss_20b__rubric", "gptoss_120b__rubric"])]
for _t, _n in [("llama31_8b", "Llama-3.1-8B"), ("gemma3_27b", "Gemma-3-27B"), ("qwen3_32b", "Qwen3-32B"), ("gptoss_20b", "gpt-oss-20b"), ("gptoss_120b", "gpt-oss-120b")]:
    NAMES[f"{_t}__errors"] = _n
    NAMES[f"{_t}__rubric_unit"] = _n
ERR_GROUP = ("LLM judges (errors prompt)", ["gemma3_27b__errors", "qwen3_32b__errors", "gptoss_20b__errors", "gptoss_120b__errors"])
TYPES = ["anatomy", "laterality", "measurement", "negation", "severity", "temporal", "uncertainty"]
macros = {}


def f2(v, d=2):
    return "--" if v is None or pd.isna(v) else f"{v:.{d}f}"


def summ(c):
    return pd.read_csv(R / f"2_full_{c}/analysis/summary_by_condition.csv")


def write(name, body):
    (OUT / name).write_text(body)
    print("[wrote]", name)


# ------------------------------------------------------------------ Table: surface-only predictability (X3 + floor)
def tab_surface():
    t = pd.read_csv(R / "3_x3_audit/table3.csv")
    rows = []
    lab = {"ClinSemBench v1 (impression, rule labels)": r"ClinSemBench-v1, \textit{Impression} (rule labels)",
           "ClinSemBench v1 (findings, rule labels)": r"ClinSemBench-v1, \textit{Findings} (rule labels)",
           "ClinSemBench v1 (480-pair set, human labels)": "ClinSemBench-v1, validation set (human labels)"}
    for r in t.itertuples():
        if r.benchmark in lab:
            rows.append(f"{lab[r.benchmark]} & {r.n:,} & {f2(r.surface_only_LR_auroc, 2)} & {f2(r.jaccard_drop_auroc, 2)} & {f2(r.edit_tokens_auroc, 2)} \\\\")
    rt = R / "3_x3_audit/rate_eval_task3.csv"
    if rt.exists():                                      # public suite (10/7 review, point 1): scripts/22
        r3 = pd.read_csv(rt).set_index("subset").loc["confident alignment"]
        rows.append(f"RaTE-Eval, synthetic task (synonym vs.\\ opposite)$^{{\\dagger}}$ & {2*int(r3.n_triplets):,} & {f2(r3.surface_only_LR_auroc, 2)} & {f2(r3.auc_jaccard_drop, 2)} & {f2(r3.auc_edit_tokens, 2)} \\\\")
    rows.append(r"\midrule")
    # ours: one row per comparison, IU / MIMIC side by side (compact; 10/7)
    for key, nm in [("confound v1-type (C0 vs P1)", r"\textsc{Conf-R}: C0 vs.\ P1"), ("confound ReEvalMed-type (C0 vs P2)", r"\textsc{Conf-P}: C0 vs.\ P2"),
                    ("controlled S0 (C0 vs P0)", r"\textsc{Ctrl-0}: C0 vs.\ P0"), ("controlled S2 (C2 vs P2)", r"\textsc{Ctrl-2}: C2 vs.\ P2")]:
        rr = [t[t.benchmark == f"factorial {corp} — {key}"].iloc[0] for corp in ["IU", "MIMIC"]]
        rows.append(f"Ours, {nm} & " + "/".join(f"{r.n:,}" for r in rr) + " & " + "/".join(f2(r.surface_only_LR_auroc, 2) for r in rr) + " & "
                    + "/".join(f2(r.jaccard_drop_auroc, 2) for r in rr) + " & " + "/".join(f2(r.edit_tokens_auroc, 2) for r in rr) + r" \\")
        for corp, r in zip(["IU", "MIMIC"], rr):
            macros[f"floor{corp}{key.split()[0][:4]}{key.split('(')[1][:2]}{key.split('vs ')[1][:2]}".replace(" ", "")] = f2(r.surface_only_LR_auroc, 2)
    for k, v in [("vOneImp", "ClinSemBench v1 (impression, rule labels)"), ("vOneFind", "ClinSemBench v1 (findings, rule labels)"), ("vOneHuman", "ClinSemBench v1 (480-pair set, human labels)")]:
        macros["floor" + k] = f2(t[t.benchmark == v].surface_only_LR_auroc.iloc[0], 2)
    body = r"""\begin{tabular}{lrccc}
\toprule
\textbf{Benchmark / comparison} & \textbf{$n$} & \textbf{Surface-only} & \textbf{Jaccard} & \textbf{\#Edit tok.} \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}"""
    write("tab_surface.tex", body)


# ------------------------------------------------------------------ Table: main (confounded vs controlled)
def tab_main():
    S = {c: summ(c) for c in ["iu", "mimic"]}
    C = {c: pd.read_csv(R / f"2_full_{c}/extended/C_contrasts.csv").set_index("metric") for c in ["iu", "mimic"]}
    W = {c: pd.read_csv(R / f"2_full_{c}/review1007/A_win_tie_loss.csv") for c in ["iu", "mimic"]}          # scripts/21
    W = {c: W[c][W[c].condition == "Ctrl-0"].set_index("metric") for c in W}
    B = {c: pd.read_csv(R / f"2_full_{c}/review1007/B_strict_matched.csv").set_index("metric") for c in ["iu", "mimic"]}
    lines, unmarked_not_above = [], []
    for g, ms in GROUPS:
        lines.append(rf"\multicolumn{{13}}{{l}}{{\textit{{{g}}}}} \\")
        for m in ms:
            cells = []
            for c in ["iu", "mimic"]:
                s = S[c][S[c].metric == m].set_index("condition")
                if s.empty:
                    cells += ["--"] * 6
                    continue
                for cond in ["confound_v1", "confound_reevalmed", "controlled_S0", "controlled_S2"]:
                    v = f2(s.loc[cond, "paired_acc"])
                    if cond == "controlled_S0" and m in C[c].index and m not in ("jaccard",):
                        if C[c].loc[m, "vsJ_hi"] < 0:
                            v += r"$^{\downarrow}$"
                        elif C[c].loc[m, "vsJ_lo"] <= 0:
                            v += r"$^{\circ}$"
                    if cond == "controlled_S0" and m != "jaccard" and (m not in C[c].index or not C[c].loc[m, "vsJ_lo"] > 0) and "downarrow" not in v and "circ" not in v:
                        unmarked_not_above.append((c, m))
                    if cond == "controlled_S2" and m in C[c].index and C[c].loc[m, "drop_lo"] > 0:
                        v += r"$^{\ast}$"
                    cells.append(v)
                    macros[f"pa{c}{cond.replace('_','')}{m.replace('_','')}".replace("0", "zero").replace("1", "one").replace("2", "two").replace("3", "three").replace("8", "eight").replace("7", "seven")] = f2(s.loc[cond, "paired_acc"])
                cells.append(f2(W[c].loc[m, "tie"]) if m in W[c].index else "--")
                cells.append(f2(B[c].loc[m, "Ctrl-0 strict"]) if m in B[c].index else "--")
            lines.append(f"{NAMES[m]} & " + " & ".join(cells) + r" \\")
        lines.append(r"\addlinespace[2pt]")
    print("  [check] Ctrl-0 cells without a marker that are NOT significantly above Jaccard:", unmarked_not_above)
    ns = {c: int(B[c].n_strict.iloc[0]) for c in B}
    macros["nstrictiu"], macros["nstrictmimic"] = str(ns["iu"]), str(ns["mimic"])
    body = r"""\begin{tabular}{lcccccccccccc}
\toprule
 & \multicolumn{6}{c}{\textbf{IU X-Ray} ($n{=}890$)} & \multicolumn{6}{c}{\textbf{MIMIC-CXR} ($n{=}1{,}050$)} \\
\cmidrule(lr){2-7}\cmidrule(lr){8-13}
 & \multicolumn{2}{c}{Confounded} & \multicolumn{2}{c}{Controlled} & \multicolumn{2}{c}{\textsc{Ctrl-0} detail} & \multicolumn{2}{c}{Confounded} & \multicolumn{2}{c}{Controlled} & \multicolumn{2}{c}{\textsc{Ctrl-0} detail} \\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(lr){8-9}\cmidrule(lr){10-11}\cmidrule(lr){12-13}
\textbf{Metric} & \textsc{R} & \textsc{P} & \textsc{0} & \textsc{2} & tie & strict & \textsc{R} & \textsc{P} & \textsc{0} & \textsc{2} & tie & strict \\
\midrule
""" + "\n".join(lines[:-1]) + r"""
\bottomrule
\end{tabular}"""
    write("tab_main.tex", body)


# ------------------------------------------------------------------ Table: judges per cell
def tab_judges():
    J = {c: pd.read_csv(R / f"2_full_{c}/analysis/judge_cells.csv") for c in ["iu", "mimic"]}
    lines = []
    for m in GROUPS[-1][1]:
        cells = []
        for c in ["iu", "mimic"]:
            j = J[c][J[c].judge == m].set_index("cell")
            cells += [f2(j.loc[x, "rate_changed"]) if x in j.index else "--" for x in ["P0", "P1", "P2", "C0", "C1", "C2"]]
        lines.append(f"{NAMES[m]} & " + " & ".join(cells) + r" \\")
    body = r"""\begin{tabular}{lcccccccccccc}
\toprule
 & \multicolumn{6}{c}{\textbf{IU X-Ray}} & \multicolumn{6}{c}{\textbf{MIMIC-CXR}} \\
\cmidrule(lr){2-7}\cmidrule(lr){8-13}
 & \multicolumn{3}{c}{False alarms $\downarrow$} & \multicolumn{3}{c}{Detections $\uparrow$} & \multicolumn{3}{c}{False alarms $\downarrow$} & \multicolumn{3}{c}{Detections $\uparrow$} \\
\cmidrule(lr){2-4}\cmidrule(lr){5-7}\cmidrule(lr){8-10}\cmidrule(lr){11-13}
\textbf{Judge} & P0 & P1 & P2 & C0 & C1 & C2 & P0 & P1 & P2 & C0 & C1 & C2 \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}"""
    write("tab_judges.tex", body)
    # by-type failures
    T = {c: pd.read_csv(R / f"2_full_{c}/analysis/judge_cells_by_type.csv") for c in ["iu", "mimic"]}
    lines = []
    for m in GROUPS[-1][1]:
        cells = []
        for c in ["iu", "mimic"]:
            t = T[c][T[c].judge == m]
            for cell, et in [("P0", "measurement"), ("P0", "severity"), ("C2", "uncertainty"), ("C2", "laterality")]:
                v = t[(t.cell == cell) & (t.edit_type == et)].rate_changed
                cells.append(f2(v.iloc[0]) if len(v) else "--")
        lines.append(f"{NAMES[m]} & " + " & ".join(cells) + r" \\")
    body = r"""\begin{tabular}{lcccccccc}
\toprule
 & \multicolumn{4}{c}{\textbf{IU X-Ray}} & \multicolumn{4}{c}{\textbf{MIMIC-CXR}} \\
\cmidrule(lr){2-5}\cmidrule(lr){6-9}
 & \multicolumn{2}{c}{P0 false alarm $\downarrow$} & \multicolumn{2}{c}{C2 detection $\uparrow$} & \multicolumn{2}{c}{P0 false alarm $\downarrow$} & \multicolumn{2}{c}{C2 detection $\uparrow$} \\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(lr){8-9}
\textbf{Judge} & Meas. & Sev. & Unc. & Lat. & Meas. & Sev. & Unc. & Lat. \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}"""
    write("tab_judges_types.tex", body)


# ------------------------------------------------------------------ Table: monotonicity
MONO_MAIN = ["jaccard", "bleu", "bertscore_distilbert", "bertscore_deberta_mnli", "radgraph", "radcliq", "green", "crimson",
             "gptoss_20b__rubric", "gptoss_120b__rubric", "gptoss_20b__errors", "gptoss_120b__errors"]


def tab_mono():
    m = pd.read_csv(R / "2_full_mimicmono/analysis/monotonicity.csv").set_index("metric")
    for fname, keep in [("tab_mono.tex", None), ("tab_mono_main.tex", MONO_MAIN)]:      # full table (appendix) and compact table (main text)
        lines = []
        for g, ms in GROUPS + [ERR_GROUP]:
            ms = [x for x in ms if x in m.index and (keep is None or x in keep)]
            if not ms:
                continue
            lines.append(rf"\multicolumn{{8}}{{l}}{{\textit{{{g}}}}} \\")
            for x in ms:
                r = m.loc[x]
                lines.append(f"{NAMES[x]} & {f2(r['kendall_tau'])} & {f2(r['step_M1>M0'])} & {f2(r['step_M2>M1'])} & {f2(r['step_M3>M2'])} & "
                             f"{f2(r['uncontrolled_K2>K1'])} & {f2(r['uncontrolled_M3>K2'])} & {f2(r['benign_over_error_M0>K1'])} \\\\")
                macros["tau" + x.replace("_", "").replace("0", "zero").replace("1", "one").replace("2", "two").replace("3", "three").replace("8", "eight").replace("7", "seven")] = f2(r["kendall_tau"])
            if keep is None:
                lines.append(r"\addlinespace[2pt]")
        body = r"""\begin{tabular}{lccccccc}
\toprule
 & \multicolumn{4}{c}{\textbf{Fixed-surface ladder}} & \multicolumn{2}{c}{\textbf{Growing-surface ladder}} & \textbf{3 benign} \\
\cmidrule(lr){2-5}\cmidrule(lr){6-7}
\textbf{Metric} & $\tau$ & $0{\to}1$ & $1{\to}2$ & $2{\to}3$ & $1{\to}2$ & $2{\to}3$ & \textbf{$>$ 1 error} \\
\midrule
""" + "\n".join(lines[:-1] if keep is None else lines) + r"""
\bottomrule
\end{tabular}"""
        write(fname, body)


# ------------------------------------------------------------------ Appendix: per-type controlled S0
def tab_types():
    for c in ["iu", "mimic"]:
        p = pd.read_csv(R / f"2_full_{c}/analysis/per_type.csv")
        p = p[p.condition == "controlled_S0"].pivot(index="metric", columns="edit_type", values="paired_acc")
        lines = []
        for g, ms in GROUPS:
            ms = [x for x in ms if x in p.index]
            if not ms:
                continue
            lines.append(rf"\multicolumn{{8}}{{l}}{{\textit{{{g}}}}} \\")
            for x in ms:
                lines.append(f"{NAMES[x]} & " + " & ".join(f2(p.loc[x, t]) for t in TYPES) + r" \\")
        body = r"""\begin{tabular}{lccccccc}
\toprule
\textbf{Metric} & Anat. & Lat. & Meas. & Neg. & Sev. & Temp. & Unc. \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}"""
        write(f"tab_types_{c}.tex", body)


# ------------------------------------------------------------------ Appendix: subtypes
def tab_subtypes():
    A = {c: pd.read_csv(R / f"2_full_{c}/extended/A_subtypes.csv") for c in ["iu", "mimic"]}
    cols = [("severity", "adjacent"), ("severity", "extreme"), ("measurement", "value"), ("measurement", "unit"),
            ("uncertainty", "hedged->definite"), ("uncertainty", "definite->hedged")]
    lines = []
    for g, ms in GROUPS:
        ms = [x for x in ms if x in set(A["iu"].metric)]
        lines.append(rf"\multicolumn{{7}}{{l}}{{\textit{{{g}}}}} \\")
        for x in ms:
            cells = []
            for et, st in cols:
                v = []
                for c in ["iu", "mimic"]:
                    a = A[c][(A[c].metric == x) & (A[c].edit_type == et) & (A[c].subtype == st)].paired_acc_S0
                    v.append(f2(a.iloc[0]) if len(a) else "--")
                cells.append("/".join(v))
            lines.append(f"{NAMES[x]} & " + " & ".join(cells) + r" \\")
    body = r"""\begin{tabular}{lcccccc}
\toprule
 & \multicolumn{2}{c}{\textbf{Severity}} & \multicolumn{2}{c}{\textbf{Measurement}} & \multicolumn{2}{c}{\textbf{Uncertainty}} \\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}
\textbf{Metric} & adjacent & extreme & value & unit$^{\ddagger}$ & hedged$\to$def. & def.$\to$hedged \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}"""
    write("tab_subtypes.tex", body)


# ------------------------------------------------------------------ Appendix: robustness
def tab_robust():
    F = {c: pd.read_csv(R / f"2_full_{c}/extended/F_robustness_subsets.csv") for c in ["iu", "mimic"]}
    subs = ["all targets", "excl. measurement:unit (P edit larger than C)", "excl. P lexicon pending expert review", "excl. all three"]
    n = {c: F[c].groupby("subset").n.first() for c in F}
    lines = []
    for g, ms in GROUPS:
        ms = [x for x in ms if x in set(F["iu"].metric)]
        lines.append(rf"\multicolumn{{5}}{{l}}{{\textit{{{g}}}}} \\")
        for x in ms:
            cells = []
            for s in subs:
                v = []
                for c in ["iu", "mimic"]:
                    a = F[c][(F[c].metric == x) & (F[c].subset == s)].S0
                    v.append(f2(a.iloc[0]) if len(a) else "--")
                cells.append("/".join(v))
            lines.append(f"{NAMES[x]} & " + " & ".join(cells) + r" \\")
    head = " & ".join(f"{n['iu'][s]}/{n['mimic'][s]}" for s in subs)
    body = r"""\begin{tabular}{lcccc}
\toprule
\textbf{Metric} & All & $-$ unit subtype & $-$ flagged lexicon & $-$ all flagged \\
$n$ (IU/MIMIC) & """ + head + r""" \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}"""
    write("tab_robust.tex", body)
    for c in ["iu", "mimic"]:
        macros[f"nConservative{c}"] = str(int(n[c]["excl. all three"]))


# ------------------------------------------------------------------ Appendix: decomposition + prompt sensitivity + CRIMSON attribution + OI
def tab_decomp():
    D = {c: pd.read_csv(R / f"2_full_{c}/analysis/decomposition.csv").set_index("metric") for c in ["iu", "mimic"]}
    X = {c: pd.read_csv(R / f"2_full_{c}/review1007/C_exchange_rate.csv").set_index("metric") for c in ["iu", "mimic"]}

    def xr(c, m, col):
        if m not in X[c].index or pd.isna(X[c].loc[m, col]):
            return "--"
        v = X[c].loc[m, col]
        return f"{v:.0f}" if abs(v) >= 10 else f"{v:.1f}"
    lines = []
    for g, ms in GROUPS:
        ms = [x for x in ms if x in D["iu"].index]
        lines.append(rf"\multicolumn{{8}}{{l}}{{\textit{{{g}}}}} \\")
        for x in ms:
            cells = []
            for col in ["meaning_effect_S0", "surface_S1", "surface_S2", "meaning_effect_S2"]:
                cells.append("/".join(f2(D[c].loc[x, col]) if x in D[c].index else "--" for c in ["iu", "mimic"]))
            cells.append("/".join(f2(D[c].loc[x, "interaction_S2"]) if x in D[c].index else "--" for c in ["iu", "mimic"]))
            cells.append("/".join(xr(c, x, "reorder_in_meaning_changes") for c in ["iu", "mimic"]))
            cells.append("/".join(xr(c, x, "paraphrase_in_meaning_changes") for c in ["iu", "mimic"]))
            lines.append(f"{NAMES[x]} & " + " & ".join(cells) + r" \\")
    body = r"""\begin{tabular}{lccccccc}
\toprule
 & \multicolumn{5}{c}{\textbf{Standardised effects}} & \multicolumn{2}{c}{\textbf{Exchange rate}} \\
\cmidrule(lr){2-6}\cmidrule(lr){7-8}
\textbf{Metric} & Meaning (C0$-$P0) & Surface S1 (P1$-$P0) & Surface S2 (P2$-$P0) & Meaning@S2 (C2$-$P2) & Interaction S2 & reorder & paraphrase \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}"""
    write("tab_decomp.tex", body)


# ------------------------------------------------------------------ Appendix (10/7 review): all five comparisons incl. Ctrl-1, win/tie/loss
def tab_allcond():
    W = {c: pd.read_csv(R / f"2_full_{c}/review1007/A_win_tie_loss.csv") for c in ["iu", "mimic"]}
    lines = []
    for g, ms in GROUPS:
        ms = [x for x in ms if x in set(W["iu"].metric)]
        lines.append(rf"\multicolumn{{7}}{{l}}{{\textit{{{g}}}}} \\")
        for x in ms:
            cells = []
            for cond in ["Ctrl-0", "Ctrl-1", "Ctrl-2"]:
                v = []
                for c in ["iu", "mimic"]:
                    a = W[c][(W[c].metric == x) & (W[c].condition == cond)]
                    v.append(f2(a.paired_acc.iloc[0]) if len(a) and not pd.isna(a.paired_acc.iloc[0]) else "--")
                cells.append("/".join(v))
            for col in ["win", "tie", "loss"]:
                v = []
                for c in ["iu", "mimic"]:
                    a = W[c][(W[c].metric == x) & (W[c].condition == "Ctrl-0")]
                    v.append(f2(a[col].iloc[0]) if len(a) and not pd.isna(a[col].iloc[0]) else "--")
                cells.append("/".join(v))
            lines.append(f"{NAMES[x]} & " + " & ".join(cells) + r" \\")
    body = r"""\begin{tabular}{lcccccc}
\toprule
 & \multicolumn{3}{c}{\textbf{Paired accuracy}} & \multicolumn{3}{c}{\textbf{\textsc{Ctrl-0} outcome shares}} \\
\cmidrule(lr){2-4}\cmidrule(lr){5-7}
\textbf{Metric} & \textsc{Ctrl-0} & \textsc{Ctrl-1} & \textsc{Ctrl-2} & win & tie & loss \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}"""
    write("tab_allcond.tex", body)


def tab_prompt():
    s = summ("iu").pivot(index="metric", columns="condition", values="paired_acc")
    j = pd.read_csv(R / "2_full_iu/analysis/judge_cells.csv").pivot(index="judge", columns="cell", values="rate_changed")
    lines = []
    for tag, nm in [("gemma3_27b", "Gemma-3-27B"), ("qwen3_32b", "Qwen3-32B"), ("gptoss_20b", "gpt-oss-20b"), ("gptoss_120b", "gpt-oss-120b")]:
        for pr in ["rubric", "errors"]:
            m = f"{tag}__{pr}"
            if m not in s.index:
                continue
            lines.append(f"{nm} & {pr} & {f2(s.loc[m,'controlled_S0'])} & {f2(s.loc[m,'controlled_S2'])} & {f2(s.loc[m,'confound_reevalmed'])} & {f2(j.loc[m,'P0'])} & {f2(j.loc[m,'P2'])} & {f2(j.loc[m,'C2'])} \\\\")
            macros[f"prompt{tag.replace('_','').replace('3','three').replace('27','twentyseven').replace('32','thirtytwo').replace('20','twenty').replace('120','onetwenty')}{pr}Stwo"] = f2(s.loc[m, "controlled_S2"])
    body = r"""\begin{tabular}{llcccccc}
\toprule
 & & \multicolumn{3}{c}{\textbf{Paired accuracy}} & \multicolumn{3}{c}{\textbf{Rate flagged}} \\
\cmidrule(lr){3-5}\cmidrule(lr){6-8}
\textbf{Judge} & \textbf{Prompt} & \textsc{Ctrl-0} & \textsc{Ctrl-2} & \textsc{Conf-P} & P0 $\downarrow$ & P2 $\downarrow$ & C2 $\uparrow$ \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}"""
    write("tab_prompt.tex", body)


def tab_crimson():
    E = {c: pd.read_csv(R / f"2_full_{c}/extended/E_crimson_attribution.csv") for c in ["iu", "mimic"]}
    P = {c: pd.read_csv(R / f"2_full_{c}/analysis/per_type.csv") for c in ["iu", "mimic"]}
    exp = {"anatomy": "location", "laterality": "location", "measurement": "measurement", "negation": "false/missing finding",
           "severity": "severity", "temporal": "temporal", "uncertainty": "certainty"}
    lines = []
    for t in TYPES:
        cells = [exp[t]]
        for col, cell in [("any_error", "C0"), ("expected_category_fired", "C0"), ("any_error", "P0")]:
            cells.append("/".join(f2(E[c][(E[c].cell == cell) & (E[c].edit_type == t)][col].iloc[0]) for c in ["iu", "mimic"]))
        cells.append("/".join(f2(P[c][(P[c].metric == "crimson") & (P[c].condition == "controlled_S0") & (P[c].edit_type == t)].paired_acc.iloc[0]) for c in ["iu", "mimic"]))
        lines.append(f"{t.capitalize()} & " + " & ".join(cells) + r" \\")
    body = r"""\begin{tabular}{llcccc}
\toprule
\textbf{Edit type} & \textbf{Expected category} & C0: any error & C0: expected cat. & P0: any error & Score paired acc. \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}"""
    write("tab_crimson.tex", body)


def tab_sets():
    lines = []
    for c, nm in [("iu", "IU X-Ray"), ("mimic", "MIMIC-CXR")]:
        t = pd.read_csv(NEW / f"data/pairs/full_{c}_targets.csv")
        log = pd.read_csv(NEW / f"data/pairs/full_{c}_paraphrase_log.csv")
        acc = log.groupby(["report_id", "section", "sent_idx"]).accepted.any().mean()
        cnt = t.edit_type.value_counts()
        lines.append(f"{nm} & {len(t):,} & {t.report_id.nunique():,} & " + " & ".join(str(int(cnt.get(x, 0))) for x in TYPES) + f" & {t.pattern.nunique()} & {100*acc:.1f} \\\\")
        macros[f"n{c}targets"] = f"{len(t):,}"
        macros[f"n{c}reports"] = f"{t.report_id.nunique():,}"
        macros[f"para{c}"] = f"{100*acc:.1f}"
    body = r"""\begin{tabular}{lrrrrrrrrrrr}
\toprule
\textbf{Corpus} & \textbf{Targets} & \textbf{Reports} & Anat. & Lat. & Meas. & Neg. & Sev. & Temp. & Unc. & \textbf{Patterns} & \textbf{Para.\ acc.\ (\%)} \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}"""
    write("tab_sets.tex", body)


def tab_oi():
    p = pd.read_csv(R / "2_full_mimicoi/analysis/per_type.csv")
    f = pd.read_csv(R / "2_full_mimicoi/shortcut_floor_all.csv").set_index("condition")
    lines = [r"\textit{Surface-only classifier (AUROC)} & " + " & ".join(f2(f.loc[f"{c}/{t}", "surface_only_LR_auroc"]) for c in ["controlled_S0", "controlled_S2"] for t in ["omission", "insertion"]) + r" \\", r"\midrule"]
    for g, ms in GROUPS:
        ms = [x for x in ms if x in set(p.metric)]
        for x in ms:
            cells = []
            for c in ["controlled_S0", "controlled_S2"]:
                for t in ["omission", "insertion"]:
                    v = p[(p.metric == x) & (p.condition == c) & (p.edit_type == t)].paired_acc
                    cells.append(f2(v.iloc[0]) if len(v) else "--")
            lines.append(f"{NAMES[x]} & " + " & ".join(cells) + r" \\")
    body = r"""\begin{tabular}{lcccc}
\toprule
 & \multicolumn{2}{c}{\textsc{Ctrl-0}} & \multicolumn{2}{c}{\textsc{Ctrl-2}} \\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}
\textbf{Metric} & Omission & Insertion & Omission & Insertion \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}"""
    write("tab_oi.tex", body)


# ------------------------------------------------------------------ Appendix (10/7 review): follow-up experiments (scripts/23, 24). Skipped if inputs are missing.
def tab_review():
    # RaTE-Eval synthetic task: all scorers
    f = R / "3_x3_audit/rate_eval_task3_metrics.csv"
    if f.exists():
        t = pd.read_csv(f).set_index("metric")
        lines = []
        for g, ms in GROUPS:
            ms = [x for x in ms if x in t.index]
            if ms:
                lines.append(rf"\multicolumn{{3}}{{l}}{{\textit{{{g}}}}} \\")
            lines += [f"{NAMES[x]} & {f2(t.loc[x, 'paired_acc'])} & {f2(t.loc[x, 'tie'])} \\\\" for x in ms]
        write("tab_rate3.tex", r"""\begin{tabular}{lcc}
\toprule
\textbf{Scorer} & \textbf{Paired acc.} & \textbf{Tie} \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}""")
    # alternative paraphraser
    f = R / "2_full_iualt/analysis/alt_vs_orig.csv"
    if f.exists():
        t = pd.read_csv(f).set_index("metric")
        lines = []
        for g, ms in GROUPS:
            ms = [x for x in ms if x in t.index]
            if ms:
                lines.append(rf"\multicolumn{{6}}{{l}}{{\textit{{{g}}}}} \\")
            for x in ms:
                r = t.loc[x]
                lines.append(f"{NAMES[x]} & {f2(r['Ctrl-0 (orig run)'])} & {f2(r['Ctrl-2 orig paraphraser'])} & {f2(r['Ctrl-2 alt paraphraser'])} & "
                             f"{f2(r['drop orig'], 3)} [{f2(r['drop orig lo'], 3)}, {f2(r['drop orig hi'], 3)}] & {f2(r['drop alt'], 3)} [{f2(r['drop alt lo'], 3)}, {f2(r['drop alt hi'], 3)}] \\\\")
        write("tab_alt.tex", r"""\begin{tabular}{lccccc}
\toprule
 & & \multicolumn{2}{c}{\textbf{\textsc{Ctrl-2}}} & \multicolumn{2}{c}{\textbf{Drop \textsc{Ctrl-0} $-$ \textsc{Ctrl-2}}} \\
\cmidrule(lr){3-4}\cmidrule(lr){5-6}
\textbf{Scorer} & \textsc{Ctrl-0} & Qwen2.5 & Llama-3.1 + guard & Qwen2.5 & Llama-3.1 + guard \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}""")
    # rubric vs rubric_unit
    lines = []
    for c, cn in [("iu", "IU"), ("mimic", "MIMIC")]:
        f = R / f"2_full_{c}/review1007/G_rubric_unit.csv"
        if not f.exists():
            continue
        t = pd.read_csv(f)
        for r in t.itertuples(index=False):
            d = r._asdict()
            vals = list(d.values())
            nm = NAMES.get(f"{vals[0]}__rubric", vals[0])
            lines.append(f"{cn} & {nm} & {vals[1].replace('_', '-')} & " + " & ".join(f2(v) for v in [vals[3], vals[4], vals[6], vals[7], vals[8], vals[9], vals[10]]) + r" \\")
    if lines:
        write("tab_unit.tex", r"""\begin{tabular}{lllccccccc}
\toprule
 & & & \multicolumn{2}{c}{\textbf{Measurement}} & \multicolumn{3}{c}{\textbf{All types}} & \multicolumn{2}{c}{\textbf{Paired acc.}} \\
\cmidrule(lr){4-5}\cmidrule(lr){6-8}\cmidrule(lr){9-10}
\textbf{Corpus} & \textbf{Judge} & \textbf{Prompt} & P0 value $\downarrow$ & C0 $\uparrow$ & P0 other $\downarrow$ & C0 $\uparrow$ & C2 $\uparrow$ & \textsc{Ctrl-0} & \textsc{Ctrl-2} \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}""")
    # external validity
    f = R / "4_external_validity/per_metric.csv"
    if f.exists():
        t = pd.read_csv(f).set_index("metric")
        hc = [c for c in t.columns if c.startswith("Task")]
        lines = []
        for g, ms in GROUPS:
            ms = [x for x in ms if x in t.index]
            if ms:
                lines.append(rf"\multicolumn{{{1 + len(hc) + 5}}}{{l}}{{\textit{{{g}}}}} \\")
            for x in ms:
                lines.append(f"{NAMES[x]} & " + " & ".join(f2(t.loc[x, c]) for c in hc + ["Conf-R", "Conf-P", "Ctrl-0", "Ctrl-2", "mono tau (fixed surface)"]) + r" \\")
        x = pd.read_csv(R / "4_external_validity/across_metrics.csv")
        foot = []
        for sub in x.scorers.unique():
            for hs in hc:
                d = x[(x.scorers == sub) & (x["human set"] == hs)].set_index("our column")
                if d.empty:
                    continue
                if sub != "all scorers" and "Task 2" in hs:
                    continue                                   # no judge was run on the paragraph task: identical to the row above
                foot.append(rf"$\rho$ with {hs.split(' (')[0]}, {sub.replace('metrics only (no LLM judges)', 'without judges')} ($n{{=}}{int(d.n_scorers.iloc[0])}$) & " + "& " * len(hc) +
                            " & ".join(f2(d.loc[c, "spearman"]) if c in d.index else "--" for c in ["Conf-R", "Conf-P", "Ctrl-0", "Ctrl-2", "mono tau (fixed surface)"]) + r" \\")
        write("tab_external.tex", r"""\begin{tabular}{l""" + "c" * (len(hc) + 5) + r"""}
\toprule
 & \multicolumn{""" + str(len(hc)) + r"""}{c}{\textbf{Kendall $\tau$ with radiologists}} & \multicolumn{5}{c}{\textbf{This paper (mean of IU, MIMIC)}} \\
\cmidrule(lr){2-""" + str(1 + len(hc)) + r"""}\cmidrule(lr){""" + str(2 + len(hc)) + "-" + str(6 + len(hc)) + r"""}
\textbf{Scorer} & """ + " & ".join(h.replace(" (", " \\scriptsize(").replace(")", ")\\small ") if False else h.split(" (")[0] + ("" if "all" not in h else " (all)") for h in hc) + r""" & \textsc{Conf-R} & \textsc{Conf-P} & \textsc{Ctrl-0} & \textsc{Ctrl-2} & Mono.\ $\tau$ \\
\midrule
""" + "\n".join(lines) + "\n\\midrule\n" + "\n".join(foot) + r"""
\bottomrule
\end{tabular}""")


def more_macros():
    for c in ["iu", "mimic"]:
        C = pd.read_csv(R / f"2_full_{c}/extended/C_contrasts.csv").set_index("metric")
        macros[f"greendrop{c}"] = f2(C.loc["green", "S0_minus_S2"], 3)
        macros[f"greendroplo{c}"] = f2(C.loc["green", "drop_lo"], 3)
        macros[f"greendrophi{c}"] = f2(C.loc["green", "drop_hi"], 3)
    safe = lambda k: "".join(ch for ch in k if ch.isalpha())
    txt = "% auto-generated by scripts/20_make_paper_tables.py — do not edit\n" + "\n".join(f"\\newcommand{{\\num{safe(k)}}}{{{v}}}" for k, v in sorted(macros.items()))
    write("numbers.tex", txt)


if __name__ == "__main__":
    tab_sets(); tab_surface(); tab_main(); tab_judges(); tab_mono(); tab_types(); tab_subtypes(); tab_robust(); tab_decomp(); tab_allcond(); tab_prompt(); tab_crimson(); tab_oi(); tab_review(); more_macros()
