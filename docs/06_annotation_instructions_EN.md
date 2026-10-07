# Annotation instructions — meaning preservation between two report texts (v3, 2026-10-05)

## 1. Task
Each row of the spreadsheet has two short chest X-ray report sections:

- `reference_text`: the original section
- `candidate_text`: an edited version of the reference

Decide whether the candidate **states the same clinical content** as the reference and write `YES`, `NO` or `UNCERTAIN`
in the `meaning_preserved` column.

There are two files; the task is the same in both. Do **PART1 first**.

| File | Rows | Expected time |
|---|---|---|
| `..._PART1_BLINDED.xlsx` | 504 | 4–6 h |
| `..._PART2_BLINDED.xlsx` | 204 | 1.5–2 h |

Expect 30–40 s per row. You may split the work over several sittings.

## 2. Criteria

| Answer | When |
|---|---|
| **YES** | a radiologist reading the candidate would understand **exactly the same findings** as from the reference |
| **NO** | **at least one** statement differs in clinical content |
| **UNCERTAIN** | after careful reading you cannot decide because the two wordings can be read either way |

Differences that do **not** change meaning (→ YES): wording, word order and synonyms ("is seen" / "is identified");
abbreviations (LLL = left lower lobe); unit conversions that keep the quantity (2.5 cm = 25 mm); sentence order,
formatting, whole sentences rewritten in other words.

Differences that **do** change meaning (→ NO): presence vs absence of a finding; side (left/right); location (upper vs
lower lobe, base vs apex); severity or size (mild / moderate / severe, small / large); degree of certainty ("may represent"
vs "represents", "consistent with" vs "suspicious for"); a measurement (2.5 cm vs 5 cm, 2.5 cm vs 2.5 mm); comparison
with prior studies (unchanged vs increased, improved vs worsened).

## 3. Practice examples (not real items)

| reference | candidate | answer | reason |
|---|---|---|---|
| Small left pleural effusion. Heart size is normal. | Heart size is normal. Small left pleural effusion. | YES | |
| There is a 1.5 cm nodule in the right upper lobe. | There is a 15 mm nodule in the RUL. | YES | |
| No focal consolidation is seen. | Focal consolidation is not seen. | YES | |
| Small left pleural effusion. | Small right pleural effusion. | NO | left → right |
| Mild cardiomegaly, unchanged. | Mild cardiomegaly, increased. | NO | unchanged → increased |
| Opacity may represent atelectasis. | Opacity represents atelectasis. | NO | may represent → represents |
| There is a 1.5 cm nodule. | There is a 1.5 mm nodule. | NO | cm → mm |

## 4. Rules
1. Judge **only the relationship between the two texts**, not medical plausibility or writing quality.
2. Do not use UNCERTAIN because a sentence is awkward or ungrammatical; judge **what it says**.
3. `XXXX` and `___` are de-identification placeholders; ignore them.
4. **For every NO or UNCERTAIN, write the differing phrase in `reason`** (a few words, e.g. `left → right`). Leave it empty for YES.
5. The difference can be anywhere and sentences may be in a different order. **Read to the end.**
6. Work **alone**. Do not discuss items with anyone and do not use AI tools (ChatGPT etc.) or automatic diff tools.
   Looking up an unfamiliar term in a dictionary or by search is fine.
7. Write exactly one of `YES`, `NO`, `UNCERTAIN` (capitals). Do not add, delete or sort rows; do not edit
   `annotation_id` or the two text columns.

## 5. Returning the file
- Replace `BLINDED` with `filled` in the file names (e.g. `annotator_A_PART1_filled.xlsx`, `annotator_A_PART2_filled.xlsx`) and send them back.
- Check that every row has an answer and that NO / UNCERTAIN rows have a reason.
- You may send PART1 as soon as it is finished, without waiting for PART2.
- Please also tell us roughly how long the work took.
