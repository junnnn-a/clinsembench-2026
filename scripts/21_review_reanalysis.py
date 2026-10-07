#!/usr/bin/env python
"""
21_review_reanalysis.py — re-analyses requested by the 10/7 review (docs/13). CPU only, no new scoring.

  A. win / tie / loss decomposition of every controlled comparison (is 0.52 "slightly above chance" or "almost all ties"?)
  B. strict-matched subset: targets where P0 and C0 are EXACTLY tied on Jaccard and token F1 (so the meaning-blind
     baselines are at 0.5 by construction); paired accuracy of all metrics on that subset, Ctrl-0 and Ctrl-2
  C. "exchange rate": how many matched meaning changes is one context paraphrase worth?  (D(P2)-D(P0)) / (D(C0)-D(P0))
  D. S2 fidelity subset: targets whose paraphrased context keeps the multiset of degree words (defect D-11);
     Ctrl-2, Conf-P and the Ctrl-0 -> Ctrl-2 drop recomputed there
  E. label-contested subsets: uncertainty without "consistent/compatible with" patterns; defect D-10 ("-sided sided")
  F. interaction terms and Ctrl-1 numbers for the text-vs-table check

Output: results/2_full_{corpus}/review1007/*.csv + REVIEW.md
Run: /opt/conda/envs/clinsev/bin/python scripts/21_review_reanalysis.py
"""
from __future__ import annotations

import importlib.util
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

NEW = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("ext", NEW / "scripts/14_extended_analysis.py")
EXT = importlib.util.module_from_spec(spec); spec.loader.exec_module(EXT)
DEG = re.compile(r"\b(?:trace|minimal|minimally|mild|mildly|slight|slightly|small|tiny|moderate|moderately|large|severe|severely|"
                 r"marked|markedly|extensive|massive|significant|significantly|substantial|prominent|subtle|gross|grossly)\b", re.I)
TOK = re.compile(r"\b\w+\b")


def toks(t):
    return TOK.findall(re.sub(r"[^a-z0-9. ]+", " ", str(t).lower()))


def wtl(c, p):
    d = (c - p)
    d = d[np.isfinite(d)]
    n = len(d)
    return (float((d > 0).mean()), float((d == 0).mean()), float((d < 0).mean())) if n else (np.nan,) * 3


def pacc(c, p):
    w, t, l = wtl(c, p)
    return w + 0.5 * t


def md(df, f=3):
    return EXT.md(df, f)


def main():
    for corpus in ["iu", "mimic"]:
        out = NEW / f"results/2_full_{corpus}/review1007"
        out.mkdir(parents=True, exist_ok=True)
        pairs, cand, metrics = EXT.load(corpus)
        w = EXT.wide(cand, metrics).reset_index(drop=True)
        tg = pd.read_csv(NEW / f"data/pairs/full_{corpus}_targets.csv")
        rep = [f"# 10/7 review re-analysis — {corpus}\n"]

        # ---------- A. win/tie/loss
        rows = []
        for m in metrics:
            for cond, (c, p) in {"Ctrl-0": ("C0", "P0"), "Ctrl-1": ("C1", "P1"), "Ctrl-2": ("C2", "P2"), "Conf-R": ("C0", "P1"), "Conf-P": ("C0", "P2")}.items():
                W, T, L = wtl(w[f"{m}|{c}"].to_numpy(float), w[f"{m}|{p}"].to_numpy(float))
                rows.append({"metric": m, "condition": cond, "win": W, "tie": T, "loss": L, "paired_acc": W + 0.5 * T,
                             "win_among_decided": W / (W + L) if (W + L) > 0 else np.nan})
        A = pd.DataFrame(rows)
        A.to_csv(out / "A_win_tie_loss.csv", index=False)
        a0 = A[A.condition == "Ctrl-0"][["metric", "win", "tie", "loss", "paired_acc", "win_among_decided"]]
        rep += ["## A. Ctrl-0: win / tie / loss\n", md(a0), ""]

        # ---------- B. strict-matched subset
        P = pairs.pivot(index="target_id", columns="cell", values="candidate")
        ref = pairs.drop_duplicates("target_id").set_index("target_id").reference
        def bag_equal(tid, a, b):
            r = Counter(toks(ref[tid])); x = Counter(toks(P.loc[tid, a])); y = Counter(toks(P.loc[tid, b]))
            jx = len(set(r) & set(x)) / len(set(r) | set(x)); jy = len(set(r) & set(y)) / len(set(r) | set(y))
            ix, iy = sum((r & x).values()), sum((r & y).values())
            return abs(jx - jy) < 1e-12 and ix == iy and sum(x.values()) == sum(y.values())
        strict0 = [t for t in w.target_id if bag_equal(t, "P0", "C0")]
        ws = w[w.target_id.isin(strict0)]
        rows = []
        for m in metrics:
            rows.append({"metric": m, "n_strict": len(ws),
                         "Ctrl-0 all": pacc(w[f"{m}|C0"].to_numpy(float), w[f"{m}|P0"].to_numpy(float)),
                         "Ctrl-0 strict": pacc(ws[f"{m}|C0"].to_numpy(float), ws[f"{m}|P0"].to_numpy(float)),
                         "Ctrl-2 all": pacc(w[f"{m}|C2"].to_numpy(float), w[f"{m}|P2"].to_numpy(float)),
                         "Ctrl-2 strict": pacc(ws[f"{m}|C2"].to_numpy(float), ws[f"{m}|P2"].to_numpy(float)),
                         "tie_strict": wtl(ws[f"{m}|C0"].to_numpy(float), ws[f"{m}|P0"].to_numpy(float))[1]})
        B = pd.DataFrame(rows)
        B.to_csv(out / "B_strict_matched.csv", index=False)
        comp = tg[tg.target_id.isin(strict0)].edit_type.value_counts().to_dict()
        rep += [f"## B. Strict-matched subset (P0 and C0 exactly tied on Jaccard and token F1): n={len(ws)} of {len(w)}; by type {comp}\n", md(B), ""]

        # ---------- C. exchange rate
        rows = []
        for m in metrics:
            num = float(np.nanmean(w[f"{m}|P2"] - w[f"{m}|P0"]))
            num1 = float(np.nanmean(w[f"{m}|P1"] - w[f"{m}|P0"]))
            den = float(np.nanmean(w[f"{m}|C0"] - w[f"{m}|P0"]))
            rows.append({"metric": m, "penalty_meaning_change": den, "penalty_paraphrase": num, "penalty_reorder": num1,
                         "paraphrase_in_meaning_changes": num / den if den > 1e-9 else np.nan,
                         "reorder_in_meaning_changes": num1 / den if den > 1e-9 else np.nan})
        C = pd.DataFrame(rows)
        C.to_csv(out / "C_exchange_rate.csv", index=False)
        rep += ["## C. Exchange rate: one context paraphrase / one reordering, in units of one matched meaning change\n",
                md(C[["metric", "paraphrase_in_meaning_changes", "reorder_in_meaning_changes"]], 2), ""]

        # ---------- D. S2 fidelity subset (degree words preserved in context)
        deg_ok = [t for t in w.target_id if sorted(x.lower() for x in DEG.findall(str(P.loc[t, "P2"]))) == sorted(x.lower() for x in DEG.findall(str(P.loc[t, "P0"])))]
        wd = w[w.target_id.isin(deg_ok)]
        rows = []
        for m in metrics:
            f = lambda d, a, b: pacc(d[f"{m}|{a}"].to_numpy(float), d[f"{m}|{b}"].to_numpy(float))
            rows.append({"metric": m, "n": len(wd), "Ctrl-0": f(wd, "C0", "P0"), "Ctrl-2": f(wd, "C2", "P2"), "Conf-P": f(wd, "C0", "P2"),
                         "drop(all)": f(w, "C0", "P0") - f(w, "C2", "P2"), "drop(degree-preserving)": f(wd, "C0", "P0") - f(wd, "C2", "P2")})
        D = pd.DataFrame(rows)
        D.to_csv(out / "D_s2_degree_preserving.csv", index=False)
        rep += [f"## D. S2 subset whose paraphrased context keeps all degree words: n={len(wd)} of {len(w)}\n", md(D), ""]

        # ---------- E. contested labels
        unc = tg[tg.edit_type == "uncertainty"]
        contested = unc[unc.pattern.str.contains("consistent with|compatible with|suspicious for|worrisome for|suggestive of|diagnostic of", regex=True)].target_id
        sided = tg[tg.p_sent.str.contains(r"-sided sided", regex=True)].target_id
        wu = w[w.target_id.isin(set(unc.target_id) - set(contested))]
        wuall = w[w.target_id.isin(set(unc.target_id))]
        rows = [{"metric": m, "uncertainty all (n=%d)" % len(wuall): pacc(wuall[f"{m}|C0"].to_numpy(float), wuall[f"{m}|P0"].to_numpy(float)),
                 "uncertainty w/o consistent-with family (n=%d)" % len(wu): pacc(wu[f"{m}|C0"].to_numpy(float), wu[f"{m}|P0"].to_numpy(float))} for m in metrics]
        E = pd.DataFrame(rows)
        E.to_csv(out / "E_uncertainty_contested.csv", index=False)
        rep += [f"## E. Uncertainty without the 'consistent with / suspicious for / suggestive of' family; D-10 '-sided sided' targets: {len(sided)}\n", md(E), ""]
        pd.DataFrame({"target_id": sided}).to_csv(out / "E_defect_D10_targets.csv", index=False)

        # ---------- F. interactions + judge C0 detection for uncertainty
        dec = pd.read_csv(NEW / f"results/2_full_{corpus}/analysis/decomposition.csv")
        rep += ["## F. Interaction (meaning x S2) and (meaning x S1) from decomposition.csv\n",
                md(dec.assign(interaction_S1=dec.meaning_effect_S1 - dec.meaning_effect_S0)[["metric", "meaning_effect_S0", "surface_S1", "surface_S2", "interaction_S1", "interaction_S2"]]), ""]
        jt = pd.read_csv(NEW / f"results/2_full_{corpus}/analysis/judge_cells_by_type.csv")
        rep += ["### judges: CHANGED rate on uncertainty, C0 vs C2\n",
                md(jt[(jt.edit_type == "uncertainty") & jt.cell.isin(["C0", "C2", "P0"])].pivot(index="judge", columns="cell", values="rate_changed").reset_index(), 2), ""]
        (out / "REVIEW.md").write_text("\n".join(rep))
        print(f"[{corpus}] wrote {out}/REVIEW.md  strict={len(ws)} degree_ok={len(wd)} D10={len(sided)}")


if __name__ == "__main__":
    main()
