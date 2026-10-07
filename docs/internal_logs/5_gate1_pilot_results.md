# 5. Gate 1 — pilot 결과 (IU X-Ray 279 target, MIMIC-CXR 280 target)

- 작성: 2026-10-01 (계획상 Gate 1은 10/4. pilot이 일찍 끝나 앞당겨 판단)
- 데이터: `data/pairs/pilot_{iu,mimic}_all.csv` (target당 7칸: identity, P0, C0, P1, C1, P2, C2)
- 결과 파일: `results/1_pilot_{iu,mimic}/analysis/{REPORT.md, JUDGES.md, summary_by_condition.csv, per_type.csv, decomposition.csv, judge_cells*.csv}`
- 코드: `scripts/7_score_metrics.py`, `9_llm_judge.py`, `10_crimson.py`, `8_analyze_factorial.py`, `11_judge_cells.py`
- 지표: **paired accuracy** = 같은 target에서 Δ(C) > Δ(P)인 비율(동점 0.5). chance = 0.5

---

## 1. Gate 1 판정

| 조건 | 기준 | 결과 | 판정 |
|---|---|---|---|
| 전제 1 | 통제 조건 surface-only 분류기 0.45–0.55 | S2: IU 0.544 / MIMIC 0.517 ✅. S0·S1: 0.60 / 0.58–0.60 (0.05 초과) | **부분 충족**. type-blind 기준. 문서 4 §4 |
| 전제 2 | P·C 후보 비문·모순 < 5% | 타입별 표본을 눈으로 확인(문서 4). 체계적 50개 검수는 사람 검증 단계에서 | 잠정 충족 |
| 진행 1 | 혼동↔통제 사이 metric 순위 변화 | BERTScore 0.01 → 0.66–0.79, RadCliQ 0.12 → 0.70, RadGraph 0.34 → 0.57 | ✅ |
| 진행 2 | LLM judge의 P0 오경보 또는 C2 누락 잔존 | gemma-3-27b P0 오경보 23–28%, Llama-3.1-8B P1 오경보 61–63%, uncertainty C2 탐지 33–38% | ✅ (단 최강 judge는 천장 근처, §4) |
| 중단 | 모든 judge가 전 칸 천장 + 순위 v1과 동일 | 해당 없음 | – |

**결론: GO.** Full 세트 생성·채점을 시작했다 (`scripts/run_full.sh`). 사용자 측 조건(U2 annotator 확보)은 별도 확인 필요.

---

## 2. 핵심 결과 1 — 혼동 조건 vs 통제 조건 (paired accuracy)

### IU X-Ray pilot

| Metric | confound v1형 (C0 vs P1) | confound ReEvalMed형 (C0 vs P2) | controlled S0 | controlled S1 | controlled S2 |
|---|---|---|---|---|---|
| *Jaccard (meaning-blind)* | 0.629 | 0.036 | 0.629 | 0.629 | 0.634 |
| *token F1 (meaning-blind)* | 0.633 | 0.036 | 0.633 | 0.633 | 0.645 |
| BLEU | 0.022 | 0.014 | 0.550 | 0.556 | 0.552 |
| ROUGE-L | 0.000 | 0.018 | 0.582 | 0.538 | 0.582 |
| BERTScore (distilbert, v1 설정) | **0.007** | 0.022 | **0.659** | 0.663 | 0.670 |
| BERTScore (roberta-large) | 0.014 | 0.014 | 0.667 | 0.670 | 0.663 |
| BERTScore (deberta-xlarge-mnli) | 0.036 | 0.057 | 0.792 | 0.767 | 0.792 |
| F1CheXbert | 0.514 | 0.513 | 0.522 | 0.514 | 0.516 |
| Temporal | 0.543 | 0.461 | 0.543 | 0.543 | 0.543 |
| SRR-BERT | 0.597 | 0.527 | 0.608 | 0.609 | 0.608 |
| RadGraph | 0.339 | 0.059 | 0.566 | 0.602 | 0.565 |
| RaTEScore | 0.647 | 0.176 | 0.694 | 0.683 | 0.694 |
| RadCliQ-v1 | 0.118 | 0.047 | 0.703 | 0.720 | 0.724 |
| GREEN | 0.737 | 0.701 | 0.835 | 0.796 | 0.763 |
| CRIMSON (MedGemma-4B) | 0.811 | 0.815 | 0.811 | 0.815 | 0.808 |
| Llama-3.1-8B judge | 0.670 | 0.756 | 0.772 | 0.681 | 0.720 |
| gemma-3-27b judge | 0.900 | 0.946 | 0.894 | 0.851 | 0.909 |
| gpt-oss-20b judge | 0.970 | 0.970 | 0.968 | 0.970 | 0.946 |

### MIMIC-CXR pilot (GREEN S0S1, BERTScore S2는 GPU OOM으로 재채점 중 → 빈칸)

| Metric | confound v1형 | confound ReEvalMed형 | controlled S0 | controlled S1 | controlled S2 |
|---|---|---|---|---|---|
| *Jaccard* | 0.584 | 0.020 | 0.584 | 0.584 | 0.591 |
| BERTScore (distilbert) | 0.000 | – | 0.600 | 0.579 | – |
| BERTScore (deberta-mnli) | 0.011 | – | 0.764 | 0.782 | – |
| F1CheXbert | 0.521 | 0.479 | 0.530 | 0.534 | 0.537 |
| RadGraph | 0.289 | 0.043 | 0.577 | 0.614 | 0.605 |
| RaTEScore | 0.561 | 0.082 | 0.614 | 0.613 | 0.623 |
| RadCliQ-v1 | 0.104 | 0.029 | 0.693 | 0.675 | 0.704 |
| CRIMSON | 0.818 | 0.825 | 0.829 | 0.830 | 0.830 |
| Llama-3.1-8B judge | 0.639 | 0.732 | 0.754 | 0.677 | 0.714 |
| gemma-3-27b judge | 0.934 | 0.957 | 0.920 | 0.866 | 0.912 |
| gpt-oss-20b judge | 0.982 | 0.966 | 0.977 | 0.977 | 0.948 |

### 읽는 법
1. **BERTScore "reversal"은 artefact다.** v1형 혼동 조건에서 0.00–0.04(완전 역전)이던 BERTScore가 surface를 맞춘 통제 조건에서는 0.60–0.79로 chance를 넘는다. v1 논문의 headline(AUROC 0.22/0.17)은 benchmark 구성이 만든 결과였다.
2. **혼동의 방향은 구성이 정한다.** Jaccard는 v1형에서 0.63(정방향처럼 보임), ReEvalMed형에서 0.04(역방향). 같은 metric, 같은 target, P 칸만 다르다.
3. **순위가 바뀐다.** IU 기준 비-LLM metric 순위
   - v1형 혼동: RaTEScore 0.65 > Jaccard 0.63 > SRR-BERT 0.60 > Temporal 0.54 > F1CheXbert 0.51 > RadGraph 0.34 > RadCliQ 0.12 > BERTScore 0.01
   - 통제 S0: BERTScore-deberta 0.79 > RadCliQ 0.70 > RaTEScore 0.69 > BERTScore-roberta 0.67 > Jaccard 0.63 > SRR-BERT 0.61 > RadGraph 0.57 > Temporal 0.54 > F1CheXbert 0.52
4. **통제 조건에서도 약하다.** RadGraph(0.57), F1CheXbert(0.52), Temporal(0.54), SRR-BERT(0.61)는 meaning-blind Jaccard(0.63)를 넘지 못한다. 이 metric들이 v1에서 보인 "의미 민감도"의 상당 부분은 surface 차이였다.
5. **GREEN은 surface 잡음에 약해진다.** 0.835 (S0) → 0.796 (S1) → 0.763 (S2) → 0.701 (C0 vs P2). CRIMSON은 0.81로 일정.
6. Jaccard가 통제 조건에서 0.58–0.63인 이유: C는 원 토큰을 지우고(`left`→`right-sided`) P는 원 토큰을 남기는(`left-sided`) 경우가 많다. 단어 치환 설계의 잔여 비대칭이며 "meaning-blind 기준선"으로 모든 표에 함께 보고한다.

---

## 3. 핵심 결과 2 — 의미 효과와 surface 효과의 분해 (IU, z-scored Δ)

| Metric | 의미 효과 (C0−P0) | surface S1 (P1−P0) | surface S2 (P2−P0) | 의미 효과 @S2 (C2−P2) |
|---|---|---|---|---|
| BLEU | 0.01 | 0.34 | 1.93 | 0.01 |
| ROUGE-L | 0.03 | 1.97 | 1.39 | 0.03 |
| BERTScore (distilbert) | 0.04 | 1.20 | 1.85 | 0.05 |
| BERTScore (roberta-large) | 0.08 | 1.45 | 1.82 | 0.08 |
| BERTScore (deberta-mnli) | 0.24 | 1.57 | 1.62 | 0.21 |
| RadGraph | 0.11 | 0.33 | 1.57 | 0.08 |
| RadCliQ-v1 | 0.18 | 0.75 | 1.78 | 0.17 |
| RaTEScore | 0.12 | 0.11 | 0.87 | 0.14 |
| F1CheXbert | 0.23 | 0.08 | 0.10 | 0.18 |
| SRR-BERT | 0.50 | 0.05 | 0.31 | 0.49 |
| GREEN | 1.14 | 0.24 | 0.42 | 0.93 |
| CRIMSON | 0.97 | 0.01 | −0.00 | 0.94 |
| Llama-3.1-8B judge | 1.11 | 0.70 | 0.23 | 0.83 |
| gemma-3-27b judge | 1.40 | 0.06 | −0.24 | 1.40 |
| gpt-oss-20b judge | 1.85 | −0.02 | 0.01 | 1.77 |

- Fig 3(의미 민감도 × surface 민감도 산점도)의 원자료. 세 군집이 보인다.
  - **surface 지배형**: BLEU, ROUGE, BERTScore, RadGraph, RadCliQ — surface 효과가 의미 효과의 5–100배
  - **둔감형**: F1CheXbert, Temporal, RaTEScore — 둘 다 작음
  - **의미 지배형**: CRIMSON, gpt-oss, gemma — 의미 효과 ≥ 1 SD, surface ≈ 0. GREEN과 Llama-8B는 의미 효과는 크지만 surface 효과도 0.2–0.7

---

## 4. 핵심 결과 3 — LLM judge의 칸별 "CHANGED" 판정률 (rubric prompt)

P 칸과 identity는 0이어야 하고(오경보), C 칸은 1이어야 한다(탐지).

| Judge | corpus | identity | P0 | P1 | P2 | C0 | C1 | C2 |
|---|---|---|---|---|---|---|---|---|
| Llama-3.1-8B | IU | 0.007 | 0.158 | **0.606** | 0.287 | 0.667 | 0.889 | 0.706 |
| Llama-3.1-8B | MIMIC | 0.007 | 0.154 | **0.632** | 0.250 | 0.646 | 0.868 | 0.668 |
| gemma-3-27b | IU | 0.000 | **0.229** | 0.269 | 0.104 | 0.910 | 0.889 | 0.817 |
| gemma-3-27b | MIMIC | 0.000 | **0.279** | 0.261 | 0.093 | 0.936 | 0.889 | 0.800 |
| gpt-oss-20b | IU | 0.000 | 0.039 | 0.029 | 0.047 | 0.961 | 0.957 | 0.928 |
| gpt-oss-20b | MIMIC | 0.004 | 0.046 | 0.043 | 0.104 | 0.986 | 0.975 | 0.954 |

타입별 주요 실패 (IU)

| 현상 | 수치 |
|---|---|
| **단위 변환을 의미 변경으로 판정** (4.7 cm → 47 mm) | P0 measurement 오경보: gemma-3-27b 0.88, Llama-8B 0.78, gpt-oss 0.00 |
| **문장 순서만 바꿔도 오경보** | Llama-8B P1: anatomy 0.68, severity 0.70, laterality 0.60 |
| severity 동의어(small-sized, slight 등)를 변경으로 판정 | P0 severity: gemma 0.33, gpt-oss 0.15 (P lexicon 자체가 틀렸을 가능성 → 전문의 확인 대상) |
| **약어 안의 flip을 놓침** (LLL vs RLL/LUL) | Llama-8B C0 anatomy 0.47, laterality 0.50 |
| **paraphrase 잡음 속 uncertainty flip 누락** | C2 uncertainty: gemma 0.33, Llama 0.38, gpt-oss 0.80 |
| paraphrase 잡음 속 laterality flip 누락 | C2 laterality: gpt-oss 0.85 (C0 0.97) |

답해야 할 질문(계획 §6.1)에 대한 pilot 답
1. C0 vs P0에서 saturate하는가 → gpt-oss-20b는 0.97로 거의 천장. gemma 0.89–0.92, Llama 0.75–0.77은 아님.
2. edit 크기를 맞춘 P0에서도 오경보가 남는가 → **남는다.** gemma 23–28%, Llama 15–16%, gpt-oss 4–5%. 특히 measurement(단위 변환)과 severity. "LLM judge가 무해한 재서술을 과하게 벌점"(Beyond Scalar Scores)은 surface 크기 효과만이 아니라 **특정 타입의 동치 판단 실패**다.
3. C2에서 flip을 놓치는가 → uncertainty와 laterality에서 놓친다. S0 대비 S2 탐지율 하락: gemma 0.91→0.82, gpt-oss 0.96→0.93.

### 위험
- 가장 강한 open-weight judge(gpt-oss-20b)가 이미 0.95–0.98이다. proprietary 최신 모델은 천장에 닿을 가능성이 높다. 그 경우 judge 결과의 메시지는 "강한 judge는 통과, 중간급 judge와 학습형 metric(GREEN)은 surface·타입 특이적 실패"가 된다. 논문의 주 기여는 §2–§3(혼동과 분해)이므로 성립하지만, 38pP P2("LLM에게 너무 쉽다")에는 "그렇다, 그리고 그것을 통제된 조건에서 처음 보였다 + 남는 실패는 uncertainty·단위 변환"으로 답하게 된다.
- severity P lexicon(small-sized, large-volume, trace↔minimal)은 gpt-oss도 15% 오경보 → lexicon이 실제로 의미를 바꿨을 수 있다. 전문의 승인(§6.5) 결과에 따라 해당 target 제거.

---

## 5. v1 대비 수정 사항 재확인

| v1 문제 (문서 2) | pilot에서의 상태 |
|---|---|
| A. Jaccard가 GREEN과 동급 (0.81 vs 0.81) | 통제 조건: Jaccard 0.63 vs GREEN 0.84 vs gpt-oss 0.97. meaning-blind 기준선을 모든 표에 포함 |
| B. BERTScore reversal = edit 크기 confound | 통제 조건에서 소멸 (0.01 → 0.66–0.79) |
| C. 비문 candidate | 문장 구조별 템플릿으로 교체. 삽입형 negation·uncertainty 삭제 |
| D. findings == impression 55% | fallback 제거, 0% |
| identity 하드코딩 (LLM judge) | identity도 모델 통과. 오경보 0–0.7% |
| BERTScore backbone 미기재 | 3종 명시 비교 |

---

## 6. 실패·미완 기록

| 항목 | 상태 |
|---|---|
| RadEval-BERTScore | 4회 모두 실패 (`data did not match any variant of untagged enum ModelWrapper`: tokenizers 버전 불일치). v1과 동일 오류. **제외**하고 Limitations에 기재 |
| Qwen3-32B judge | bf16: GPU 경합으로 3회 실패(OOM / KV 부족). FP8: `deepgemm` JIT가 CUDA toolkit(nvcc) 요구 → 실행 불가. GPU 여유 시 bf16으로 재실행 대기 (`run_queue4.sh`) |
| MIMIC pilot GREEN(S0S1), BERTScore(S2) | 다른 프로젝트와의 GPU 경합으로 OOM → 재채점 중 |
| errors prompt (GREEN식) | 대기 중 |
| MedGemma-27b / Llama-3.3-70B | HF 라이선스 미동의(403) — 사용자 조치 필요 |
| proprietary judge | API key 없음 — 사용자 조치 필요 (IU만) |

---

## 7. Full 세트 (진행 중)

| | IU X-Ray | MIMIC-CXR |
|---|---|---|
| target 수 | 890 | 1,050 |
| 타입별 | anatomy 150, laterality 146, measurement 94, negation 119, severity 137, temporal 150, uncertainty 94 | 각 150 |
| report 수 | 714 | 1,037 |
| 부정 문장 target (laterality/anatomy/measurement) | 0–6% | 0% |
| 전문의 확인 필요 P lexicon 비율 | anatomy 33%, severity 69%, uncertainty 24% | 33%, 66%, 31% |

- 생성기 v5: `target_negated` 플래그 추가, 샘플러가 laterality·anatomy·measurement에서 비부정 문장 우선
- IU는 measurement·uncertainty가 94개로 공급 한계 (계획 §5.4에서 예상)
- 파이프라인: `scripts/run_full.sh` (paraphrase → floor → metric 병렬 채점 → CRIMSON → judges)
