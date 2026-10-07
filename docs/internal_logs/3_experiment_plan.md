# 3. ARR October 실험 계획 (길라잡이)

- 작성일: 2026-09-30
- 선행 문서: `0_prior_paper_and_experiment_analysis.md`, `1_review_analysis.md`, `2_audit_findings_and_revision_plan.md`
- 용도: 10/12 제출까지 무엇을 어떤 순서로 하고, 어디서 멈출지 정하는 기준 문서. 문서 2의 E1–E9 중 이 문서와 다른 부분은 이 문서를 따른다.
- 표기: ✅ 웹에서 직접 확인함 / ⚠️ 확인 필요(추정 또는 일부만 확인)

---

## 0. 한눈에 보기

| 항목 | 내용 |
|---|---|
| 마감 | **2026-10-12 (월)**, 남은 기간 12일 |
| 주장 | Perturbation 기반 metric 메타평가는 **surface 거리와 의미 변화를 혼동**한다. 혼동의 방향은 benchmark 구성이 정한다. 둘을 분리하면 metric 순위와 LLM judge에 대한 기존 결론이 달라진다 |
| 핵심 실험 | X1 factorial 세트 → X2 LLM judge → X3 기존 benchmark audit → X4 metric 확장 → X5 사람 검증 → X6 외부 타당성 |
| Gate | 10/4 pilot 결과로 October 제출 여부 결정 (§9) |
| 데이터 역할 | **IU X-Ray = 공개 트랙** (모든 judge, 사람 검증, release) / **MIMIC-CXR = 로컬 트랙** (로컬 모델만, 규모·재현 확인) |
| 수준 판단 | X1–X6이 깨끗하면 main conference권. Oral급은 X3의 일반화와 전문의 검증 유무에 달림 |

---

## 1. 확인된 사실 (2026-09-30 기준)

### 1.1 ARR 일정과 규정

| 항목 | 내용 | 상태 | 계획에 주는 영향 |
|---|---|---|---|
| October cycle 제출일 | 10월 12일. 리뷰 마감 11/16, author response 11/24–11/30, meta-review 12/17, cycle 종료 12/20 | ✅ | 시간대(AoE 여부)는 OpenReview에서 확인 ⚠️ |
| 대상 학회 | October가 마지막 cycle인 학회는 NAACL 2027, COLING 2027 (commit 12/23). ACL 2027의 마지막 cycle은 2027년 1월 | ✅ | October 리뷰를 ACL 2027에 commit 가능한지는 ACL 2027 CFP에서 확인 ⚠️ |
| 재제출 요건 | 이전 제출 링크 필수. 변경 요약 + 모든 리뷰어·meta-review 지적에 대한 point-by-point 응답 필수. 누락 시 desk reject | ✅ | revision note를 10/9부터 작성 (§8) |
| 리뷰어 배정 | 기본은 원래 리뷰어·AC. 새 리뷰어 요청에는 근거 필요 | ✅ | 같은 리뷰어 유지 |
| 재제출 제한 | meta-review 1.5는 다음 cycle 재제출 불가. 우리는 2점이라 해당 없음 | ✅ | |
| Service contributor | October 2026부터 자격 있는 contributor가 없으면 리뷰가 보장되지 않음(추첨). 제출 후 48시간 내 등록 | ✅ | 저자 중 누가 맡을지 지금 정함 |
| OpenReview 프로필 | 모든 저자가 ORCID·소속 이력 등을 갖춘 프로필 필요. 마감 후 1주 이내 완료 | ✅ | 전문의를 공저자로 넣으면 지금 프로필 생성 |
| 동시기 연구 기준 | 마감 3개월 이내(2026-07-12 이후) 공개 논문은 상세 비교 의무 없음 | ✅ | §1.3 표의 "비교 의무" 열 |
| 분량 | long paper 본문 8쪽, Limitations 필수, 부록은 2단 형식 | ✅ | |
| 익명 자료 | 익명 저장소 사용. Google Drive·Dropbox 링크 불가 | ✅ | anonymous.4open.science 사용 |

### 1.2 데이터 규정

| 항목 | 내용 | 상태 | 계획에 주는 영향 |
|---|---|---|---|
| MIMIC + 외부 LLM | 2025-09 PhysioNet 공지: zero data retention 필수, 로컬 LLM 강력 권장, 특정 플랫폼을 승인·추천하지 않음. 데이터 처리 방식이 불분명하면 사용 금지 | ✅ | 문서 2의 "승인 경로(Azure/Bedrock/Vertex)"는 2023년 공지 기준이므로 폐기. **MIMIC은 로컬 모델만** |
| MIMIC 파생 데이터 공개 | 파생 데이터는 PhysioNet에서 같은 계약으로 공유해야 함 | ✅ | 익명 repo에는 **IU X-Ray 쌍 + 코드 + MIMIC reconstruction script**만 |
| ReXVal | PhysioNet credentialed, MIMIC 파생 | ⚠️ | 로컬 모델만. 다운로드 가능 여부 확인 |

### 1.3 문서 0–2에 빠진 선행연구

| 논문 | 내용 | 비교 의무 | 우리 논문에서의 처리 |
|---|---|---|---|
| ReEvalMed (EMNLP 2025) | MIMIC 50 + ReXVal 20 report에서 DeepSeek-R1으로 한 aspect씩 재작성, 임상의 검증 400쌍. Discrimination / Robustness / Monotonicity. aspect당 10개 | 있음 | 핵심 비교 대상. X3에서 audit |
| Beyond Scalar Scores (arXiv 2606.18797, 2026-06-17) | ReEvalMed 위에서 LLM evaluator 8개 평가. "오류는 잘 잡지만 무해한 재서술을 과하게 벌점" 보고. Qwen3-8B·MedGemma-4B로 metric 학습 | 있음 | **E4 결론을 선점**. 우리 질문은 "그 과민이 edit 크기를 맞춰도 남는가"로 차별화 |
| RadSEM (arXiv 2606.17062, 2026-06-03) | 5단계 monotonicity stress test. lexical artifact를 줄이려 동의어 치환 사용 | 있음 | 인용. 문제 인식은 있으나 정량화는 없다는 근거 ⚠️ (초록 수준만 확인) |
| CRIMSON (arXiv 2603.06183, 2026-03) | 임상 맥락을 반영한 LLM metric. RadJudge, RadPref(전문의 판단) 공개. MedGemma fine-tune 모델 공개 | 있음 | metric으로 포함(X4). RadPref는 X6 후보 |
| REREF (arXiv 2609.19093, 2026-09) | 전문의가 검증한 대체 reference로 CRIMSON·GREEN·RadCliQ 등이 보고 관행 차이에 민감함을 보임 | 없음(동시기) | 인용만 ⚠️ (일부만 확인) |
| RadOT-Eval (arXiv 2606.08769) | ReXErr-v1 stress test에 reference-count-only control 사용 | 있음 | "통제 baseline" 선례로 인용 |

ReEvalMed의 공개 표에서 읽히는 사실 (X3의 출발점)

| Metric | significant-error 쌍 평균 점수 | insignificant 쌍 평균 점수 |
|---|---|---|
| BLEU | 78.48 | 41.89 |
| ROUGE-L | 87.90 | 65.95 |
| RadGraph | 81.35 | 58.56 |
| BERT-F1 | 97.31 | 92.99 |
| GREEN | 74.30 | 74.76 |

- Surface 계열 metric은 오류가 있는 쌍에 더 높은 점수를 준다. 저자들도 insignificant 쌍은 surface 변화가 크고 significant 쌍은 국소적이라는 **데이터 설계 탓**이라고 본문에 적었으나 통제하지 않았다.
- 우리 v1의 Audit A·B와 같은 현상이다. 단 v1에서는 Jaccard가 "정방향"으로 보였고(benign이 토큰 bag을 안 바꿈) ReEvalMed에서는 lexical metric이 "역방향"으로 보인다. **혼동의 방향이 benchmark 구성에 따라 바뀐다**는 것이 우리 주장의 근거다.
- ReEvalMed 데이터는 공개 재배포하지 않으며 PhysioNet 제출 절차 중이라고 기재되어 있다. 현재 접근 가능 여부는 GitHub에서 확인 ⚠️

---

## 2. 사용자가 정해야 할 것

| # | 항목 | 기한 | 안 되면 |
|---|---|---|---|
| U1 | 영상의학과 전문의 섭외 (2–3시간 분량, §6.5) | 10/1 | 전문의 없이 제출 가능하나 oral급 근거가 빠짐. jzA1 J2·J4는 말로만 대응하게 됨 |
| U2 | 대학원생 annotator 2명 (10/5–10/8, 각 약 480쌍) | 10/1 | 사람 검증 없이 제출 불가 → 1월 cycle |
| U3 | API key (Claude / GPT / Gemini). IU X-Ray에만 사용 | 10/3 | X2를 open-weight만으로 진행. 38pP P5가 절반만 해결됨 |
| U4 | ReXVal 다운로드 (PhysioNet) | 10/5 | X6 생략 또는 RadPref로 대체 |
| U5 | ReEvalMed 데이터 접근 확인 (GitHub, PhysioNet) | 10/5 | X3은 공개 표 기반 분석 + v1 + 우리 세트 내 재현으로 진행 |
| U6 | Service contributor 지정, 전 저자 OpenReview 프로필 | 10/8 | 리뷰 추첨 대상 또는 desk reject |
| U7 | IRB / exemption 필요 여부 (May checklist D4 = No) | 10/5 | checklist 기재 방식 결정 |
| U8 | 목표 학회: NAACL/COLING 2027 commit인지, ACL 2027까지 보유인지 | 10/4 | gate 판단 기준에 영향 (§9) |
| U9 | 저자 변경(전문의 추가) 여부 | 10/8 | 재제출 양식에 사유 기재 필요 |

이미 답이 나온 것
- 같은 리뷰어 재배정: **유지**
- 재annotation: **필수**. 기존 480쌍 라벨은 "통제 전(v1)" 조건의 근거로만 사용
- MIMIC 원본 txt: 불필요 (CSV의 full text로 재파싱)
- 추가 corpus(CheXpert Plus, ReXGradient): 이번에는 하지 않음

---

## 3. 논문 구성

### 3.1 기여 (3개)
1. **진단**: 기존 perturbation benchmark(v1, ReEvalMed)의 라벨이 surface feature만으로 예측된다는 것을 보임. meaning-blind baseline을 메타평가의 필수 보고 항목으로 제안
2. **설계**: 같은 target 문장에서 의미와 surface를 독립적으로 조작한 factorial minimal-pair benchmark. surface를 맞춘 조건에서 lexical baseline이 chance임을 보고
3. **결과**: metric·LLM judge를 "의미 민감도"와 "surface 민감도" 두 축으로 분해. 혼동 조건과 통제 조건에서 순위가 어떻게 달라지는지, LLM judge에 남는 실패가 무엇인지 보고

### 3.2 v1 대비 변경

| | ARR May (v1) | ARR October |
|---|---|---|
| Headline | GREEN 최강, BERTScore reversed | surface–의미 혼동과 그 분해 |
| v1 결과의 위치 | 주 결과 | "통제 전" 조건 (혼동의 증거) |
| Sensitivity card | 기여 3 | 부록 또는 삭제 |
| 주 지표 | pooled AUROC | surface 층 내 paired accuracy / AUROC + 혼동 조건과의 차이 |
| Corpus | MIMIC | IU X-Ray(공개) + MIMIC(로컬) |

### 3.3 그림·표 예산 (본문 8쪽)

| 번호 | 내용 | 출처 실험 |
|---|---|---|
| Fig 1 | 설계 도식: 한 reference에서 나온 6칸 예시 | X1 |
| Table 1 | 세트 통계 + shortcut floor (surface-only 분류기 AUROC) | X1 |
| Fig 2 | metric별 혼동 조건 AUROC vs 통제 조건 AUROC (slope chart) | X1, X4 |
| Fig 3 | 의미 민감도 × surface 민감도 산점도 (metric·judge 전체) | X1, X2, X4 |
| Table 2 | LLM judge: 칸별 TPR/FPR, 타입별 | X2 |
| Table 3 | 기존 benchmark audit | X3 |
| Table 4 | 사람 검증 요약 | X5 |
| Fig 4 | 통제 점수 vs 전문의 상관 (외부 타당성) | X6 |

---

## 4. E1: 데이터 재구축 (문서 2의 E1 유지, 아래만 변경)

- **IU X-Ray를 먼저** 만든다. 공개·API·사람 검증이 모두 이 corpus에서 이뤄지므로 pilot도 IU로 한다
- IU: `XXXX` 비식별 토큰이 있는 문장은 target에서 제외
- MIMIC: fallback 제거. IMPRESSION/FINDINGS 헤더가 실제로 있고 두 본문이 다른 report만 사용
- 문장 분리기 교체 (`Dr.`, `a.m.`, 번호 목록)
- **3문장 이상**인 섹션만 target 후보 (S1·S2 칸을 만들려면 필요)
- 평가 세트는 하나. subset 계층 없음
- 샘플링은 `hashlib` 기반 고정 seed (Python `hash()` 사용 금지, 문서 0 §5.3 E5)

---

## 5. X1: Factorial 세트 (P0)

### 5.1 설계

한 target 문장(report R 안의 문장 s)에서 아래 칸을 모두 만든다.

| | S0 최소 (target 문장만) | S1 구조 (재배열·서식, 토큰 bag 유지) | S2 재서술 (나머지 문장 paraphrase, 토큰 bag 변경) |
|---|---|---|---|
| **P 의미 보존** | P0: s에 benign 치환 | P1: P0 + 나머지 문장 재배열·서식 | P2: P0 + 나머지 문장 paraphrase |
| **C 의미 변경** | C0: s의 같은 위치에 flip | C1: P1과 동일하되 s에 flip | C2: P2와 동일하되 s에 flip |

- 같은 열의 P와 C는 **target 구절 하나만 다르다**. 따라서 열 안에서는 surface 거리가 같다
- 우선순위: S0과 S2는 필수. S1은 규칙 기반이라 비용이 낮으므로 함께 만든다
- S1은 v1의 benign(format, sentence_order)에, S2는 ReEvalMed의 insignificant 재작성에 대응한다. 한 세트 안에서 두 benchmark의 혼동을 모두 재현한다

비교 조건

| 조건 | 비교 | 의미 |
|---|---|---|
| 통제 (최소) | C0 vs P0 | 국소 edit에서의 의미 민감도 |
| 통제 (재서술) | C2 vs P2 | surface 잡음 속에서의 의미 민감도. LLM judge용 hard tier |
| 혼동 (v1형) | C0 vs P1 | v1 재현 |
| 혼동 (ReEvalMed형) | C0 vs P2 | ReEvalMed 재현 |
| Surface 효과 | P2 vs P0, P1 vs P0 | 의미가 같을 때 surface만으로 생기는 penalty |

### 5.2 타입별 matched 쌍

| 타입 | C (변경) | P (보존) | 비고 |
|---|---|---|---|
| laterality | left → right | left → left-sided | bilateral 제외. 병변 laterality만 |
| negation | No X is seen → X is seen | No X is seen → X is not seen | 문장 구조별 템플릿. 명사구 중간 삽입 금지 |
| measurement | 4.7 cm → 9.4 cm (수치) / 4.7 cm → 4.7 mm (단위) | 4.7 cm → 47 mm | 수치·단위를 하위 타입으로 분리 |
| temporal | unchanged → increased | unchanged → stable | 기구 위치 문장 제외 |
| severity | mild → moderate (인접) / mild → severe (양극단) | mild cardiomegaly → mildly enlarged heart | 인접·양극단을 하위 타입으로 |
| uncertainty | may represent → represents | may represent → could represent | hedged↔definite 치환만. 삽입형 금지 |
| anatomy | upper lobe → lower lobe | right base → right basilar | |

- P의 치환 lexicon은 **전문의 승인 후 확정** (§6.5). 승인 전에는 pilot 용도로만 사용
- deletion / insertion은 같은 위치 치환이 불가능하므로 core 설계에서 분리한다. 시간이 남으면 "중복 문장 삽입·삭제"를 크기 matched benign으로 두고 별도 층으로 보고(P1). 없으면 v1 조건에서만 보고하고 통제되지 않았음을 명시

### 5.3 제약

| 제약 | 기준 |
|---|---|
| Edit 크기 | 같은 target의 P0와 C0의 edit 토큰 수 차이 ≤ 2 |
| 패턴 다양성 | 한 치환 패턴이 해당 타입의 15%를 넘지 않음 (v1은 한 패턴이 81%) |
| 문법성 | LM perplexity 증가량 상한. P와 C의 분포가 비슷해야 함 |
| 모순 | reference 안에 같은 구절이 여러 번 나오면 제외하거나 전부 일관 처리 |
| S2 paraphrase 검증 | 양방향 NLI 통과 + 생성 모델과 다른 모델의 동치 확인 + 사람 검증 표본에 전부 포함 |
| 순환 방지 | S2 생성에 쓴 모델 계열은 judge 결과에서 따로 표시 |
| Shortcut floor | surface-only 분류기(Jaccard, token F1, edit distance, edit 토큰 수, 길이 비율 → 로지스틱 회귀, 5-fold)의 AUROC가 통제 조건에서 **0.45–0.55**. 벗어나면 세트를 고친다 |

### 5.4 규모

| | target 수 | candidate 수 (6칸) |
|---|---|---|
| Pilot (IU) | 7타입 × 40 = 280 | 1,680 |
| Full (corpus당) | 7타입 × 150 = 1,050 | 6,300 + identity |

- IU에서 50개 미만인 타입(measurement 가능성 높음)은 가능한 만큼만 만들고 본문에 명시

### 5.5 분석

- Penalty 정의는 v1과 동일: `Δ = m(x, x) − m(x, x̃)`
- 주 지표: **paired accuracy** = 같은 target에서 `Δ(C) > Δ(P)`인 비율 (동점 0.5). 보조로 AUROC
- 혼합효과 모형: `Δ ~ 의미 × surface + (1 | report)`. metric마다 의미 주효과, surface 주효과, 상호작용을 표준화해서 보고 → Fig 3의 두 축
- CI는 report 단위 cluster bootstrap. metric 간 차이는 paired bootstrap
- 타입별·하위 타입별 분해 (severity 인접 vs 양극단은 dose-response로)

---

## 6. 나머지 실험

### 6.1 X2: LLM judge (P0) — 대응: 38pP P5, AC

| 항목 | 내용 |
|---|---|
| 모델 | 38pP가 지목한 계열(Gemini, Claude, GPT, MedGemma, Qwen)에서 각 1개 이상 + Llama 계열. 정확한 버전은 실행 직전에 확인하고 버전 문자열·실행일을 기록 ⚠️ |
| 실행 위치 | open-weight: 두 corpus 모두 (H200, vLLM). proprietary: **IU X-Ray만** |
| Prompt | (a) binary rubric + 확신도 (b) GREEN식 error 나열 + 임상 중요도. 2개로 고정 |
| 점수 | 로컬은 label token logit, API는 0–100 확신도 또는 error 수. identity 행도 실제로 통과시킴 |
| 보고 | 칸별 TPR(C0, C1, C2)과 FPR(P0, P1, P2), 타입별, prompt 간 차이, 쌍당 비용 |

답해야 할 질문
1. C0 vs P0에서 saturate하는가 (38pP P2)
2. **edit 크기를 맞춘 P0에서도 benign 오경보가 남는가** (Beyond Scalar Scores의 결론이 surface 효과인지 검증)
3. C2에서 flip을 놓치는가. 어떤 타입에서인가

### 6.2 X3: 기존 benchmark audit (P0, CPU 1일) — 대응: AC novelty, 38pP P1

| 대상 | 방법 | 필요 자원 |
|---|---|---|
| v1 | 완료 (Audit A·B). surface-only 분류기 수치만 추가 | 없음 |
| ReEvalMed (공개 표) | §1.3의 표로 surface 계열 metric의 방향을 분석 | 없음 |
| ReEvalMed (데이터) | surface-only 분류기로 significant/insignificant 예측 | U5 |
| 우리 세트 | 혼동 조건(C0 vs P1, C0 vs P2)에서 v1·ReEvalMed 패턴이 재현되고 통제 조건에서 사라짐 | X1 |
| RadJudge 등 | 접근·라이선스가 되면 추가 ⚠️ | 선택 |

- 산출물: Table 3. 행은 benchmark, 열은 surface-only AUROC, 혼동의 방향, 통제 여부

### 6.3 X4: Metric 확장 (P1) — 대응: 38pP P3, AC

| 우선순위 | Metric | 비고 |
|---|---|---|
| 필수 | GREEN, RaTEScore, RadGraph, F1CheXbert, Temporal | v1에서 실행됨 |
| 필수 | CRIMSON | RadEval의 `crimson` + 공개 MedGemma 모델, 로컬 |
| 필수 | RadCliQ-v1 | May의 import 오류 수정 |
| 필수 | BERTScore 3종 (distilbert / roberta-large / deberta-xlarge-mnli) | backbone을 본문에 기재. reversal이 통제 조건에서 사라지는지 확인 |
| 필수 | BLEU, ROUGE-L, Jaccard, token F1 | shortcut floor로 표 맨 위 |
| 선택 | SRR-BERT, RadEval-BERTScore | tokenizer 오류가 빨리 풀리면 |
| 제외 | GEMA-Score, FineRadScore, CheXprompt | X2의 LLM judge로 대체. Limitations에 명시 |

### 6.4 X6: 외부 타당성 (P1) — 대응: jzA1 J3

- ReXVal 200쌍에 로컬 metric·judge 전부 실행 → 전문의 error 수와의 Kendall τ
- 질문: metric의 **통제 조건 점수**가 **v1 pooled AUROC**보다 ReXVal τ를 잘 예측하는가
- 한계를 본문에 명시: metric 수가 적어 검정력이 낮음. ReXVal 자체의 전문의 간 상관이 낮다는 지적(ReEvalMed Table 1)이 있음
- proprietary judge는 ReXVal에 돌릴 수 없으므로 문헌에 보고된 값만 인용

### 6.5 X5: 사람 검증 (P0, 병목)

| 층 | 누가 | 무엇을 | 분량 |
|---|---|---|---|
| 유형 단위 | 전문의 | P 치환 lexicon 승인/기각 | 50–80개 항목 |
| 유형 단위 | 전문의 | changed 타입·하위 타입별 임상 중요도 등급 (J2) | 약 12개 |
| 쌍 단위 | 전문의 | meaning preserved 여부 | 150–200쌍 (P칸 위주) |
| 쌍 단위 | 대학원생 2명 | meaning preserved 여부, **전수 이중 annotation** | 약 480쌍 (6칸 × 7타입 균등) |

- 검증 표본은 **IU X-Ray에서만** 뽑는다 (라벨과 텍스트를 함께 공개하기 위해)
- v1의 문제 수정: 단일 annotation 없음, UNCERTAIN 사용 기준을 지침에 명시, NO·UNCERTAIN에는 사유 필수, 칸·타입 blind
- 보고: 칸별 일치율, Cohen κ, 전문의–대학원생 일치, 3-class 처리 3가지 (rebuttal 분석 재사용)
- 사람 라벨 기준 paired accuracy / AUROC를 rule 라벨 기준과 나란히 보고

### 6.6 기타

| 항목 | 내용 | 우선순위 |
|---|---|---|
| E8 메커니즘 | GREEN이 출력한 error category가 실제 perturbation 타입과 일치하는가. RadGraph의 laterality·measurement 누락 | P1, 각 반나절 |
| Release | 익명 repo: 코드 전체, IU 쌍·점수·사람 judgment, MIMIC reconstruction script, rule 표 | P0 (Software 1점 대응) |
| 논문–코드 일치 | 문서 0 §5의 R1–R5, D1–D4, E1–E8 전부 해소 | P0 |

---

## 7. 하지 않는 것

| 항목 | 이유 |
|---|---|
| CheXpert Plus, ReXGradient 등 추가 corpus | 라이선스·전처리 시간. IU + MIMIC으로 J1·W1 대응 |
| MIMIC을 외부 API로 전송 | PhysioNet 2025-09 공지 |
| MIMIC 파생 쌍의 직접 공개 | PhysioNet 파생 데이터 지침 |
| Composed stress (v1 rebuttal 설계) | 설계 결함. C2 칸이 대체 |
| 다중 seed 전면 재실행 | paired 설계 + cluster bootstrap으로 충분. 생성 seed 2개만 부록에 |
| Sensitivity card를 기여로 제시 | novelty 없음 |
| "clinical severity" 주장 | 38pP P4에 동의한 대로 text-level semantic test로 framing. 임상 중요도는 전문의 등급으로만 |

---

## 8. 리뷰 지적 ↔ 대응 (revision note 초안용)

| 지적 | 대응 |
|---|---|
| AC: novelty 제한, BERTScore는 알려진 사실 | 주장 전환. reversal은 artefact임을 보임 (X1, X3) |
| AC / 38pP P5: 최신 LLM | X2 |
| AC / 38pP P3: 최신 metric | X4 (CRIMSON, RadCliQ, BERTScore 변형). 제외한 것은 사유 기재 |
| 38pP P1: ReEvalMed와의 차이 | X3 + related work. Beyond Scalar Scores도 함께 |
| 38pP P2: LLM에게 너무 쉬움 | C2 칸, X2 질문 1·3 |
| 38pP P4: framing | text-level로 수정 |
| jzA1 J1 / 84Wq W1: 단일 corpus | IU X-Ray를 주 공개 트랙으로 |
| jzA1 J2: 임상 중요도 | X5 전문의 등급 + 등급별 결과 |
| jzA1 J3: construct validity | X6 |
| jzA1 J4: annotator 임상 경험 | X5 전문의 |
| jzA1 J5: rule 상세 | 부록 rule 표 (코드와 일치) |
| jzA1 J6·J7: UNCERTAIN | 3가지 처리 + Khorasani 2003 인용 |
| jzA1 J8, Software 1점 | 익명 repo |
| jzA1 J9: 표기 | 반영 |
| 84Wq W2: fine-grained 분석 | 타입별 표 본문 승격 + E8 |
| 84Wq W3: 데이터 구성 혼란 | 평가 세트 통일 |

---

## 9. 일정과 gate

| 날짜 | 서버 작업 | 사용자 작업 |
|---|---|---|
| 9/30 (수)–10/1 (목) | E1: IU 재구축 → MIMIC 재파싱. 문장 분리기, 규칙 재작성 | U1, U2 요청 발송. U6 시작 |
| 10/2 (금)–10/3 (토) | X1 pilot 생성(IU 280 target). shortcut floor 확인. vLLM 설치. RadCliQ·CRIMSON 환경 | U3 |
| 10/4 (일) | pilot에 Jaccard, BERTScore, RaTEScore, GREEN, 로컬 LLM 2개 실행 → **Gate 1** | U8 결정. Gate 판단 |
| 10/5 (월)–10/6 (화) | Full 세트 생성(IU, MIMIC). X4 전체. X2 open-weight | annotation 시작. 전문의 lexicon 승인. U4, U5, U7 |
| 10/7 (수)–10/8 (목) | X2 proprietary(IU). X3. X6. 본문 §1–§3 초안 | annotation 완료. U6 완료 |
| 10/9 (금) | **실험 동결 (Gate 2)**. 분석, 그림, E8 | revision note 초안 |
| 10/10 (토)–10/11 (일) | 본문 완성, 부록, 익명 repo, checklist | 전체 검토 |
| 10/12 (월) | 제출 | service contributor 등록 (48시간 내) |

### Gate 1 (10/4): October에 낼 것인가

전제 조건 (하나라도 실패하면 세트부터 고침)
- 통제 조건에서 surface-only 분류기 AUROC가 0.45–0.55
- P·C 후보를 눈으로 50개씩 확인했을 때 비문·모순이 5% 미만

진행 조건 (하나 이상 충족)
- 혼동 조건과 통제 조건 사이에 metric 순위가 바뀜 (예: BERTScore reversal 소멸, GREEN 하락)
- LLM judge의 P0 오경보 또는 C2 누락이 유의하게 남음

중단 조건
- 모든 judge가 전 칸에서 천장이고 순위도 v1과 같음 → 논문이 "LLM judge를 쓰라"로 줄어듦. **1월 cycle로 넘기고 설계를 다시 함**
- U2가 확보되지 않음 → 1월 cycle

### Gate 2 (10/9): 무엇을 본문에 넣을 것인가

| 상태 | 처리 |
|---|---|
| X5 전문의 미완 | 대학원생 검증만으로 제출. Limitations에 명시. oral급 기대는 낮춤 |
| X2 proprietary 미완 | open-weight만으로 제출하지 않는다. 38pP P5가 남으므로 최소 2개 계열은 필요 |
| X6 미완 | 부록 또는 생략 |
| X3의 ReEvalMed 데이터 없음 | 공개 표 기반 분석 + 우리 세트 내 재현으로 진행 |

---

## 10. 위험과 대비

| 위험 | 대비 |
|---|---|
| P 치환이 실제로는 의미를 바꿈 (전문의가 기각) | 기각된 lexicon 항목과 그 쌍을 제거. 전문의 승인을 full 생성 전(10/5)에 받음 |
| S2 paraphrase가 의미를 바꿈 | NLI + 교차 모델 확인 + 사람 표본. 통과율을 보고 |
| IU에서 일부 타입 수가 부족 | 해당 타입은 MIMIC 로컬 트랙에서만 보고 |
| LLM judge가 비문에 반응 | P와 C의 perplexity 분포를 맞추고 표로 보고 |
| S2 생성 모델과 judge의 순환 | 생성 모델 계열을 표시하고 제외했을 때의 결과도 보고 |
| 시간 부족 | S1 칸, deletion/insertion 층, E8, X6 순으로 뺌. X1(S0·S2), X2, X4 필수분, X5 대학원생, release는 빼지 않음 |

---

## 11. 출처

- ARR Dates and Venues: https://aclrollingreview.org/dates
- ARR Call for Papers: https://aclrollingreview.org/cfp
- PhysioNet, Use of MIMIC Data with LLMs and Online Services (2025-09-24): https://physionet.org/news/post/llm-responsible-use/
- PhysioNet, Responsible use of MIMIC data with online services like GPT (2023-04-18, 구 공지): https://physionet.org/news/post/gpt-responsible-use
- PhysioNet 파생 데이터 지침: https://www.physionet.org
- ReEvalMed: https://arxiv.org/html/2510.00280v1
- Beyond Scalar Scores: https://arxiv.org/pdf/2606.18797
- RadSEM: https://arxiv.org/pdf/2606.17062
- CRIMSON: https://arxiv.org/html/2603.06183
- REREF (Reporting Practice Matters): https://arxiv.org/pdf/2609.19093
- RadOT-Eval: https://arxiv.org/pdf/2606.08769
