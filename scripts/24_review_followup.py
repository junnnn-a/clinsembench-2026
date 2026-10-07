#!/usr/bin/env python
"""
24_review_followup.py — analyses of the GPU experiments launched for the 10/7 review (docs/13). Each part is skipped if its inputs are missing.

  A. S2 robustness (`iualt`): 301 IU targets re-paraphrased with another model family (Llama-3.1-8B) and a degree-word guard.
     Ctrl-0 / Ctrl-2 / Conf-P and the Ctrl-0 -> Ctrl-2 drop, next to the SAME targets under the original paraphraser (Qwen2.5-7B).
  B. `rubric_unit` vs `rubric`: does telling the judge that unit conversion is benign remove the measurement false alarms?
  C. RaTE-Eval synthetic task (`rate3`): paired accuracy of every scorer (opposite penalised more than synonym rewrite) + tie share.

Output: results/2_full_iualt/analysis/ALT.md + alt_vs_orig.csv ; results/2_full_{iu,mimic}/review1007/G_rubric_unit.csv ;
        results/3_x3_audit/rate_eval_task3_metrics.csv ; all summarised in results/REVIEW1007_FOLLOWUP.md
Run: /opt/conda/envs/clinsev/bin/python scripts/24_review_followup.py
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

NEW = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("ext", NEW / "scripts/14_extended_analysis.py")
EXT = importlib.util.module_from_spec(spec); spec.loader.exec_module(EXT)
md = EXT.md


def wtl(c, p):
    d = np.asarray(c, float) - np.asarray(p, float)
    d = d[np.isfinite(d)]
    return (float((d > 0).mean()), float((d == 0).mean()), float((d < 0).mean())) if len(d) else (np.nan,) * 3


def part_a(n_boot=1000):
    if not (NEW / "results/2_full_iualt/scores").exists():
        return ["## A. alt paraphraser: no scores yet\n"]
    _, ca, ma = EXT.load("iualt"); wa = EXT.wide(ca, ma)
    _, ci, mi = EXT.load("iu"); wi = EXT.wide(ci, mi)
    wi = wi[wi.target_id.isin(set(wa.target_id))].reset_index(drop=True)
    rows = []
    for m in [x for x in ma if x in mi and f"{x}|C2" in wa.columns]:
        f = lambda w, a, b: EXT.pacc(w[f"{m}|{a}"].to_numpy(float), w[f"{m}|{b}"].to_numpy(float))
        drop = lambda w: f(w, "C0", "P0") - f(w, "C2", "P2")
        lo, hi = EXT.boot_ci(wa, drop, n_boot)
        lo0, hi0 = EXT.boot_ci(wi, drop, n_boot)
        rows.append({"metric": m, "n": int(np.isfinite(wa[f"{m}|C2"]).sum()),
                     "Ctrl-0 (orig run)": f(wi, "C0", "P0"), "Ctrl-0 (alt run)": f(wa, "C0", "P0"),
                     "Ctrl-2 orig paraphraser": f(wi, "C2", "P2"), "Ctrl-2 alt paraphraser": f(wa, "C2", "P2"),
                     "Conf-P orig": f(wi, "C0", "P2"), "Conf-P alt": f(wa, "C0", "P2"),
                     "drop orig": drop(wi), "drop orig lo": lo0, "drop orig hi": hi0, "drop alt": drop(wa), "drop alt lo": lo, "drop alt hi": hi})
    A = pd.DataFrame(rows)
    out = NEW / "results/2_full_iualt/analysis"; out.mkdir(parents=True, exist_ok=True)
    A.to_csv(out / "alt_vs_orig.csv", index=False)
    log = pd.read_csv(NEW / "data/pairs/full_iualt_paraphrase_log.csv")
    acc = log.groupby(["report_id", "section", "sent_idx"]).accepted.any().mean()
    txt = [f"## A. S2 robustness: Llama-3.1-8B paraphraser + degree-word guard, {wa.target_id.nunique()} IU targets (context sentences with an accepted paraphrase: {100*acc:.1f}%)\n",
           md(A[["metric", "n", "Ctrl-0 (orig run)", "Ctrl-2 orig paraphraser", "Ctrl-2 alt paraphraser", "drop orig", "drop alt", "drop alt lo", "drop alt hi", "Conf-P orig", "Conf-P alt"]]), ""]
    (out / "ALT.md").write_text("\n".join(txt))
    return txt


def part_b():
    txt = ["## B. rubric vs rubric_unit (prompt states that unit conversion and abbreviation are benign)\n"]
    for c in ["iu", "mimic"]:
        jd = NEW / f"results/2_full_{c}/judges"
        pairs = pd.read_csv(NEW / f"data/pairs/full_{c}_all.csv")[["uid", "target_id", "cell", "edit_type", "subtype"]]
        rows = []
        for f in sorted(jd.glob("*__rubric_unit.csv")):
            tag = f.stem.replace("__rubric_unit", "")
            if not (jd / f"{tag}__rubric.csv").exists():
                continue
            for pr in ["rubric", "rubric_unit"]:
                j = pd.read_csv(jd / f"{tag}__{pr}.csv")
                d = pairs.merge(j, on="uid")
                d["chg"] = (d[f"{tag}__{pr}__label"].astype(str).str.upper() == "CHANGED").astype(float)
                d.loc[d[f"{tag}__{pr}__label"].isna(), "chg"] = np.nan
                rate = lambda q: float(d.query(q).chg.mean())
                w = d.pivot(index="target_id", columns="cell", values=f"{tag}__{pr}")
                pa = lambda a, b: EXT.pacc((w["identity"] - w[a]).to_numpy(float), (w["identity"] - w[b]).to_numpy(float))
                rows.append({"judge": tag, "prompt": pr,
                             "P0 meas (all)": rate("cell=='P0' and edit_type=='measurement'"),
                             "P0 meas:value": rate("cell=='P0' and edit_type=='measurement' and subtype=='value'"),
                             "C0 meas": rate("cell=='C0' and edit_type=='measurement'"),
                             "P0 all types": rate("cell=='P0'"), "P0 w/o meas": rate("cell=='P0' and edit_type!='measurement'"),
                             "C0 all types": rate("cell=='C0'"), "C2 all types": rate("cell=='C2'"),
                             "Ctrl-0": pa("C0", "P0"), "Ctrl-2": pa("C2", "P2")})
        if rows:
            G = pd.DataFrame(rows)
            G.to_csv(NEW / f"results/2_full_{c}/review1007/G_rubric_unit.csv", index=False)
            txt += [f"### {c}\n", md(G, 2), ""]
    return txt


def part_c():
    base = NEW / "results/2_full_rate3"
    if not (base / "scores").exists():
        return ["## C. RaTE-Eval task 3: no scores yet\n"]
    pairs = pd.read_csv(NEW / "data/pairs/full_rate3_all.csv")[["uid", "target_id", "cell"]]
    parts = []
    for d in ["scores", "judges"]:
        for f in sorted((base / d).glob("*.csv")):
            df = pd.read_csv(f)
            cols = [c for c in df.columns if c != "uid" and pd.api.types.is_numeric_dtype(df[c]) and not c.endswith(("__conf", "__label")) and not c.startswith("crimson_")]
            parts.append(df[["uid"] + cols].drop_duplicates("uid").set_index("uid"))
    S = pd.concat(parts, axis=1)
    df = pairs.merge(S, left_on="uid", right_index=True, how="left")
    rows = []
    for m in S.columns:
        w = df.pivot(index="target_id", columns="cell", values=m).astype(float)
        if m in EXT.ORIENT_LOWER_BETTER:
            w = -w
        # penalty relative to identity; the suite's own criterion (score of rewrite > score of opposite) is the same comparison
        W, T, L = wtl(w["identity"] - w["C0"], w["identity"] - w["P0"])
        rows.append({"metric": m, "n": int((w["C0"].notna() & w["P0"].notna()).sum()), "paired_acc": W + 0.5 * T, "win": W, "tie": T, "loss": L})
    C = pd.DataFrame(rows).sort_values("paired_acc")
    C.to_csv(NEW / "results/3_x3_audit/rate_eval_task3_metrics.csv", index=False)
    return ["## C. RaTE-Eval synthetic task: share of triplets where the opposite rewrite is penalised more than the synonym rewrite\n", md(C), ""]


if __name__ == "__main__":
    txt = ["# 10/7 review — follow-up analyses of the GPU experiments\n"] + part_a() + part_b() + part_c()
    (NEW / "results/REVIEW1007_FOLLOWUP.md").write_text("\n".join(txt))
    print("\n".join(txt))
