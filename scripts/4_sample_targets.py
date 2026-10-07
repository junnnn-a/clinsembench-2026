#!/usr/bin/env python
"""
4_sample_targets.py  — balanced target sampling (pilot / full) with a per-pattern cap.

  * n targets per (corpus, edit_type); split as evenly as possible over sections
  * no rewrite pattern may exceed `--pattern_cap` of a type (best effort: if the type has too
    few patterns to satisfy the cap, the cap is relaxed and this is reported)
  * one target per report per type (already guaranteed by the generator), and at most
    `--max_per_report` targets per report across types, so a report does not dominate
  * deterministic: hashlib-seeded

Writes  data/pairs/{tag}_{corpus}_targets.csv  and  data/pairs/{tag}_{corpus}_S0S1.csv
"""
from __future__ import annotations

import argparse
import hashlib
import random
from pathlib import Path

import pandas as pd

NEW = Path(__file__).resolve().parent.parent


def rng_for(*keys):
    return random.Random(int(hashlib.md5("|".join(map(str, keys)).encode()).hexdigest()[:12], 16))


def pick(g: pd.DataFrame, n: int, cap: float, rng: random.Random, report_load: dict, max_per_report: int):
    """greedy round-robin over patterns, respecting per-pattern cap, per-report load and
    shape balance (as many P_longer as C_longer targets; 'equal' shapes are unconstrained)."""
    n = min(n, len(g))
    cap_n = max(1, int(cap * n + 1e-9))
    by_pat = {p: gg.sample(frac=1.0, random_state=rng.randint(0, 10**9)).to_dict("records") for p, gg in g.groupby("pattern")}
    taken, counts = [], {p: 0 for p in by_pat}
    shape = {"P_longer": 0, "C_longer": 0, "equal": 0}
    relaxed = False

    def shape_ok(cand):
        s = cand.get("shape_sign", "equal")
        if s == "equal":
            return True
        other = "C_longer" if s == "P_longer" else "P_longer"
        return shape[s] <= shape[other]          # never let one direction lead by more than 1

    while len(taken) < n:
        progressed = False
        pats = sorted(by_pat, key=lambda p: (counts[p], rng.random()))
        for p in pats:
            if len(taken) >= n:
                break
            if counts[p] >= cap_n:
                continue
            skipped = []
            while by_pat[p]:
                cand = by_pat[p].pop()
                if report_load.get(cand["report_id"], 0) >= max_per_report:
                    continue
                if not shape_ok(cand):
                    skipped.append(cand)
                    continue
                taken.append(cand)
                counts[p] += 1
                shape[cand.get("shape_sign", "equal")] += 1
                report_load[cand["report_id"]] = report_load.get(cand["report_id"], 0) + 1
                progressed = True
                break
            by_pat[p] = skipped + by_pat[p]      # keep shape-deferred candidates for later rounds
        if not progressed:
            if all(counts[p] >= cap_n or not by_pat[p] for p in by_pat) and any(by_pat[p] for p in by_pat):
                cap_n += 1          # relax the cap
                relaxed = True
                continue
            break
    return pd.DataFrame(taken), relaxed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", nargs="+", default=["iu"])
    ap.add_argument("--n_per_type", type=int, default=40)
    ap.add_argument("--pattern_cap", type=float, default=0.15)
    ap.add_argument("--max_per_report", type=int, default=2)
    ap.add_argument("--tag", default="pilot")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--exclude_review", action="store_true", help="drop targets whose P lexicon needs expert review")
    args = ap.parse_args()

    for corpus in args.corpus:
        tg = pd.read_csv(NEW / f"data/pairs/{corpus}_targets.csv")
        pairs = pd.read_csv(NEW / f"data/pairs/{corpus}_factorial_S0S1.csv")
        if args.exclude_review:
            tg = tg[~tg.needs_expert_review]
        # laterality / anatomy / measurement flips inside a negated sentence ("No left pneumothorax") are weak
        # meaning changes: use asserted sentences only whenever the supply allows it.
        if "target_negated" in tg.columns:
            keep = []
            for (et, sec), g in tg.groupby(["edit_type", "section"]):
                if et in ("laterality", "anatomy", "measurement"):
                    pos = g[~g.target_negated]
                    need = args.n_per_type // tg.section.nunique()
                    g = pos if len(pos) >= need else pd.concat([pos, g[g.target_negated].head(need - len(pos))])
                keep.append(g)
            tg = pd.concat(keep, ignore_index=True)
        report_load: dict = {}
        parts, notes = [], []
        for etype, g in tg.groupby("edit_type"):
            rng = rng_for(args.seed, corpus, etype)
            secs = sorted(g.section.unique())
            per_sec = {s: args.n_per_type // len(secs) for s in secs}
            for s in secs[: args.n_per_type % len(secs)]:
                per_sec[s] += 1
            # if one section lacks supply, move quota to the other
            supply = g.section.value_counts().to_dict()
            for s in secs:
                short = per_sec[s] - supply.get(s, 0)
                if short > 0:
                    per_sec[s] -= short
                    for o in secs:
                        if o != s:
                            per_sec[o] += short
            chosen = []
            for s in secs:
                sel, relaxed = pick(g[g.section == s], per_sec[s], args.pattern_cap, rng, report_load, args.max_per_report)
                chosen.append(sel)
                if relaxed:
                    notes.append(f"{corpus}/{etype}/{s}: pattern cap {args.pattern_cap} relaxed (too few patterns)")
            sel = pd.concat(chosen, ignore_index=True)
            parts.append(sel)
        out = pd.concat(parts, ignore_index=True)
        cov = out.groupby(["edit_type", "section"]).agg(n=("target_id", "size"),
                                                          top_pattern_share=("pattern", lambda x: x.value_counts(normalize=True).iloc[0]),
                                                          n_patterns=("pattern", "nunique")).reset_index()
        out.to_csv(NEW / f"data/pairs/{args.tag}_{corpus}_targets.csv", index=False)
        sub = pairs[pairs.target_id.isin(set(out.target_id))]
        sub.to_csv(NEW / f"data/pairs/{args.tag}_{corpus}_S0S1.csv", index=False)
        print(f"[{args.tag}/{corpus}] targets={len(out)} rows={len(sub)} reports={out.report_id.nunique()}")
        print(cov.to_string(index=False))
        for n in notes:
            print("  note:", n)


if __name__ == "__main__":
    main()
