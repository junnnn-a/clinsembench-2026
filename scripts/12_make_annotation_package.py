#!/usr/bin/env python
"""
12_make_annotation_package.py — X5 human-validation package (IU X-Ray only, so that text + labels can be released).

A. Graduate annotators (2 people, FULL double annotation, blinded to cell / type / rule label):
     n_per_stratum pairs for each (edit_type, cell) with cell in {P0, P1, P2, C0, C1, C2}; a different target
     for every pair (no reference is shown twice), deterministic sampling.
     -> annotator_{A,B}_BLINDED.csv/.xlsx (independently shuffled), KEY_DO_NOT_SEND.csv
B. Radiologist:
     B1 lexicon_review.csv     one row per meaning-preserving substitution pattern (+2 examples, + the matched C)
                               columns to fill: equivalent? (YES/NO/DEPENDS), comment
     B2 clinical_importance.csv one row per edit type x subtype with an example; fill: importance 1-5
     B3 radiologist_pairs_BLINDED.csv  pair-level meaning judgment, P cells emphasised
                               (per type: P0 x10, P2 x10, C0 x5) -> ~175 pairs, disjoint from A
C. INSTRUCTIONS_{EN,KR}.md

v1 problems fixed: no singly-annotated items, explicit UNCERTAIN criterion, mandatory reason for NO/UNCERTAIN,
hashlib-seeded sampling (v1 used Python hash()).
"""
from __future__ import annotations

import argparse
import hashlib
import random
from pathlib import Path

import pandas as pd

NEW = Path(__file__).resolve().parent.parent
CELLS = ["P0", "P1", "P2", "C0", "C1", "C2"]


def rng_for(*keys):
    return random.Random(int(hashlib.md5("|".join(map(str, keys)).encode()).hexdigest()[:12], 16))


def blinded(df, seed_key):
    d = df.sample(frac=1.0, random_state=rng_for(seed_key).randint(0, 10**9)).reset_index(drop=True)
    return pd.DataFrame({"annotation_id": d.annotation_id, "reference_text": d.reference, "candidate_text": d.candidate,
                         "meaning_preserved (YES/NO/UNCERTAIN)": "", "reason (required if NO or UNCERTAIN)": ""})


def save(df, path):
    df.to_csv(path.with_suffix(".csv"), index=False, encoding="utf-8-sig")
    try:
        df.to_excel(path.with_suffix(".xlsx"), index=False)
    except Exception as e:  # openpyxl missing
        print(f"  (xlsx skipped: {e})")


INSTR_EN = """# Annotation instructions — meaning preservation between two report texts

You will see pairs of short chest X-ray report sections: a **reference** and a **candidate**.
The candidate was produced by editing the reference. Decide whether the candidate **states the same clinical
content** as the reference.

Answer in the column `meaning_preserved`:

- **YES** — a radiologist reading the candidate would understand exactly the same findings as from the reference.
  Differences in wording, synonyms, abbreviations (e.g. LLL = left lower lobe), unit conversions that keep the
  same quantity (2.5 cm = 25 mm), sentence order or formatting do **not** change meaning.
- **NO** — at least one statement differs in clinical content: a finding is present in one and absent/negated in
  the other; a different side (left/right) or location; a different severity or size; a different degree of
  certainty (e.g. "may represent" vs "represents"); a different measurement; a different comparison with prior
  studies (e.g. "unchanged" vs "increased").
- **UNCERTAIN** — use this only if, after careful reading, you cannot decide because the two wordings could be
  read either way (for example two hedging expressions whose strength you cannot rank). Do **not** use UNCERTAIN
  for texts that are merely awkward or ungrammatical: judge what they say.

Rules
1. Judge only the relationship between the two texts. Do not judge whether the report is medically plausible or
   correct for a patient, and do not judge writing quality.
2. Tokens such as `XXXX` or `___` are de-identification placeholders; ignore them.
3. For every **NO** or **UNCERTAIN**, write in `reason` the phrase that differs (a few words are enough).
4. Work independently. Do not discuss items with the other annotator. Do not use AI tools.
5. Compare the whole section: differences can be anywhere, and the sentences may be in a different order.
"""

INSTR_KR = """# 어노테이션 지침 — 두 판독문 텍스트의 의미 보존 여부

짧은 흉부 X선 판독문 섹션 쌍(**reference**, **candidate**)이 주어집니다. candidate는 reference를 편집해 만든 것입니다.
candidate가 reference와 **같은 임상 내용**을 말하는지 판단해 주세요.

`meaning_preserved` 열에 다음 중 하나를 적습니다.

- **YES** — candidate를 읽은 영상의학과 의사가 reference와 정확히 같은 소견으로 이해한다.
  표현·동의어·약어(예: LLL = left lower lobe)·같은 양을 유지하는 단위 변환(2.5 cm = 25 mm)·문장 순서·서식의 차이는
  의미를 바꾸지 **않습니다**.
- **NO** — 임상 내용이 하나라도 다르다: 소견의 유무(부정), 좌우, 위치, 정도·크기, 확신의 정도
  (예: "may represent" vs "represents"), 측정값, 이전 검사와의 비교(예: "unchanged" vs "increased").
- **UNCERTAIN** — 주의 깊게 읽고도 두 표현이 어느 쪽으로도 읽혀 결정할 수 없을 때만 사용합니다
  (예: 강도를 비교하기 어려운 두 hedge 표현). 단지 어색하거나 비문이라는 이유로 UNCERTAIN을 쓰지 마세요.
  그 문장이 말하는 내용을 기준으로 판단합니다.

규칙
1. 두 텍스트 사이의 관계만 판단합니다. 의학적 타당성, 환자에 대한 정확성, 글의 품질은 판단하지 않습니다.
2. `XXXX`, `___`는 비식별 처리 토큰이므로 무시합니다.
3. **NO**와 **UNCERTAIN**에는 `reason` 열에 달라진 구절을 반드시 적습니다 (몇 단어면 충분).
4. 독립적으로 작업합니다. 다른 annotator와 상의하지 않고, AI 도구를 사용하지 않습니다.
5. 섹션 전체를 비교합니다. 차이는 어디에나 있을 수 있고 문장 순서가 다를 수 있습니다.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", default=str(NEW / "data/pairs/full_iu_all.csv"))
    ap.add_argument("--targets", default=str(NEW / "data/pairs/full_iu_targets.csv"))
    ap.add_argument("--out", default=str(NEW / "data/annotation"))
    ap.add_argument("--n_per_stratum", type=int, default=12)
    ap.add_argument("--seed", type=int, default=2026)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    pairs = pd.read_csv(args.pairs)
    tg = pd.read_csv(args.targets)
    pairs = pairs[pairs.cell != "identity"]

    # ---------- A. graduate annotators: distinct target per pair
    used, rows = set(), []
    for et in sorted(tg.edit_type.unique()):
        ids = tg[tg.edit_type == et].target_id.tolist()
        rng_for(args.seed, "A", et).shuffle(ids)
        k = 0
        for cell in CELLS:
            take = ids[k:k + args.n_per_stratum]
            k += args.n_per_stratum
            used.update(take)
            rows.append(pairs[pairs.target_id.isin(take) & (pairs.cell == cell)])
    A = pd.concat(rows, ignore_index=True)
    A = A.sample(frac=1.0, random_state=args.seed).reset_index(drop=True)
    A["annotation_id"] = [f"G{i:04d}" for i in range(len(A))]
    key_cols = ["annotation_id", "uid", "target_id", "report_id", "section", "edit_type", "subtype", "pattern", "edit_detail",
                "cell", "is_changed", "needs_expert_review", "reference", "candidate"]
    A[key_cols].to_csv(out / "grad_KEY_DO_NOT_SEND.csv", index=False)
    for name in ["A", "B"]:
        save(blinded(A, f"{args.seed}-{name}"), out / f"annotator_{name}_BLINDED")
    print(f"[grad] {len(A)} pairs  ({A.groupby(['edit_type','cell']).size().min()}–{A.groupby(['edit_type','cell']).size().max()} per stratum)")

    # ---------- B3. radiologist pair-level (disjoint targets), P cells emphasised
    rows = []
    for et in sorted(tg.edit_type.unique()):
        ids = [t for t in tg[tg.edit_type == et].target_id.tolist() if t not in used]
        rng_for(args.seed, "R", et).shuffle(ids)
        k = 0
        for cell, n in [("P0", 10), ("P2", 10), ("C0", 5)]:
            take = ids[k:k + n]; k += n
            rows.append(pairs[pairs.target_id.isin(take) & (pairs.cell == cell)])
    R = pd.concat(rows, ignore_index=True).sample(frac=1.0, random_state=args.seed + 1).reset_index(drop=True)
    R["annotation_id"] = [f"R{i:04d}" for i in range(len(R))]
    R[key_cols].to_csv(out / "radiologist_KEY_DO_NOT_SEND.csv", index=False)
    save(blinded(R, f"{args.seed}-R"), out / "radiologist_pairs_BLINDED")
    print(f"[radiologist pairs] {len(R)}")

    # ---------- B1. lexicon review: one row per P-substitution pattern
    def sub_of(r):
        # show only the differing part for compact review
        import difflib
        a, p, c = r.target_sent.split(), r.p_sent.split(), r.c_sent.split()
        def diff(x, y):
            sm = difflib.SequenceMatcher(a=x, b=y, autojunk=False)
            o = [(" ".join(x[i1:i2]), " ".join(y[j1:j2])) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != "equal"]
            return " ; ".join(f"[{s}] -> [{d}]" for s, d in o)
        return diff(a, p), diff(a, c)
    tg[["p_edit", "c_edit"]] = tg.apply(lambda r: pd.Series(sub_of(r)), axis=1)
    # normalise the P edit to a lexicon key (lower-case)
    norm_edit = tg.p_edit.str.lower().str.replace(r"[.,;:]", "", regex=True).str.replace(r"\b(left|right)\b", "<side>", regex=True)
    tg["lex_key"] = tg.edit_type + " | " + tg.pattern + " | " + norm_edit
    # negation/measurement edits depend on the sentence -> group by pattern only
    tg.loc[tg.edit_type.isin(["negation", "measurement"]), "lex_key"] = tg.edit_type + " | " + tg.pattern
    lex = []
    for key, g in tg.groupby("lex_key"):
        ex = g.sample(n=min(2, len(g)), random_state=args.seed)
        row = {"lexicon_id": "", "edit_type": g.edit_type.iloc[0], "pattern": g.pattern.iloc[0], "n_targets": len(g),
               "flagged_by_us": bool(g.needs_expert_review.any()),
               "P_substitution (should preserve meaning)": g.p_edit.iloc[0] if g.edit_type.iloc[0] not in ("negation", "measurement") else "(see examples)"}
        for i, (_, e) in enumerate(ex.iterrows(), 1):
            row[f"example{i}_original"] = e.target_sent
            row[f"example{i}_P"] = e.p_sent
            row[f"example{i}_C (meaning-changing counterpart)"] = e.c_sent
        row["equivalent? (YES/NO/DEPENDS)"] = ""
        row["comment"] = ""
        lex.append(row)
    L = pd.DataFrame(lex).sort_values(["edit_type", "n_targets"], ascending=[True, False]).reset_index(drop=True)
    L["lexicon_id"] = [f"L{i:03d}" for i in range(len(L))]
    save(L, out / "radiologist_lexicon_review")
    print(f"[lexicon] {len(L)} patterns")

    # ---------- B2. clinical importance per type x subtype
    imp = []
    for (et, st), g in tg.groupby(["edit_type", "subtype"]):
        e = g.sample(n=1, random_state=args.seed).iloc[0]
        imp.append({"edit_type": et, "subtype": st, "n_targets": len(g), "example_original": e.target_sent, "example_changed": e.c_sent,
                    "clinical importance of this kind of error (1=negligible ... 5=could change management)": "", "comment": ""})
    I = pd.DataFrame(imp)
    save(I, out / "radiologist_clinical_importance")
    print(f"[importance] {len(I)} rows")

    (out / "INSTRUCTIONS_EN.md").write_text(INSTR_EN)
    (out / "INSTRUCTIONS_KR.md").write_text(INSTR_KR)
    print("[wrote]", out)


if __name__ == "__main__":
    main()
