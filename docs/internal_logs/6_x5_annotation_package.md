# 6. X5 사람 검증 패키지

- 작성: 2026-10-01
- 코드: `scripts/12_make_annotation_package.py` (실행 env: `envs/llm`, hashlib 고정 seed 2026)
- 출력: `data/annotation/`
- 원천: IU X-Ray full 세트 (`data/pairs/full_iu_all.csv`, 890 target × 7칸). IU만 쓰는 이유: 텍스트와 라벨을 함께 공개하기 위해 (계획 §6.5)

> **[10/5 갱신]** 전문의 층은 폐기(파일은 `data/annotation/_unused_radiologist/`). 대학원생용 PART2(204쌍, `scripts/19_make_supplementary_annotation.py`)를 추가했다. 현행 안내는 `11_annotation_handover.md`.

---

## 1. 파일 목록과 전달 대상

| 파일 | 대상 | 분량 | 내용 |
|---|---|---|---|
| `annotator_A_BLINDED.xlsx/.csv` | 대학원생 A | 504쌍 | reference / candidate / `meaning_preserved` / `reason` |
| `annotator_B_BLINDED.xlsx/.csv` | 대학원생 B | 504쌍 (A와 같은 항목, 순서만 다름) | 동일 |
| `radiologist_lexicon_review.xlsx` | 전문의 | 61행 | P 치환 패턴별 예시 2개 + 대응 C. `equivalent? (YES/NO/DEPENDS)` 기입 |
| `radiologist_clinical_importance.xlsx` | 전문의 | 11행 | 타입·하위타입별 예시. 임상 중요도 1–5 기입 (jzA1 J2 대응) |
| `radiologist_pairs_BLINDED.xlsx` | 전문의 | 169쌍 | 쌍 단위 meaning preserved 판단. P 칸 위주 |
| `INSTRUCTIONS_EN.md`, `INSTRUCTIONS_KR.md` | 전원 | – | 지침 |
| `grad_KEY_DO_NOT_SEND.csv`, `radiologist_KEY_DO_NOT_SEND.csv` | **전달 금지** | – | annotation_id ↔ uid, 칸, 타입, rule 라벨 |

## 2. 표본 설계

### 대학원생 (전수 이중 annotation)
- 7타입 × 6칸(P0, P1, P2, C0, C1, C2) × 12쌍 = **504쌍**
- 쌍마다 **서로 다른 target** (같은 reference가 두 번 나오지 않음 → 칸·타입 추측 방지)
- rule 라벨 비율: preserved 252 / changed 252
- A·B는 같은 504쌍을 서로 다른 순서로 받음. 단일 annotation 항목 없음 (v1은 480 중 300이 단일)

### 전문의
- lexicon 승인: P 치환 패턴 61개 (anatomy·uncertainty·laterality·negation·temporal·severity·measurement). 우리가 경계선으로 표시한 것(`flagged_by_us`)을 포함. NO로 판정된 패턴의 target은 full 세트에서 제거하고 재집계
- 임상 중요도: 11행 (anatomy/region, laterality, measurement value·unit, negation 두 방향, severity adjacent·extreme, temporal, uncertainty 두 방향)
- 쌍 단위: 타입당 P0 10 + P2 10 + C0 5 = 169쌍 (IU에서 measurement·uncertainty 공급 부족으로 175가 아닌 169). 대학원생 표본과 target이 겹치지 않음
- 예상 소요: lexicon 61행 약 30–40분, 중요도 10분, 쌍 169개 약 60–80분 → 계획의 2–3시간 이내

## 3. v1 대비 수정 (문서 2 Audit E)

| v1 문제 | 조치 |
|---|---|
| 480쌍 중 300쌍이 1인 판단 (rule 일치 86.0%) | 전 항목 2인 |
| UNCERTAIN 사용 기준이 annotator마다 다름 (0% / 0.7% / 8.6%) | 지침에 기준 명시: "두 표현이 어느 쪽으로도 읽혀 결정 불가"일 때만. 비문이라는 이유로 쓰지 않음 |
| 사유 기록이 한 명만 없음 | NO·UNCERTAIN에 `reason` 필수 |
| 샘플링이 Python `hash()` 의존 | hashlib md5 seed |
| 임상 경험 없는 annotator만 | 전문의 3종 시트 |
| benign 합의율이 낮음 (만장일치 53%) | P lexicon을 전문의가 유형 단위로 사전 승인 + P 칸 위주 쌍 검증 |

## 4. 회수 후 분석 계획 (스크립트는 회수 시 작성: `13_analyze_annotation.py`)

- 칸별·타입별 human–rule 일치율 (Wilson CI), A–B Cohen κ, 3-class 처리 3가지 (exclude / →changed / →preserved)
- 전문의–대학원생 일치 (전문의 169쌍은 대학원생과 다른 target이므로 칸·타입 단위 비율로 비교)
- 사람 라벨 기준 paired accuracy·AUROC를 rule 라벨 기준과 나란히 보고
- lexicon NO 패턴 제거 전후의 주요 수치 변화 (robustness)
- 임상 중요도 등급으로 가중한 타입별 결과

## 5. 주의

- 표본은 생성기 v5 + S2 paraphrase(Qwen2.5-7B, 문장 채택률 91.8%)의 결과다. **이후 생성기·paraphrase를 다시 돌리면 annotation과 불일치**하므로 `data/pairs/full_iu_*.csv`는 동결한다.
- 전문의가 lexicon 패턴을 기각하면 target을 제거만 하고 재생성하지 않는다.
