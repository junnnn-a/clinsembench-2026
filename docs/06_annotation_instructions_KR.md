# 어노테이션 지침 — 두 판독문 텍스트의 의미 보존 여부 (v3, 2026-10-05)

## 1. 무엇을 하는 작업인가
엑셀 파일의 각 행에 짧은 흉부 X선 판독문 섹션 두 개가 있습니다.

- `reference_text`: 원래 판독문
- `candidate_text`: reference를 조금 고친 판독문

**candidate가 reference와 같은 임상 내용을 말하는지** 판단해서 `meaning_preserved` 열에 `YES` / `NO` / `UNCERTAIN` 중 하나를 적습니다.

파일은 두 개입니다. 작업 방법은 같습니다.

| 파일 | 행 수 | 예상 시간 |
|---|---|---|
| `..._PART1_BLINDED.xlsx` | 504 | 4–6시간 |
| `..._PART2_BLINDED.xlsx` | 204 | 1.5–2시간 |

**PART1을 먼저** 끝내고 PART2를 해 주세요. 한 행에 30–40초 정도이고, 여러 번에 나눠서 하셔도 됩니다.

## 2. 판단 기준

| 답 | 언제 |
|---|---|
| **YES** | candidate를 읽은 영상의학과 의사가 reference와 **정확히 같은 소견**으로 이해한다 |
| **NO** | 임상 내용이 **하나라도** 다르다 |
| **UNCERTAIN** | 주의 깊게 읽고도 두 표현이 어느 쪽으로도 읽혀서 결정할 수 없다 |

의미를 **바꾸지 않는** 차이 (→ YES)
- 표현·어순·동의어: "is seen" ↔ "is identified"
- 약어: LLL = left lower lobe, RUL = right upper lobe
- 같은 양을 유지하는 단위 변환: 2.5 cm = 25 mm
- 문장 순서, 서식, 문장 전체를 다른 말로 다시 쓴 것

의미를 **바꾸는** 차이 (→ NO)
- 소견의 유무: "No pneumothorax" ↔ "Pneumothorax is present"
- 좌우: left ↔ right
- 위치: upper lobe ↔ lower lobe, base ↔ apex
- 정도·크기: mild ↔ moderate ↔ severe, small ↔ large
- 확신의 정도: "may represent" ↔ "represents", "consistent with" ↔ "suspicious for"
- 측정값: 2.5 cm ↔ 5 cm, 2.5 cm ↔ 2.5 mm
- 이전 검사와의 비교: unchanged ↔ increased, improved ↔ worsened

## 3. 예시 (실제 문항이 아닌 연습용)

| reference | candidate | 답 | reason |
|---|---|---|---|
| Small left pleural effusion. Heart size is normal. | Heart size is normal. Small left pleural effusion. | YES | |
| There is a 1.5 cm nodule in the right upper lobe. | There is a 15 mm nodule in the RUL. | YES | |
| No focal consolidation is seen. | Focal consolidation is not seen. | YES | |
| Small left pleural effusion. | Small right pleural effusion. | NO | left → right |
| Mild cardiomegaly, unchanged. | Mild cardiomegaly, increased. | NO | unchanged → increased |
| Opacity may represent atelectasis. | Opacity represents atelectasis. | NO | may represent → represents |
| There is a 1.5 cm nodule. | There is a 1.5 mm nodule. | NO | cm → mm |

## 4. 규칙
1. **두 텍스트 사이의 관계만** 판단합니다. 판독문이 의학적으로 타당한지, 글이 잘 쓰였는지는 판단하지 않습니다.
2. 문장이 어색하거나 문법이 이상해도 UNCERTAIN을 쓰지 않습니다. **그 문장이 말하는 내용**으로 YES/NO를 정합니다.
3. `XXXX`, `___`는 개인정보를 가린 자리입니다. 무시합니다.
4. **NO와 UNCERTAIN에는 `reason` 열에 달라진 구절을 반드시 적습니다.** 몇 단어면 충분합니다 (예: `left → right`). YES는 비워 둡니다.
5. 차이는 섹션 어디에나 있을 수 있고 문장 순서가 다를 수 있습니다. **끝까지 읽고** 비교합니다.
6. **혼자서** 작업합니다. 다른 사람과 상의하지 않고, ChatGPT 등 **AI 도구나 자동 비교 도구(diff)를 쓰지 않습니다.** 모르는 용어를 사전·검색으로 찾아보는 것은 괜찮습니다.
7. 답은 대문자로 `YES`, `NO`, `UNCERTAIN` 중 하나만 적습니다. 행을 추가·삭제·정렬하지 말고, `annotation_id`와 두 텍스트 열은 고치지 않습니다.

## 5. 제출
- 파일 이름의 `BLINDED`를 `filled`로 바꿔 저장해서 보내 주세요 (예: `annotator_A_PART1_filled.xlsx`, `annotator_A_PART2_filled.xlsx`).
- 모든 행의 `meaning_preserved`가 채워졌는지, NO·UNCERTAIN 행에 `reason`이 있는지 확인해 주세요.
- PART1이 끝나면 PART2를 기다리지 말고 먼저 보내 주셔도 됩니다.
- 작업에 걸린 대략의 시간을 함께 알려 주세요.
