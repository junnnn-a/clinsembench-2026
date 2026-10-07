#!/usr/bin/env python
"""
17_make_figures.py — paper figures from the full-set analysis (static, paper size).

  fig2_confound_vs_controlled.{pdf,png}   dumbbell per metric: paired accuracy under the v1-type confound (C0 vs P1)
                                          -> controlled (C0 vs P0); one panel per corpus; chance line at 0.5 and
                                          the meaning-blind Jaccard baseline marked.
  fig3_meaning_vs_surface.{pdf,png}       scatter: standardised meaning effect (x) vs surface effect of paraphrase (y)
                                          per metric / judge, both corpora (small multiples).
  fig_dose_response.{pdf,png}             extra penalty on the meaning-preserving candidate vs amount rewritten.

Design notes (dataviz skill): form chosen by job (before->after per item = dumbbell, one hue two shades +
filled/hollow markers; all-pairs scatter capped at three categorical hues, slots 1-3 of the validated reference
palette); direct labels; recessive grid; no dual axes; text in ink colours, never series colours.

Run: /opt/conda/envs/clinsev/bin/python scripts/17_make_figures.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

NEW = Path(__file__).resolve().parent.parent
OUT = NEW / "figures/paper"
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"
BLUE, BLUE_LIGHT, ORANGE, AQUA = "#2a78d6", "#a9c9ef", "#eb6834", "#1baf7a"

NAMES = {
    "jaccard": "Jaccard", "token_f1": "Token F1", "bleu": "BLEU", "rougeL": "ROUGE-L",
    "bertscore_distilbert": "BERTScore (DistilBERT)", "bertscore_roberta_large": "BERTScore (RoBERTa-L)",
    "bertscore_deberta_mnli": "BERTScore (DeBERTa-MNLI)", "f1chexbert": "F1CheXbert", "temporal": "Temporal F1",
    "srrbert": "SRR-BERT", "radgraph": "RadGraph F1", "ratescore": "RaTEScore", "radcliq": "RadCliQ-v1",
    "green": "GREEN", "crimson": "CRIMSON", "llama31_8b__rubric": "Llama-3.1-8B judge",
    "gemma3_27b__rubric": "Gemma-3-27B judge", "qwen3_32b__rubric": "Qwen3-32B judge",
    "gptoss_20b__rubric": "gpt-oss-20b judge", "gptoss_120b__rubric": "gpt-oss-120b judge",
}
GROUP = {**{k: "Lexical / embedding" for k in ["jaccard", "token_f1", "bleu", "rougeL", "bertscore_distilbert",
                                                 "bertscore_roberta_large", "bertscore_deberta_mnli"]},
         **{k: "Clinical (non-LLM)" for k in ["f1chexbert", "temporal", "srrbert", "radgraph", "ratescore", "radcliq"]},
         **{k: "LLM-based" for k in ["green", "crimson", "llama31_8b__rubric", "gemma3_27b__rubric", "qwen3_32b__rubric",
                                      "gptoss_20b__rubric", "gptoss_120b__rubric"]}}
GCOL = {"Lexical / embedding": BLUE, "Clinical (non-LLM)": ORANGE, "LLM-based": AQUA}
CORPORA = [("iu", "IU X-Ray"), ("mimic", "MIMIC-CXR")]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "pdf.fonttype": 42})


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    print("[wrote]", OUT / f"{name}.pdf")


def fig2():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 4.3), sharey=True)
    order = None
    for ax, (c, title) in zip(axes, CORPORA):
        s = pd.read_csv(NEW / f"results/2_full_{c}/analysis/summary_by_condition.csv")
        s = s[s.metric.isin(NAMES)]
        w = s.pivot(index="metric", columns="condition", values="paired_acc")
        if order is None:
            order = w.sort_values("controlled_S0").index.tolist()
        w = w.reindex([m for m in order if m in w.index])
        y = range(len(w))
        ax.axvline(0.5, color=INK2, lw=0.8, ls=(0, (3, 3)), zorder=1)
        for i, m in enumerate(w.index):
            a, b = w.loc[m, "confound_v1"], w.loc[m, "controlled_S0"]
            ax.plot([a, b], [i, i], color=GRID, lw=2.0, solid_capstyle="round", zorder=2)
            ax.scatter([a], [i], s=26, facecolor=SURFACE, edgecolor=BLUE, linewidth=1.2, zorder=3)
            ax.scatter([b], [i], s=26, facecolor=BLUE, edgecolor=SURFACE, linewidth=0.6, zorder=4)
        ax.set_yticks(list(y))
        ax.set_yticklabels([NAMES[m] for m in w.index])
        ax.set_xlim(-0.03, 1.03)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.grid(axis="x", color=GRID, lw=0.5)
        ax.set_axisbelow(True)
        ax.set_title(title, loc="left", color=INK, fontsize=8.5, fontweight="bold")
        ax.tick_params(length=0)
        ax.text(0.5, len(w) - 0.35, "chance", color=INK2, ha="center", va="bottom", fontsize=6.5)
    h1 = plt.Line2D([], [], marker="o", ls="", markerfacecolor=SURFACE, markeredgecolor=BLUE, markeredgewidth=1.2, markersize=5,
                    label="Surface-confounded comparison (Conf-R: benign edit = reordered sentences)")
    h2 = plt.Line2D([], [], marker="o", ls="", markerfacecolor=BLUE, markeredgecolor=SURFACE, markersize=5.5,
                    label="Surface-controlled comparison (matched minimal edits)")
    fig.supxlabel("Paired accuracy: share of targets where the meaning-changing candidate is penalised more", color=INK2, fontsize=7.5, y=0.075)
    fig.legend(handles=[h1, h2], loc="lower center", ncol=1, frameon=False, bbox_to_anchor=(0.5, -0.075), labelcolor=INK)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "fig2_confound_vs_controlled")


def _scatter(ax, c, fs, crowd_x=0.62, step=0.135, short_names=True):
    d = pd.read_csv(NEW / f"results/2_full_{c}/analysis/decomposition.csv")
    d = d[d.metric.isin(NAMES)]
    ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
    for g, col in GCOL.items():
        s = d[d.metric.map(GROUP) == g]
        ax.scatter(s.meaning_effect_S0, s.surface_S2, s=30, color=col, edgecolor=SURFACE, linewidth=0.8, zorder=3, label=g)
    short = lambda m: NAMES[m].replace("BERTScore", "BS").replace(" judge", "").replace("DistilBERT", "Distil").replace("DeBERTa-MNLI", "DeBERTa").replace("Temporal F1", "Temporal")
    crowd = d[(d.meaning_effect_S0 < 0.4) & (d.surface_S2 > 1.1)].sort_values("surface_S2", ascending=False)
    rest = d[~d.metric.isin(crowd.metric)]
    # hand-tuned offsets (points) for the labels that would otherwise collide
    off = {"gptoss_20b__rubric": (-34, 8), "gptoss_120b__rubric": (-54, -1), "qwen3_32b__rubric": (5, -3), "gemma3_27b__rubric": (-12, -10),
           "crimson": (-12, -10), "llama31_8b__rubric": (-44, 5), "green": (4, 3), "srrbert": (5, 2), "ratescore": (5, 1),
           "temporal": (4, 5), "f1chexbert": (5, -7)}
    for r in rest.itertuples():
        ax.annotate(short(r.metric), (r.meaning_effect_S0, r.surface_S2), xytext=off.get(r.metric, (4, 3)), textcoords="offset points", fontsize=fs, color=INK2)
    # the surface-dominated cluster: labels in a column to the right, joined by thin leader lines
    y_top = max(crowd.surface_S2.max(), 2.0) + 0.05
    for k, r in enumerate(crowd.itertuples()):
        ax.annotate(short(r.metric), xy=(r.meaning_effect_S0, r.surface_S2), xytext=(crowd_x, y_top - step * k), fontsize=fs, color=INK2, va="center",
                    arrowprops=dict(arrowstyle="-", color=GRID, lw=0.6, shrinkA=0, shrinkB=2))
    ax.set_xlabel("Meaning effect  (C0 − P0, SD units)")
    ax.grid(color=GRID, lw=0.4); ax.set_axisbelow(True); ax.tick_params(length=0)


def fig3():
    # main text: one panel drawn at column width (10/7 review: the two-panel version was unreadable at column width)
    fig, ax = plt.subplots(figsize=(3.25, 2.15))
    _scatter(ax, "iu", fs=6.3, crowd_x=0.78, step=0.14)
    ax.set_ylabel("Surface effect of paraphrase  (P2 − P0, SD)")
    ax.set_xlim(-0.12, 2.2); ax.set_ylim(-0.55, 2.2)
    ax.legend(frameon=False, loc="upper right", labelcolor=INK, handletextpad=0.2, fontsize=6.3, borderaxespad=0.1, bbox_to_anchor=(1.0, 0.72))
    fig.tight_layout(pad=0.3)
    save(fig, "fig3_meaning_vs_surface")
    # appendix: both corpora, full width
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.5), sharex=True, sharey=True)
    for ax, (c, title) in zip(axes, CORPORA):
        _scatter(ax, c, fs=6.3)
        ax.set_title(title, loc="left", color=INK, fontsize=8.5, fontweight="bold")
    axes[0].set_ylabel("Surface effect of paraphrase  (P2 − P0, SD units)")
    axes[0].legend(frameon=False, loc="lower left", labelcolor=INK, handletextpad=0.3, bbox_to_anchor=(0.0, 0.0))
    fig.tight_layout()
    save(fig, "fig3_meaning_vs_surface_both")


def fig_dose():
    show = ["bertscore_distilbert", "radgraph", "radcliq", "ratescore", "green", "crimson", "gemma3_27b__rubric"]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9), sharey=True)
    for ax, (c, title) in zip(axes, CORPORA):
        p = NEW / f"results/2_full_{c}/extended/B_surface_dose_response.csv"
        if not p.exists():
            continue
        b = pd.read_csv(p)
        bins = list(dict.fromkeys(b.surface_bin))
        x = [b[b.surface_bin == q].edit_frac_mean.iloc[0] for q in bins]
        for m in show:
            s = b[b.metric == m].set_index("surface_bin").reindex(bins)
            col = GCOL[GROUP[m]]
            ax.plot(x, s.P2_penalty_z, color=col, lw=1.4, marker="o", ms=3.2, markeredgecolor=SURFACE, markeredgewidth=0.5)
            ax.annotate(NAMES[m].replace("BERTScore (DistilBERT)", "BERTScore").replace(" judge", ""), (x[-1], s.P2_penalty_z.iloc[-1]),
                        xytext=(4, 0), textcoords="offset points", va="center", fontsize=5.8, color=INK2)
        ax.axhline(0, color=GRID, lw=0.8)
        ax.set_title(title, loc="left", color=INK, fontsize=8.5, fontweight="bold")
        ax.grid(color=GRID, lw=0.4); ax.set_axisbelow(True); ax.tick_params(length=0)
        ax.set_xlim(min(x) - 0.03, max(x) + 0.22)
    axes[0].set_ylabel("Extra penalty on a meaning-\npreserving candidate (SD units)")
    hs = [plt.Line2D([], [], color=c, lw=1.6, label=g) for g, c in GCOL.items()]
    axes[0].legend(handles=hs, frameon=False, loc="upper left", labelcolor=INK)
    fig.supxlabel("Share of reference tokens rewritten in the meaning-preserving candidate (quartile means)", color=INK2, fontsize=7.5, y=0.02)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, "fig_dose_response")


if __name__ == "__main__":
    fig2(); fig3(); fig_dose()
