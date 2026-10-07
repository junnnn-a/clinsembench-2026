# 11. Annotation 전달 안내 — Annotator A, B 2명 (v2, 2026-10-05)

- 전제 변경: **전문의 검증은 받을 수 없다.** 이번 버전은 컨퍼런스용이고, 전문의·의사 검증은 저널 확장에서 다룬다
- 이 문서는 그 전제에서 (1) Annotator 2명에게 무엇을 어떻게 전달하고 돌려받을지 (2) 전문의가 하기로 했던 일을 무엇으로 대체하는지 (3) 논문에서 무엇을 주장하고 무엇을 주장하지 않는지를 정리한다
- 이전 버전(v1)의 전문의 항목과 `send_to_radiologist/` 폴더는 폐기. 파일은 `data/annotation/_unused_radiologist/`에 보관만 함

---

## 1. 요약

| 대상 | 보낼 폴더 | 파일 | 분량 | 예상 시간 | 회수 기한 |
|---|---|---|---|---|---|
| Annotator A | `data/annotation/send_to_annotator_A/` | PART1, PART2, 지침서 | 504 + 204쌍 | 6–8시간 | PART1 **10/8 (목)**, PART2 10/9 (금) |
| Annotator B | `data/annotation/send_to_annotator_B/` | PART1, PART2, 지침서 | 504 + 204쌍 | 6–8시간 | 동일 |

기준 경로: `/home/irteam/junah-data-1/ARR_10/2_ClimSemBench/data/annotation/`

폴더째로 보내시면 됩니다. 각 폴더에는 그 annotator에게 필요한 파일만 들어 있습니다.

---

## 2. 전문의 없이 무엇이 달라지는가

전문의에게 맡기려던 일은 세 가지였습니다. 각각을 이렇게 처리합니다.

| 원래 전문의가 할 일 | 왜 필요했나 | 대체 방법 | 논문에서의 표현 |
|---|---|---|---|
| ① 의미 보존 치환 lexicon 승인 (61개 패턴) | "mild → slight" 같은 치환이 정말 같은 뜻인지 | **PART2 추가**: 모든 치환 패턴을 Annotator 2명이 쌍 단위로 판단. 사전에 정한 규칙(§6)으로 패턴을 유지/제거. + 확인 대상 패턴을 전부 뺀 "보수적 세트" 결과를 본문 주 결과로 병기 (문서 9 §F에서 결론 유지 확인됨) | "두 명의 비임상 annotator가 text-level에서 검증" |
| ② 오류 유형별 임상 중요도 등급 | jzA1 J2 (임상적 중요도) | **하지 않음**. 임상 중요도에 대한 주장을 논문에서 하지 않는다 | Limitations: "임상적 중요도 가중은 다루지 않으며 전문의 검증이 필요" |
| ③ 쌍 단위 전문의 판단 169쌍 | jzA1 J4 (annotator의 임상 경험) | **하지 않음**. Annotator 전수 이중 annotation으로 대체 | Limitations + 저널 확장 계획 |

### 전문의 없이도 임상 전문가 근거를 일부 확보하는 방법 (데이터만 있으면 됨)

우리 annotator가 아니라 **이미 전문의가 라벨링한 공개 데이터**를 쓰는 방법입니다. annotator을 섭외할 필요가 없습니다.

| 데이터 | 전문가 라벨 | 우리가 할 분석 | 필요한 것 |
|---|---|---|---|
| ReXVal | 영상의학과 전문의 6명의 오류 수 | 통제 조건 점수가 전문의 오류 수 상관을 예측하는지 (jzA1 J3) | PhysioNet 다운로드 |
| ReEvalMed | 임상의 검증 400쌍 | 그 라벨이 surface만으로 예측되는지 직접 측정 | 저자 공개 여부 확인 |

둘 다 없어도 제출은 가능합니다. 있으면 "전문의 검증이 없다"는 약점을 상당 부분 덮습니다.

### 기대 수준에 대한 솔직한 평가

- jzA1(임상 배경, 3점)의 J2·J4는 실험이 아니라 **framing과 Limitations로** 답하게 됩니다. v1 rebuttal에서 이미 "text-level semantic test이며 임상 중요도는 주장하지 않는다"고 답했으므로 일관됩니다.
- 논문 전체에서 "clinical"이라는 단어를 주장에 쓰지 않도록 정리해야 합니다 (benchmark 이름의 "Clin"은 도메인 표시로만).
- 주 기여(혼동의 진단, 통제 설계, monotonicity 반례)는 annotator 라벨에 의존하지 않는 **구성적 성질**이라 전문의가 없어도 성립합니다. annotator 검증이 받치는 것은 "P는 정말 의미 보존, C는 정말 의미 변경"이라는 라벨 타당성이고, 이는 text-level 판단이라 Annotator으로 방어 가능합니다.
- oral 가능성은 전문의가 있을 때보다 낮아집니다. main conference 수준은 여전히 가능하다고 봅니다.

---

## 3. Annotator에게 보낼 파일

| 파일 | 행 수 | 무엇을 검증하나 (annotator에게는 비공개) |
|---|---|---|
| `annotator_X_PART1_BLINDED.xlsx` | 504 | 6칸 전체의 라벨 타당성. 7유형 × 6칸 × 12쌍. 의미 보존 252 / 변경 252 |
| `annotator_X_PART2_BLINDED.xlsx` | 204 | **치환 패턴별 타당성** (전문의 lexicon 승인의 대체). 패턴당 최대 3쌍의 "치환만 적용한" 쌍 139개 + 의미 변경 쌍 65개 |
| `INSTRUCTIONS_KR.md` / `INSTRUCTIONS_EN.md` | – | 지침 v3 (예시 7개, 두 파일 안내, AI·diff 도구 금지) |

- A와 B는 **같은 쌍을 서로 다른 순서로** 받습니다. 두 annotator는 같은 파일을 받으면 안 됩니다.
- PART1과 PART2는 report가 겹치지 않습니다.
- PART2는 10/5에 새로 만들었습니다. 이전에 PART1만 전달하셨다면 PART2와 지침 v3를 추가로 보내 주세요.

### 엑셀 구조 (두 파일 동일)

| 열 | annotator가 할 일 |
|---|---|
| `annotation_id` (PART1: G0000–, PART2: S0000–) | 건드리지 않음 |
| `reference_text`, `candidate_text` | 읽기 |
| `meaning_preserved (YES/NO/UNCERTAIN)` | **YES / NO / UNCERTAIN 중 하나** |
| `reason (required if NO or UNCERTAIN)` | **NO·UNCERTAIN이면 달라진 구절** |

### 시간이 부족할 때의 우선순위

1. PART1 전체 (필수. 없으면 제출 불가)
2. PART2 전체 (강력 권장. 없으면 lexicon 타당성은 PART1의 P 칸 252쌍과 "보수적 세트" 결과로만 방어)

---

## 4. Annotator 조건과 전달 방법

### 조건

| 조건 | 이유 |
|---|---|
| Annotator | 판독문 영어를 읽을 수 있어야 함 |
| **논문 저자가 아님** | 논문에 그렇게 기재 |
| **실험의 규칙 설계·결과를 모름** | blinding |
| 두 Annotator가 서로 상의하지 않음 | 일치도(κ)의 전제 |
| ARR May annotator와 같은 annotator이어도 됨 | 단 알려 주세요 (논문에 기재) |

### 말해도 되는 것 / 안 되는 것

| 말해도 됨 | 말하면 안 됨 |
|---|---|
| 판독문 쌍의 의미가 같은지 판단하는 연구용 작업 | 편집 유형의 목록·비율 |
| 지침서의 기준과 예시 | YES/NO 비율, PART2가 무엇을 검증하는지 |
| 분량과 시간, 나눠서 해도 됨 | 어떤 행이 어떤 조건인지 |
| 결과가 논문에 쓰이고 익명으로 공개될 수 있음 | 기대하는 결과 |

### 보낼 메시지 예시

```
안녕하세요. 영상의학 판독문 평가 지표 연구에 쓸 annotation을 부탁드립니다.

- 작업: 엑셀 각 행의 판독문 두 개(reference, candidate)가 같은 임상 내용을 말하는지
  YES / NO / UNCERTAIN으로 판단
- 파일: PART1 (504행, 4–6시간), PART2 (204행, 1.5–2시간). PART1을 먼저 해 주세요.
  여러 번에 나눠서 하셔도 됩니다.
- 기한: PART1은 10월 8일(목), PART2는 10월 9일(금)까지
- 방법: 첨부한 INSTRUCTIONS_KR.md를 먼저 읽어 주세요. 예시가 들어 있습니다.
- 주의: 혼자서 작업해 주세요. 다른 분과 상의하거나 ChatGPT 등 AI 도구, 자동 비교 도구를
  쓰시면 안 됩니다. 모르는 용어를 검색하는 것은 괜찮습니다.
- 제출: 파일 이름의 BLINDED를 filled로 바꿔 보내 주시고, 걸린 시간도 알려 주세요.
  PART1이 끝나면 먼저 보내 주셔도 됩니다.

판단 결과는 연구 논문에 사용되며, 개별 판단이 익명으로 공개될 수 있습니다.
동의하시면 진행 부탁드립니다. 감사합니다.
```

---

## 5. 회수

받은 파일을 아래 위치에 넣어 주세요.

```
data/annotation/returned/annotator_A_PART1_filled.xlsx
data/annotation/returned/annotator_A_PART2_filled.xlsx
data/annotation/returned/annotator_B_PART1_filled.xlsx
data/annotation/returned/annotator_B_PART2_filled.xlsx
```

| 넣기 전 확인 | 기준 |
|---|---|
| 행 수 | PART1 504, PART2 204 그대로 |
| 빈칸 | `meaning_preserved` 전부 채워짐 |
| 값 | `YES` / `NO` / `UNCERTAIN`만 |
| 사유 | NO·UNCERTAIN 행에 `reason` |
| `annotation_id` | 수정 없음 |

일부만 끝났어도 넣어 주시면 채워진 행으로 먼저 분석합니다. 파일이 들어오면 형식 점검 → 일치도 → annotator 라벨 기준 결과 순으로 분석합니다 (반나절).

---

## 6. 회수 후 분석 — 라벨을 보기 전에 정해 두는 규칙

결과를 보고 기준을 바꾸지 않도록 지금 고정합니다.

| 분석 | 규칙 |
|---|---|
| 항목 라벨 | 두 annotator가 일치하면 그 라벨. 불일치하거나 UNCERTAIN이 포함되면 "미합의". 주 결과는 합의 항목 기준, 미합의를 양쪽으로 넣은 민감도 분석 2가지 병기 |
| 일치도 | PART1 전체와 칸별 Cohen κ (3-class, 2-class), raw agreement |
| rule 라벨 타당성 | 칸별·유형별 human–rule 일치율과 Wilson 95% CI |
| **치환 패턴 유지/제거** | 패턴의 "치환만 적용한 쌍(P0)"에 대한 판단을 PART1 + PART2, 두 annotator 합쳐서 **YES 비율 ≥ 0.75이고 판단 수 ≥ 4이면 유지**. 미달이면 그 패턴의 target을 "검증 세트"에서 제거. 판단 수 < 4인 패턴(희귀 패턴 15개 예상)은 "미검증"으로 분류해 검증 세트에서 제외 |
| 보고할 세트 3가지 | (a) 전체 (b) **검증 세트** = 유지된 패턴만 (c) 보수적 세트 = 저희가 사전에 경계선으로 표시한 패턴 전부 제외. 세 세트의 주 결과를 나란히 |
| annotator 라벨 기준 metric 결과 | 합의 항목에서 paired accuracy를 다시 계산해 rule 라벨 기준과 비교 |

- 현재 표본에서 61개 패턴 중 46개가 판단 수 ≥ 4를 확보합니다. 나머지 15개는 IU에 target이 1–2개뿐인 희귀 패턴입니다.

---

## 7. 절대 보내면 안 되는 파일

| 파일 | 내용 |
|---|---|
| `grad_KEY_DO_NOT_SEND.csv` | PART1 정답 키 |
| `part2_KEY_DO_NOT_SEND.csv` | PART2 정답 키 |
| `_unused_radiologist/` 폴더 | 폐기된 전문의용 파일과 키 |
| `docs/`, `results/` | 설계와 결과 |

`send_to_annotator_A/`, `send_to_annotator_B/`에는 이 파일들이 없습니다.

---

## 8. 논문에 적어야 해서 알려 주실 것

| 항목 | 필요한 정보 |
|---|---|
| annotator 배경 | 과정(석사/박사), 전공, 의료 AI/NLP 경력 대략 |
| 저자 여부 | 저자가 아님 |
| ARR May annotator와 동일 인물인지 | 예 / 아니오 |
| 모집 방법 | 예: 연구실 내 요청 |
| 보상 | 금액 또는 "연구 과제의 일부로 수행" |
| 동의 | 연구 사용·익명 공개 동의 (위 메시지로 받으시면 됨) |
| 소요 시간 | 각자, PART별 |
| IRB | May 제출 때는 "심의·면제 확인을 받지 않음"으로 기재. 이번에도 같으면 그대로 |

---

## 9. 이 결정이 다른 계획에 주는 영향

| 문서 | 바뀌는 것 |
|---|---|
| 3 (계획) §6.5 | 전문의 3개 층 삭제. Annotator가 PART2가 lexicon 층을 대체 |
| 3 §8 (리뷰 대응) | jzA1 J2·J4: 실험 대응 → framing·Limitations 대응. J3은 ReXVal이 있으면 실험 대응 |
| 10 (현황) §6 | A3(전문의 lexicon)·B0(전문의 쌍 검증) 삭제. A2가 PART1 + PART2로 확대. B2(ReXVal)·B3(ReEvalMed)의 우선순위 상승 |
| 10 §7 D4 | 10/12 제출 조건이 "API key + annotation 회수" 두 가지로 줄어듦 |
| 논문 | 주 결과를 "검증 세트" 기준으로 보고. Limitations에 비임상 annotator·임상 중요도 미검증 명시. 저널 확장 계획 한 문장 |
