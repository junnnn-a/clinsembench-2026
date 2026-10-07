# 2. Audit 결과와 ARR October 보완 계획

- 작성일: 2026-09-30
- 선행 문서: `0_prior_paper_and_experiment_analysis.md`, `1_review_analysis.md`
- Audit 코드 (모두 `OLD/`는 읽기만 함)
  - `scripts/0_audit_prior_experiment.py` → `results/0_audit/AUDIT_REPORT.md` 및 `A_*.csv` ~ `E_*.csv`
  - `scripts/1_audit_trivial_baseline_human_labels.py` → `results/0_audit/F_trivial_baselines_on_human_labels.csv`
  - 실행 로그: `logs/0_audit_prior_experiment.log`, `logs/1_audit_trivial_baseline_human_labels.log`
  - 실행 환경: `/opt/conda/envs/clinsev/bin/python`, bootstrap 500회

---

## Part I. Audit 결과

리뷰어가 지적하지 않았지만 데이터를 직접 보면 드러나는 문제들이다. 재제출본이 공개 데이터/코드를 포함하게 되면 새 리뷰어가 발견할 수 있으므로 먼저 해결해야 한다.

### A. Bag-of-words baseline이 GREEN과 같은 성능을 낸다 (가장 중요)

논문 Table 3과 **같은 행**(subset200, 섹션당 2,400 candidate)에서 계산.

| Metric | Impression | Findings | Human-label (n=467) |
|---|---|---|---|
| GREEN | 0.903 | 0.896 | 0.814 |
| **Jaccard (token set overlap)** | **0.849** | **0.890** | **0.811** |
| token_f1 | 0.821 | 0.818 | 0.767 |
| "edit이 작을수록 changed" (−#edited tokens) | 0.814 | 0.844 | 0.762 |
| "토큰 bag이 바뀌었는가" (0/1) | 0.812 | 0.827 | 0.756 |
| RaTEScore | 0.768 | 0.804 | 0.725 |
| RadGraph | 0.650 | 0.639 | 0.587 |
| Temporal | 0.613 | 0.609 | 0.584 |
| F1CheXbert | 0.572 | 0.581 | 0.570 |
| BERTScore | 0.221 | 0.165 | 0.274 |

- Jaccard는 의미를 전혀 모르는 metric인데 human-label AUROC가 GREEN과 0.003 차이다.
- "토큰이 하나라도 바뀌었는가"라는 0/1 신호만으로 0.81–0.83이 나온다.
- 원인: benign 3타입 중 format과 sentence_order는 **alphanumeric 토큰 bag을 바꾸지 않는다** (bag 불변 비율: format 88–96%, sentence_order 100%). 반면 changed 9타입은 100% bag이 바뀐다.
- 의미: 현재 benchmark의 pooled AUROC는 "의미 변화 탐지력"이 아니라 상당 부분 "토큰 변화 탐지력"을 잰다. 논문 Appendix B에서 token_f1 Spearman 0.769를 보고하면서 "benchmark 구성의 영향"이라고 한 줄로 넘어갔지만, 실제로는 headline 결과 전체에 영향을 주는 문제다.

benign 타입별로 나눠 보면 더 분명하다 (ALL changed vs 단일 benign 타입, impression).

| Metric | vs format | vs sentence_order | vs paraphrase_rule |
|---|---|---|---|
| token_f1 | 0.904 | **1.000** | **0.561** |
| Jaccard | 0.883 | 0.979 | 0.686 |
| GREEN | 0.909 | 0.885 | 0.916 |
| RaTEScore | 0.657 | 0.867 | 0.779 |
| RadGraph | 0.667 | 0.550 | 0.732 |
| BERTScore | 0.160 | 0.156 | 0.346 |

- 의미 이해가 필요한 비교는 **paraphrase_rule 하나뿐**인데, 이 타입은 정규식 4개로만 만들어지고 subset200의 81%가 `There is no → No` 한 가지다.

### B. BERTScore reversal은 edit 크기 confound다

| 타입 | 평균 edit 토큰 수 (imp / find) |
|---|---|
| benign_sentence_order | 33.7 / 45.9 |
| benign_format | 4.1 / 5.6 |
| benign_paraphrase_rule | 2.8 / 3.3 |
| finding_deletion | 13.8 / 14.0 |
| false_finding_insertion | 8.7 / 9.0 |
| negation_flip | 1.95 / 2.48 |
| laterality, severity, anatomy, temporal, measurement | 1.0 / 1.0 |
| uncertainty_flip | 1.1 / 1.06 |

Spearman(metric penalty, #edited tokens):

| Metric | Impression | Findings |
|---|---|---|
| **BERTScore** | **0.810** | **0.865** |
| F1CheXbert | 0.353 | 0.377 |
| RadGraph | 0.219 | 0.289 |
| Temporal | 0.115 | 0.085 |
| RaTEScore | −0.030 | −0.052 |
| GREEN | −0.139 | −0.167 |

- BERTScore penalty는 바뀐 토큰 수를 거의 그대로 따라간다. benign은 많이 바꾸고 changed는 1 토큰만 바꾸도록 설계했으므로 "reversal"은 설계의 결과다.
- AC의 "BERTScore가 surface change에 민감한 건 이미 알려져 있다"는 평가와 정확히 맞닿는다.
- 같은 이유로 RadGraph의 낮은 AUROC도 일부는 format/sentence_order에 대한 과민 반응 때문이다 (vs paraphrase에서는 0.732 / 0.805).

### C. 규칙이 만든 candidate의 품질 문제

full clean 5k 기준 비율 (impression / findings). 휴리스틱 탐지이므로 근사치다.

| 타입 | 문제 | 비율 | 예시 |
|---|---|---|---|
| negation_flip | `no ` 삽입 방식이 차지하는 비중 | 62.9% / 41.4% | |
| negation_flip | 그중 명사구 중간에 `no`가 끼어 비문이 됨 | 94.3% / 94.5% | "Large left **no** pleural effusion has not improved" |
| negation_flip | 이미 부정 문맥인 문장에 `no` 추가 (의미가 실제로 안 바뀜) | 7.6% / 8.6% | "No evidence of pneumonia or vascular congestion or **no** pleural effusion" |
| negation_flip | negated→present 후 병렬 구조가 깨짐 | 13.9% / 27.0% | "Pleural effusion is present or pneumothorax" |
| uncertainty_flip | `possible ` 삽입 방식 비중 | 81.0% / 82.5% | "**possible** endotracheal tube has been removed" |
| laterality_flip | bilateral을 한쪽으로 치환 (논문은 skip이라 기술) | 9.1% / 6.3% | |
| laterality_flip | reference에 left와 right가 모두 있음 (첫 매칭만 뒤집어 모순 가능) | 34.5% / 46.1% | "small **right** pleural effusion, associated to a left retrocardiac atelectasis" |
| laterality_flip | reference에 기구·심장 구조 등 비병변 laterality 표현이 있음 (첫 매칭이 이것이면 병변이 아닌 대상이 뒤집힘. 상한 추정치) | 21.5% / 27.7% | "right heart failure" → "left heart failure" |
| measurement_flip | 단위 교체만 있음 | 100% | 4.7 cm → 4.7 mm |
| severity_flip | 인접 등급이 아닌 양극단 교체 | 79.4% / 80.6% | trace → large |
| temporal_flip | 기구 위치 문장에 적용되어 어색함 | 15.4% / 15.6% | "Port-A-Cath tip ... **increased** since" |
| benign_format | "Report impression:" 접두 | 14.2% / 2.1% | findings 섹션에도 동일 문구 |
| benign_format | 번호 목록이 깨짐 | 10.5% / 1.9% | "- 1. - Endotracheal tube ..." |
| benign_sentence_order | 담화 접속어(However, Otherwise, This ...)가 있어 순서 의존적 | 13.5% / 13.4% | |
| benign_sentence_order | `Dr.` / `p.m.` 에서 문장이 잘못 분리됨 | reference의 8.0% / 3.8%가 위험군 | "___ was paged at 12:25 p.m. The heart is ... Dr. There is ..." |
| finding_deletion | 섹션 전체가 "No acute cardiopulmonary abnormality."로 대체 | 11.4% / 0.7% | |
| false_finding_insertion | 삽입 문장이 laterality+severity+size를 동반 (minimal 아님) | 100% | "A new 3 cm nodular opacity ... left upper lobe" |

함의
- 비문 candidate는 LLM 기반 metric이 **의미가 아니라 부자연스러움**에 반응하게 만들 수 있다.
- human annotator가 benign을 "changed"로 본 사례 다수가 깨진 format/shuffle이다 (예: "- 1. - Endotracheal...", "Dr."에서 잘린 문장).
- 공개 데이터에서 위 예시가 보이면 benchmark 신뢰도가 크게 떨어진다.

### D. Impression / Findings 섹션이 실제로는 분리되어 있지 않다

| 범위 | n | IMPRESSION 헤더 있음 | FINDINGS 헤더 있음 | 둘 다 | findings 텍스트 == impression 텍스트 |
|---|---|---|---|---|---|
| 전체 prepared reports | 172,171 | 77.1% | 57.4% | 41.2% | **58.1%** |
| clean 5k (두 섹션 공통) | 4,666 | 82.5% | 62.3% | 44.8% | **54.6%** |
| subset200 impression | 1,741 | 79.9% | 55.3% | 35.2% | 64.0% |
| subset200 findings | 1,727 | 82.3% | 64.2% | 46.5% | 52.9% |

- 원인: `prepare`의 fallback (`findings = findings or impression or text`).
- clean 5k에서 두 섹션 세트는 **같은 4,666개 report**이며 그중 2,548개(54.6%)는 reference 텍스트가 완전히 동일하다.
- subset200에서도 749개 report가 양쪽에 있고 468개는 텍스트가 같다.
- 따라서 Table 3의 "Impression"과 "Findings" 열은 독립된 두 섹션 실험이 아니다. 두 열 수치가 비슷한 것은 재현성의 증거가 아니라 데이터 중복의 결과일 수 있다.
- "FINAL REPORT" 등 행정 헤더 오염(334/5000)도 같은 fallback에서 나온다.

### E. Human validation의 구조

| 항목 | 값 |
|---|---|
| 3중 annotation 항목 (180개)의 majority-rule 일치 | 98.3% |
| **단일 annotation 항목 (300개)의 rule 일치** | **86.0%** |
| 단일 항목 중 uncertainty_flip 일치 | 60.0% (n=25) |
| annotator별 rule 일치 | A 91.4%, B 85.0%, C 82.9% |
| annotator B의 uncertainty_flip 일치 | 8% (대부분 UNCERTAIN으로 응답) |
| annotator C의 negation_flip 일치 | 68% |
| overlap에서 benign 3타입의 만장일치 비율 | 각 53.3% |
| comment 작성률 | A 1.1%, B 99.3%, C 100% |

- 93.1%라는 수치는 3중 항목(98.3%)과 단일 항목(86.0%)의 혼합이다. 480개 중 300개가 1인 판단이다.
- benign edit에 대한 annotator 간 합의가 낮다 (만장일치 53%). "benign이 정말 benign인가"가 가장 약한 고리다.
- annotator 3명의 UNCERTAIN 사용 기준이 다르다 (A 0.7%, B 8.6%, C 0%).

### F. 통계 처리
- CI를 candidate 단위 bootstrap으로 계산했으나 report 단위 cluster bootstrap으로 다시 계산해도 폭이 거의 같다 (예: GREEN impression [0.893, 0.913]). 이 부분은 문제 없음.
- metric 간 차이에 대한 유의성 검정은 없다.
- seed는 0 하나만 metric 평가에 사용 (seed 1, 2는 lexical metric만).

### Audit 요약

| 심각도 | 항목 | 재제출 전 조치 |
|---|---|---|
| 치명 | A. lexical shortcut | benign 세트 재설계, lexical baseline을 본문 표에 포함 |
| 치명 | B. edit 크기 confound | edit 크기 통제 설계, headline 변경 |
| 높음 | C. 비문·off-spec 규칙 | 규칙 재작성 + 자동 validity check |
| 높음 | D. 섹션 fallback | 섹션 재파싱, 진짜 섹션이 있는 report만 사용 |
| 중간 | E. human validation | 새 쌍에 대해 전 항목 다중 annotation + 임상의 subset |
| 낮음 | F. 통계 | paired bootstrap 검정, 다중 seed |
| 필수 | 논문-코드 불일치 (`0_...md` §5) | 전부 일치시킴 |

---

## Part II. 보완 방향

### 1. Framing 전환

| | ARR May | ARR October (제안) |
|---|---|---|
| Headline | GREEN이 최강, BERTScore는 reversed | **edit 크기와 lexical overlap을 통제하면 metric 순위와 blind spot이 어떻게 달라지는가**. 최신 LLM judge도 남는 blind spot은 무엇인가 |
| Benchmark 성격 | rule 기반 minimal pair | **shortcut-controlled** minimal pair (lexical baseline이 chance 수준임을 보고) |
| Metric 범위 | 6개 + lexical | RadEval 전체 + LLM judge (open-weight, proprietary) |
| 데이터 | MIMIC-CXR (섹션 혼재) | MIMIC-CXR (정제) + IU X-Ray + 추가 corpus |
| 검증 | 대학원생 3명, text-level | + 영상의학과 전문의 subset, clinical significance 등급 |
| 외부 타당성 | 없음 | radiologist error annotation 데이터와의 연결 |

Audit A·B는 약점이지만 **스스로 발견해서 통제한 결과로 제시하면 기여가 된다**. "기존 stress test는 lexical shortcut으로 풀린다. 이를 통제한 benchmark를 제안한다"는 주장은 ReEvalMed 대비 차별점(38pP P1)과 AC의 novelty 지적에 동시에 답한다. v1 결과는 "통제 전" 조건으로 본문에 남겨 대비시킨다.

### 2. 실험 계획

우선순위: P0 = 없으면 재제출 의미 없음, P1 = 리뷰어 요구 직접 대응, P2 = 있으면 강해짐

#### E1. 데이터 재구축 (P0) — 대응: Audit C·D, 84Wq W3
- 섹션 재파싱: fallback 제거. IMPRESSION/FINDINGS 헤더가 실제로 있고 본문이 다른 report만 사용. 행정 헤더는 파싱 단계에서 제거
- 문장 분리기 교체: 약어(`Dr.`, `a.m.`), 번호 목록 처리
- 규칙 재작성
  - negation: 문장 구조별 템플릿 (`There is X` ↔ `There is no X`, `X is seen` ↔ `No X is seen`). 명사구 중간 삽입 금지
  - laterality: bilateral 제외, 병변 laterality만, 같은 문장 내 모든 언급 일관 처리 여부 명시
  - measurement: 수치 변경(예: ×2, ÷2)과 단위 변경을 별도 하위 타입으로
  - severity: 인접 등급(mild↔moderate)과 양극단(mild↔severe)을 별도 하위 타입으로 → dose-response 분석 가능
  - uncertainty: hedged↔definite 치환 위주. 삽입형은 문법 템플릿으로
  - false insertion: finding만 넣는 최소 템플릿
- 자동 validity check: 문법성(LM perplexity 증가량), reference 내 모순 여부, 중복 문장
- **평가 세트 하나로 통일**: 모든 metric이 같은 세트에서 평가. subset200/500/5k 구분 제거

#### E2. Shortcut-controlled benign 세트 (P0) — 대응: Audit A·B, AC novelty, 38pP P1·P2
- 핵심 설계: **같은 target 문장**에 대해 (changed edit, benign edit) 쌍을 만든다. 같은 reference, 같은 위치, 비슷한 edit 크기
  - 예) ref "Small left pleural effusion." / changed "Small **right** pleural effusion." / benign "Small **left-sided** pleural effusion."
- benign 유형 확장
  - lexical 동의어·약어 (pleural effusion ↔ pleural fluid, ETT ↔ endotracheal tube, cardiomegaly ↔ enlarged cardiac silhouette)
  - 통사 변형 (`No X is seen` ↔ `X is not seen`, 능동/수동)
  - LLM paraphrase + 검증 (생성 후 양방향 entailment 또는 human check)
  - format·sentence_order는 "surface 변형" 하위군으로 유지하되 별도 보고
- 보고 방식: lexical baseline(Jaccard, edit distance)을 본문 표 맨 위에 "shortcut floor"로 넣고 chance 수준임을 보임
- edit 크기 bin별 AUROC, 크기 matched AUROC

#### E3. Metric 확장 (P1) — 대응: 38pP P3, AC
| Metric | 실행 방법 | 필요 자원 |
|---|---|---|
| CRIMSON | RadEval `crimson` + `rajpurkarlab/medgemma-4b-it-crimson` (로컬) | HF 다운로드 (gated 가능성) |
| RadCliQ-v1, RadGraph-RadCliQ | RadEval (May에 import 오류로 실패) | 오류 수정 |
| SRR-BERT, RadEval-BERTScore | RadEval | tokenizer 오류 수정 |
| BERTScore 변형 | roberta-large, deberta-xlarge-mnli, rescale on/off | 로컬 |
| GEMA-Score | `OLD/external/`에 코드·가중치 있음 (복사해서 사용) | 로컬 |
| FineRadScore, CheXprompt, RadFact | GPT 계열 API 기반 | API key |
| GREEN 다른 backbone | GREEN 공개 변형 | 로컬 |

#### E4. LLM judge (P0) — 대응: 38pP P5 (post-rebuttal 핵심 우려), AC
- Open-weight (H200 143GB 1장으로 가능): Qwen 계열(2.5-7B는 캐시에 있음), Llama 3.3 70B, MedGemma 27B/4B, 기타 최신 공개 모델. vLLM 설치 필요
- Proprietary: Claude, GPT, Gemini 최신 모델 — **API key 필요**
- Prompt 변형: (a) binary rubric (b) GREEN 방식 error count (c) reasoning 포함. prompt 민감도 보고
- 연속 점수: label token logit 또는 error count 사용 (May의 0/0.5/1 세 값 문제 해결)
- identity 행도 실제로 모델에 통과시킴
- **MIMIC 데이터 사용 제약**: PhysioNet은 credentialed 데이터를 일반 상용 LLM API로 보내는 것을 금지하고, 승인된 경로(Azure OpenAI의 human review opt-out, Amazon Bedrock, Google Vertex AI 등)만 허용한다. 따라서
  - proprietary 모델은 **IU X-Ray(공개 데이터) 세트에서 평가**하거나
  - MIMIC은 승인 경로로만 실행
  - 최신 규정은 PhysioNet 공지에서 재확인 필요

#### E5. Multi-corpus (P1) — 대응: jzA1 J1, 84Wq W1
- IU X-Ray/OpenI: 전체 규모로, **모든 metric을 같은 subset**에서 (May rebuttal은 GREEN만 subset10)
- 추가 후보: CheXpert Plus, ReXGradient-160K, PadChest-GR 등. 다운로드·라이선스 확인 필요
- 보고: corpus × metric AUROC, 순위 상관(Kendall τ)

#### E6. 임상 검증 (P1) — 대응: jzA1 J2·J4, 38pP clinical
- 영상의학과 전문의가 subset(예: 타입당 20–30쌍)에 대해 (a) meaning preserved 여부 (b) clinical significance 등급
- clinical significance 가중 분석: 임상적으로 중요한 타입에서의 metric 민감도를 별도 보고
- IRB/exemption 여부 확인 (May checklist D4 = No)

#### E7. 외부 타당성 (P2) — 대응: jzA1 J3
- ReXVal 등 radiologist error annotation 데이터에서, ClinSemBench 타입별 민감도가 해당 error category에 대한 metric-radiologist 상관을 예측하는지 분석
- 데이터 다운로드 필요 (PhysioNet credentialed)

#### E8. Failure mechanism 분석 (P1) — 대응: 84Wq W2
- RadGraph: entity/relation 추출 결과에서 laterality·measurement가 어떻게 누락되는지
- GREEN: 출력한 error category가 실제 perturbation 타입과 일치하는지 (diagnosis accuracy)
- F1CheXbert: 14 label 공간 밖의 변화 비율
- uncertainty: hedged→definite와 asserted→possible 방향별 분리

#### E9. 통계 (P2)
- metric 간 paired bootstrap 검정, report-cluster CI, 다중 seed

### 3. 리뷰 지적 ↔ 실험 대응표

| 지적 | 대응 실험 |
|---|---|
| AC: novelty 제한, BERTScore는 알려진 사실 | E2 (framing 전환), E4 |
| AC / 38pP P3: 최신 metric | E3 |
| AC / 38pP P5: 최신 LLM | E4 |
| 38pP P1: ReEvalMed와의 차이 | E2 + related work 비교표 |
| 38pP P2: LLM에게 너무 쉬움 | E2, E4 |
| 38pP P4 / jzA1 J2·J4: 임상 타당성 | E6, framing |
| jzA1 J1 / 84Wq W1: 단일 corpus | E5 |
| jzA1 J3: construct validity | E7 |
| jzA1 J5: rule 상세 | E1 + 부록 rule 표 |
| jzA1 J6·J7: UNCERTAIN | rebuttal 분석 본문 반영 |
| jzA1 J8, Software 1점: release | 익명 repo + reconstruction script |
| 84Wq W2: fine-grained 분석 | E8 + per-type 표 본문 승격 |
| 84Wq W3: 데이터 구성 혼란 | E1 (세트 통일) |

### 4. 권장 실행 순서

1. E1 → E2: 새 데이터 (GPU 불필요, 가장 먼저)
2. E3 + E4(open-weight): H200에서 실행
3. E5: IU X-Ray에 같은 파이프라인 적용
4. E8, E9: 분석
5. E4(proprietary), E6, E7: 외부 자원 확보 후
6. 논문 작성 (`docs/paper/`)

### 5. 사용자 확인이 필요한 사항

| # | 질문 | 영향 |
|---|---|---|
| Q1 | ARR October 제출 마감일 | 실험 범위 결정 |
| Q2 | proprietary LLM API key 제공 가능 여부 (Claude / GPT / Gemini), MIMIC용 승인 경로(Bedrock, Vertex, Azure) 사용 가능 여부 | E4 |
| Q3 | 영상의학과 전문의 annotation 가능 여부와 규모 | E6 |
| Q4 | 새 쌍에 대한 human annotation을 다시 할 수 있는지 (기존 480쌍 라벨은 구 규칙 기준) | E1·E2 검증 |
| Q5 | 추가 corpus(CheXpert Plus, ReXGradient 등)와 ReXVal 다운로드 가능 여부 | E5, E7 |
| Q6 | 같은 리뷰어 재배정 요청 여부 | revision note 작성 방향 |
| Q7 | MIMIC-CXR 원본 txt가 필요할 때 이 서버로 가져올 수 있는지 (현재는 전처리 CSV만 있음) | E1 |

Q2·Q3·Q5가 불가능한 경우에도 E1, E2, E3(로컬 가능분), E4(open-weight), E5(IU X-Ray), E8, E9는 현재 서버 자원만으로 진행할 수 있다.
