#!/usr/bin/env python
"""
19_make_supplementary_annotation.py — annotation PART 2 (lexicon-coverage set) for the two graduate annotators.

Why: no radiologist is available for this (conference) version, so the meaning-preserving substitution lexicon
cannot be approved by an expert. Instead every substitution pattern is judged at pair level by both annotators:

  * for each of the 61 P-substitution patterns: up to 3 targets not used in PART 1, shown as their P0 cell
    (reference vs reference-with-the-substitution only) -> isolates the substitution itself
  * plus C0 cells from other unused targets (10 per edit type) so that the sheet is not all "YES"

Same blinded format, same instructions, independently shuffled for A and B.  IDs S0000...
Pre-registered use (docs/11 §6): a pattern is KEPT if the pooled YES rate over all its P0 judgments
(PART 1 + PART 2, both annotators) is >= 0.75 with at least 4 judgments; otherwise its targets are removed
from the "validated" analysis set. Patterns with < 4 judgments are reported as unvalidated.

Output: data/annotation/annotator_{A,B}_PART2_BLINDED.{xlsx,csv}, part2_KEY_DO_NOT_SEND.csv
Run: envs/llm/bin/python scripts/19_make_supplementary_annotation.py
"""
from __future__ import annotations

import difflib
import hashlib
import random
from pathlib import Path

import pandas as pd

NEW = Path(__file__).resolve().parent.parent
OUT = NEW / "data/annotation"
SEED = 2026


def rng_for(*keys):
    return random.Random(int(hashlib.md5("|".join(map(str, keys)).encode()).hexdigest()[:12], 16))


def lex_keys(tg):
    def pe(r):
        a, p = r.target_sent.split(), r.p_sent.split()
        sm = difflib.SequenceMatcher(a=a, b=p, autojunk=False)
        return " ; ".join(f"[{' '.join(a[i1:i2])}] -> [{' '.join(p[j1:j2])}]" for t, i1, i2, j1, j2 in sm.get_opcodes() if t != "equal")
    tg = tg.copy()
    tg["p_edit"] = tg.apply(pe, axis=1)
    ne = tg.p_edit.str.lower().str.replace(r"[.,;:]", "", regex=True).str.replace(r"\b(left|right)\b", "<side>", regex=True)
    tg["lex_key"] = tg.edit_type + " | " + tg.pattern + " | " + ne
    m = tg.edit_type.isin(["negation", "measurement"])
    tg.loc[m, "lex_key"] = tg.edit_type[m] + " | " + tg.pattern[m]
    return tg


def blinded(df, key):
    d = df.sample(frac=1.0, random_state=rng_for(key).randint(0, 10**9)).reset_index(drop=True)
    return pd.DataFrame({"annotation_id": d.annotation_id, "reference_text": d.reference, "candidate_text": d.candidate,
                         "meaning_preserved (YES/NO/UNCERTAIN)": "", "reason (required if NO or UNCERTAIN)": ""})


def main():
    tg = lex_keys(pd.read_csv(NEW / "data/pairs/full_iu_targets.csv"))
    pairs = pd.read_csv(NEW / "data/pairs/full_iu_all.csv")
    used = set(pd.read_csv(OUT / "grad_KEY_DO_NOT_SEND.csv").target_id)
    free = tg[~tg.target_id.isin(used)]
    p_ids = []
    for key, g in free.groupby("lex_key"):
        ids = sorted(g.target_id)
        rng_for(SEED, "P", key).shuffle(ids)
        p_ids += ids[:3]
    rest = free[~free.target_id.isin(p_ids)]
    c_ids = []
    for et, g in rest.groupby("edit_type"):
        ids = sorted(g.target_id)
        rng_for(SEED, "C", et).shuffle(ids)
        c_ids += ids[:10]
    S = pd.concat([pairs[pairs.target_id.isin(p_ids) & (pairs.cell == "P0")], pairs[pairs.target_id.isin(c_ids) & (pairs.cell == "C0")]], ignore_index=True)
    S = S.merge(tg[["target_id", "lex_key"]], on="target_id", how="left")
    S = S.sample(frac=1.0, random_state=SEED).reset_index(drop=True)
    S["annotation_id"] = [f"S{i:04d}" for i in range(len(S))]
    S[["annotation_id", "uid", "target_id", "report_id", "section", "edit_type", "subtype", "pattern", "lex_key", "edit_detail",
       "cell", "is_changed", "needs_expert_review", "reference", "candidate"]].to_csv(OUT / "part2_KEY_DO_NOT_SEND.csv", index=False)
    for n in ["A", "B"]:
        b = blinded(S, f"{SEED}-part2-{n}")
        b.to_csv(OUT / f"annotator_{n}_PART2_BLINDED.csv", index=False, encoding="utf-8-sig")
        b.to_excel(OUT / f"annotator_{n}_PART2_BLINDED.xlsx", index=False)
    # coverage report: P0 judgments per pattern over PART 1 + PART 2 (per annotator)
    k1 = pd.read_csv(OUT / "grad_KEY_DO_NOT_SEND.csv").merge(tg[["target_id", "lex_key"]], on="target_id")
    cov = pd.concat([k1[k1.cell == "P0"], S[S.cell == "P0"]]).groupby("lex_key").size().reindex(tg.lex_key.unique(), fill_value=0)
    print(f"[part2] pairs={len(S)}  P0={int((S.cell=='P0').sum())}  C0={int((S.cell=='C0').sum())}")
    print(f"  patterns={len(cov)}  with >=2 P0 pairs (=>4 judgments from 2 annotators): {(cov>=2).sum()}  with 0: {(cov==0).sum()}")
    print("  uncovered / thin patterns:", cov[cov < 2].to_dict())


if __name__ == "__main__":
    main()
