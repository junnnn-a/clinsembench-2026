#!/usr/bin/env python
"""
14_extended_analysis.py — analyses that go beyond the main table (docs/9).

  A. subtype breakdown        paired accuracy by edit_type x subtype (severity adjacent/extreme, measurement
                              value/unit, negation direction, uncertainty direction) in controlled S0 and S2
  B. surface dose-response    S2 targets binned by how much of the context was rewritten (token edit fraction
                              reference -> P2): mean standardised penalty of P2 and paired accuracy C2 vs P2 per bin
  C. key contrasts            cluster-bootstrap CIs for (i) paired acc S0 - S2, (ii) paired acc - Jaccard paired acc
                              (does the metric beat the meaning-blind baseline?), per metric
  D. mixed-effects model      z(D) ~ meaning * surface + (1 | report)   (statsmodels MixedLM), per metric
  E. CRIMSON error attribution (E8)  which CRIMSON error category fires for each edit type in C0 / P0

Run:  envs/llm/bin/python scripts/14_extended_analysis.py --corpus iu mimic
Outputs: results/2_full_{corpus}/extended/*.csv + EXTENDED.md
"""
from __future__ import annotations

import argparse
import difflib
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

NEW = Path(__file__).resolve().parent.parent
ORIENT_LOWER_BETTER = {"radcliq"}
CRIMSON_CATS = ["false_findings", "missing_findings", "location_errors", "severity_errors", "descriptor_errors",
                "measurement_errors", "certainty_errors", "unspecific_errors", "overinterpretation_errors", "temporal_errors"]
EXPECTED = {"laterality": ["location_errors"], "anatomy": ["location_errors"], "severity": ["severity_errors"],
            "measurement": ["measurement_errors"], "uncertainty": ["certainty_errors"], "temporal": ["temporal_errors"],
            "negation": ["false_findings", "missing_findings"]}


def md(df, f=3):
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.{f}f}")
    cols = [str(c) for c in d.columns]
    return "\n".join(["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"] +
                     ["| " + " | ".join(map(str, r)) + " |" for r in d.itertuples(index=False)])


def load(corpus):
    base = NEW / f"results/2_full_{corpus}"
    pairs = pd.read_csv(NEW / f"data/pairs/full_{corpus}_all.csv")
    parts = []
    for d in ["scores", "judges"]:
        for f in sorted((base / d).glob("*.csv")):
            df = pd.read_csv(f)
            cols = [c for c in df.columns if c != "uid" and pd.api.types.is_numeric_dtype(df[c])
                    and not c.endswith(("__conf", "__label")) and not c.startswith("crimson_")]
            parts.append(df[["uid"] + cols].drop_duplicates("uid").set_index("uid"))
    S = pd.concat(parts, axis=1)
    metrics = list(S.columns)
    df = pairs.merge(S, left_on="uid", right_index=True, how="left")
    for m in metrics:
        if m in ORIENT_LOWER_BETTER:
            df[m] = -df[m]
    idn = df[df.cell == "identity"].set_index("target_id")[metrics]
    cand = df[df.cell != "identity"].copy()
    for m in metrics:
        cand[m] = cand.target_id.map(idn[m]) - cand[m]          # penalty D
    return pairs, cand, metrics


def wide(cand, metrics):
    w = cand.pivot_table(index=["target_id", "report_id", "edit_type", "subtype"], columns="cell", values=metrics)
    w.columns = [f"{m}|{c}" for m, c in w.columns]
    return w.reset_index()


def pacc(a, b):
    d = a - b
    ok = np.isfinite(d)
    d = d[ok]
    return float(np.mean((d > 0) + 0.5 * (d == 0))) if len(d) else np.nan


def boot_ci(w, fn, n_boot, seed=0):
    rng = np.random.default_rng(seed)
    groups = [g.index.to_numpy() for _, g in w.groupby("report_id")]
    vals = []
    for _ in range(n_boot):
        idx = np.concatenate([groups[i] for i in rng.integers(0, len(groups), len(groups))])
        vals.append(fn(w.loc[idx]))
    return float(np.nanpercentile(vals, 2.5)), float(np.nanpercentile(vals, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", nargs="+", default=["iu", "mimic"])
    ap.add_argument("--n_boot", type=int, default=1000)
    ap.add_argument("--reuse_contrasts", action="store_true")
    args = ap.parse_args()
    for corpus in args.corpus:
        out = NEW / f"results/2_full_{corpus}/extended"
        out.mkdir(parents=True, exist_ok=True)
        pairs, cand, metrics = load(corpus)
        w = wide(cand, metrics).reset_index(drop=True)
        rep = [f"# Extended analysis — {corpus}\n"]

        # ---------------- A. subtypes
        rows = []
        for (et, st), g in w.groupby(["edit_type", "subtype"]):
            for m in metrics:
                r = {"edit_type": et, "subtype": st, "n": len(g), "metric": m}
                for cond, (c, p) in {"S0": ("C0", "P0"), "S2": ("C2", "P2")}.items():
                    r[f"paired_acc_{cond}"] = pacc(g[f"{m}|{c}"].to_numpy(float), g[f"{m}|{p}"].to_numpy(float))
                rows.append(r)
        A = pd.DataFrame(rows)
        A.to_csv(out / "A_subtypes.csv", index=False)
        for et in ["severity", "measurement", "negation", "uncertainty"]:
            s = A[A.edit_type == et]
            rep += [f"## A. {et}: controlled S0 paired accuracy by subtype\n",
                    md(s.pivot(index="metric", columns="subtype", values="paired_acc_S0").reset_index()), ""]

        # ---------------- B. surface dose-response in S2
        p2 = pairs[pairs.cell == "P2"].copy()
        def frac(r):
            a, b = str(r.reference).split(), str(r.candidate).split()
            sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
            e = sum(max(i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != "equal")
            return e / max(1, len(a))
        p2["edit_frac"] = p2.apply(frac, axis=1)
        w = w.merge(p2[["target_id", "edit_frac"]], on="target_id", how="left")
        w["surface_bin"] = pd.qcut(w.edit_frac, 4, labels=["Q1 (least rewritten)", "Q2", "Q3", "Q4 (most rewritten)"])
        rows = []
        for b, g in w.groupby("surface_bin", observed=True):
            for m in metrics:
                sd = np.nanstd(cand[m].to_numpy(float)) or 1.0
                rows.append({"surface_bin": b, "edit_frac_mean": g.edit_frac.mean(), "n": len(g), "metric": m,
                             "P2_penalty_z": float(np.nanmean(g[f"{m}|P2"] - g[f"{m}|P0"])) / sd,
                             "paired_acc_C2_vs_P2": pacc(g[f"{m}|C2"].to_numpy(float), g[f"{m}|P2"].to_numpy(float)),
                             "paired_acc_C0_vs_P2": pacc(g[f"{m}|C0"].to_numpy(float), g[f"{m}|P2"].to_numpy(float))})
        B = pd.DataFrame(rows)
        B.to_csv(out / "B_surface_dose_response.csv", index=False)
        rep += ["## B. Surface dose-response (S2): extra penalty on the meaning-preserving candidate, z(D(P2) - D(P0)), by amount rewritten\n",
                md(B.pivot(index="metric", columns="surface_bin", values="P2_penalty_z").reset_index(), 2), "",
                "### paired accuracy C2 vs P2 by amount rewritten\n",
                md(B.pivot(index="metric", columns="surface_bin", values="paired_acc_C2_vs_P2").reset_index()), ""]

        # ---------------- C. contrasts
        rows = []
        base = "jaccard"
        cached = out / "C_contrasts.csv"
        for m in ([] if (args.reuse_contrasts and cached.exists()) else metrics):
            f_s0 = lambda d, m=m: pacc(d[f"{m}|C0"].to_numpy(float), d[f"{m}|P0"].to_numpy(float))
            f_s2 = lambda d, m=m: pacc(d[f"{m}|C2"].to_numpy(float), d[f"{m}|P2"].to_numpy(float))
            f_drop = lambda d: f_s0(d) - f_s2(d)
            f_vs = lambda d, m=m: f_s0(d) - pacc(d[f"{base}|C0"].to_numpy(float), d[f"{base}|P0"].to_numpy(float))
            f_vs2 = lambda d, m=m: f_s2(d) - pacc(d[f"{base}|C2"].to_numpy(float), d[f"{base}|P2"].to_numpy(float))
            lo, hi = boot_ci(w, f_drop, args.n_boot)
            lo2, hi2 = boot_ci(w, f_vs, args.n_boot)
            lo3, hi3 = boot_ci(w, f_vs2, args.n_boot)
            rows.append({"metric": m, "S0": f_s0(w), "S2": f_s2(w), "S0_minus_S2": f_drop(w), "drop_lo": lo, "drop_hi": hi,
                         "S0_minus_jaccard": f_vs(w), "vsJ_lo": lo2, "vsJ_hi": hi2,
                         "S2_minus_jaccard": f_vs2(w), "vsJ2_lo": lo3, "vsJ2_hi": hi3})
        CT = pd.read_csv(cached) if (args.reuse_contrasts and cached.exists()) else pd.DataFrame(rows)          # NB: must not be called `C` — patsy resolves C(...) in this namespace
        CT["beats_blind_baseline_S0"] = CT.vsJ_lo > 0
        CT["degrades_under_paraphrase"] = CT.drop_lo > 0
        CT.to_csv(out / "C_contrasts.csv", index=False)
        rep += ["## C. Contrasts (report-cluster bootstrap 95% CI)\n", md(CT), ""]

        # ---------------- D. mixed-effects
        try:
            import statsmodels.formula.api as smf
            rows = []
            long = cand[cand.cell.isin(["P0", "C0", "P1", "C1", "P2", "C2"])].copy()
            long["meaning"] = long.cell.str[0].map({"P": 0, "C": 1})
            long["surface"] = long.cell.str[1].map({"0": "S0", "1": "S1", "2": "S2"})
            for m in metrics:
                d = long[["report_id", "meaning", "surface", m]].dropna().copy()
                sd = d[m].std() or 1.0
                d["z"] = (d[m] - d[m].mean()) / sd
                model = "mixedlm"
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    try:
                        fit = smf.mixedlm("z ~ meaning * C(surface)", d, groups=d["report_id"]).fit(reml=False, method="lbfgs")
                        _ = fit.conf_int()
                    except Exception:      # singular random-effects fit (e.g. metrics that are constant within report)
                        model = "ols_cluster_robust"
                        fit = smf.ols("z ~ meaning * C(surface)", d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["report_id"])[0]})
                ci = fit.conf_int()
                for name in ["meaning", "C(surface)[T.S1]", "C(surface)[T.S2]", "meaning:C(surface)[T.S1]", "meaning:C(surface)[T.S2]"]:
                    rows.append({"metric": m, "model": model, "term": name, "coef": fit.params[name], "ci_lo": ci.loc[name, 0], "ci_hi": ci.loc[name, 1], "p": fit.pvalues[name]})
            D = pd.DataFrame(rows)
            D.to_csv(out / "D_mixed_effects.csv", index=False)
            rep += ["## D. Mixed-effects coefficients (z-scored penalty; random intercept per report)\n",
                    md(D.pivot(index="metric", columns="term", values="coef").reset_index()), ""]
        except ImportError:
            rep += ["## D. (statsmodels not installed — skipped)\n"]

        # ---------------- E. CRIMSON attribution
        cf = NEW / f"results/2_full_{corpus}/scores/crimson.csv"
        if cf.exists():
            cr = pd.read_csv(cf)
            cols = [f"crimson_{c}" for c in CRIMSON_CATS if f"crimson_{c}" in cr.columns]
            d = pairs.merge(cr[["uid"] + cols], on="uid")
            rows = []
            for cell in ["P0", "C0", "P2", "C2"]:
                s = d[d.cell == cell]
                for et, g in s.groupby("edit_type"):
                    r = {"cell": cell, "edit_type": et, "n": len(g), "any_error": float((g[cols].sum(axis=1) > 0).mean())}
                    exp = [f"crimson_{c}" for c in EXPECTED[et] if f"crimson_{c}" in cols]
                    r["expected_category_fired"] = float((g[exp].sum(axis=1) > 0).mean())
                    r["only_other_category"] = float(((g[cols].sum(axis=1) > 0) & (g[exp].sum(axis=1) == 0)).mean())
                    for c in cols:
                        r[c.replace("crimson_", "")] = float((g[c] > 0).mean())
                    rows.append(r)
            E = pd.DataFrame(rows)
            E.to_csv(out / "E_crimson_attribution.csv", index=False)
            show = ["cell", "edit_type", "n", "any_error", "expected_category_fired", "only_other_category"]
            rep += ["## E. CRIMSON error attribution — share of candidates with >=1 error (any / expected category / only other categories)\n",
                    md(E[E.cell.isin(["C0", "P0"])][show]), "",
                    "### C0: which category fires (share of candidates)\n",
                    md(E[E.cell == "C0"][["edit_type"] + [c.replace("crimson_", "") for c in cols]], 2), ""]
        # ---------------- F. robustness to known defects / pending expert review
        tg = pd.read_csv(NEW / f"data/pairs/full_{corpus}_targets.csv")
        awkward = tg[(tg.edit_type == "negation") & tg.pattern.str.startswith("N3") &
                     tg.target_sent.str.contains(r"\b(?:identified|seen|noted|present|visualized|detected|appreciated|demonstrated|evident)\.?$", regex=True)].target_id
        subsets = {
            "all targets": set(tg.target_id),
            "excl. measurement:unit (P edit larger than C)": set(tg[~((tg.edit_type == "measurement") & (tg.subtype == "unit"))].target_id),
            "excl. awkward negation fragments": set(tg.target_id) - set(awkward),
            "excl. P lexicon pending expert review": set(tg[~tg.needs_expert_review].target_id),
            "excl. all three": set(tg[~tg.needs_expert_review & ~((tg.edit_type == "measurement") & (tg.subtype == "unit"))].target_id) - set(awkward),
        }
        rows = []
        for name, ids in subsets.items():
            g = w[w.target_id.isin(ids)]
            for m in metrics:
                rows.append({"subset": name, "n": len(g), "metric": m,
                             "S0": pacc(g[f"{m}|C0"].to_numpy(float), g[f"{m}|P0"].to_numpy(float)),
                             "S2": pacc(g[f"{m}|C2"].to_numpy(float), g[f"{m}|P2"].to_numpy(float)),
                             "confound_v1": pacc(g[f"{m}|C0"].to_numpy(float), g[f"{m}|P1"].to_numpy(float)),
                             "confound_reevalmed": pacc(g[f"{m}|C0"].to_numpy(float), g[f"{m}|P2"].to_numpy(float))})
        Fd = pd.DataFrame(rows)
        Fd.to_csv(out / "F_robustness_subsets.csv", index=False)
        rep += ["## F. Robustness: controlled S0 paired accuracy on target subsets\n",
                md(Fd.assign(subset=Fd.subset + " (n=" + Fd.n.astype(str) + ")").pivot(index="metric", columns="subset", values="S0").reset_index()), ""]
        (out / "EXTENDED.md").write_text("\n".join(rep))
        print(f"[{corpus}] wrote {out}/EXTENDED.md")


if __name__ == "__main__":
    main()
