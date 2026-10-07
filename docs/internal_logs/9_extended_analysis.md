# 9. 확장 분석 — 하위 타입, surface dose-response, 대비 검정, 혼합효과, CRIMSON 오류 귀속(E8), robustness

- 작성: 2026-10-03
- 코드: `scripts/14_extended_analysis.py` (env: `envs/llm`, statsmodels), 그림 `scripts/17_make_figures.py`
- 결과: `results/2_full_{iu,mimic}/extended/{A_subtypes, B_surface_dose_response, C_contrasts, D_mixed_effects, E_crimson_attribution, F_robustness_subsets}.csv`, `EXTENDED.md`
- 그림: `figures/paper/{fig2_confound_vs_controlled, fig3_meaning_vs_surface, fig_dose_response}.{pdf,png}`
- 주의: gpt-oss-20b는 재실행 중이라 이 문서의 표에서 제외했다 (문서 8 §6). 재실행 후 같은 스크립트로 갱신한다.

---

## A. 하위 타입 (통제 S0 paired accuracy, IU / MIMIC)

### A1. severity — 인접 등급 vs 양극단 (dose-response)

| Metric | adjacent (mild→moderate) | extreme (mild→severe) |
|---|---|---|
| Jaccard | 0.71 / 0.72 | 0.76 / 0.63 |
| BERTScore distilbert | **0.00 / 0.08** | 0.14 / 0.16 |
| BERTScore roberta-large | 0.21 / 0.19 | 0.26 / 0.32 |
| BERTScore deberta-mnli | 0.32 / 0.36 | 0.72 / 0.79 |
| RadGraph | 0.33 / 0.30 | 0.33 / 0.45 |
| RadCliQ-v1 | 0.31 / 0.28 | 0.40 / 0.34 |
| RaTEScore | 0.56 / 0.53 | 0.74 / 0.74 |
| GREEN | 0.83 / 0.82 | 0.98 / 0.82 |
| CRIMSON | 0.81 / 0.83 | 0.99 / 0.95 |
| Llama-3.1-8B | 0.76 / 0.64 | 0.92 / 0.80 |
| gemma-3-27b | 0.90 / 0.81 | 0.99 / 0.89 |
| Qwen3-32B | 0.92 / 0.88 | 0.99 / 0.89 |

- LLM 계열은 양극단이 인접보다 쉽다(dose-response가 있음). embedding·graph metric은 **둘 다 chance 미만**: 등급 단어(mild/moderate/severe)끼리는 embedding이 가깝고, 동의어 P(`slight`, `small-sized`)가 더 멀다.
- 단 severity P lexicon의 약 2/3가 전문의 확인 대상(§F). 확인 대상을 빼도 방향은 같다.

### A2. measurement — value vs unit

| Metric | value (P `47 mm` / C `94 mm`) | unit (P `47 mm` / C `47 cm`) |
|---|---|---|
| Jaccard | 0.67 / 0.49 | **0.01 / 0.01** |
| BERTScore distilbert | 0.87 / 0.75 | 0.00 / 0.00 |
| RadCliQ-v1 | 0.76 / 0.69 | 0.16 / 0.11 |
| RaTEScore | 0.78 / 0.60 | 0.19 / 0.25 |
| GREEN | 0.81 / 0.80 | 0.64 / 0.84 |
| CRIMSON | 0.72 / 0.77 | 0.75 / 0.67 |
| gemma-3-27b | 0.54 / 0.74 | 0.61 / 0.69 |
| Qwen3-32B | 0.80 / 0.53 | 0.82 / 0.54 |

- **알려진 결함 (D-1)**: `unit` 하위타입은 surface가 맞춰지지 않았다. P는 값과 단위 2토큰을 바꾸고(`4.7 cm → 47 mm`) C는 값 1토큰만 바꾼다(`4.7 cm → 47 cm`). 그래서 meaning-blind Jaccard가 0.01이고, lexical·embedding metric의 낮은 수치는 "P가 더 많이 바뀌었다"를 따라간 것이다. 이 하위타입은 **통제 조건이 아니라 혼동(역방향) 조건**으로 보고해야 한다. `value` 하위타입(둘 다 2토큰)은 통제되어 있다.
- 원인: 생성기 v4에서 measurement 변형을 "숫자가 P·C 모두에서 바뀌도록" 고치면서 `magnitude` 변형의 토큰 수 불일치를 허용(`MAX_EDIT_DIFF=1`).
- 조치: (i) 본 문서 §F에서 이 하위타입을 제외한 수치를 병기 (ii) 다음 생성 버전에서는 `4.7 cm → 4.7 centimeters`(P, 1토큰) vs `4.7 cm → 4.7 mm`(C, 1토큰)로 교체. full 세트는 annotation 때문에 동결되어 있어 재생성하지 않는다.
- LLM judge·CRIMSON이 단위 변환 P를 "변경"으로 판정하는 현상(문서 8 §4)은 이 결함과 무관하게 성립한다 (P 자체에 대한 판정).

### A3. uncertainty — 방향

| Metric | hedged→definite | definite→hedged |
|---|---|---|
| GREEN | 0.56 / 0.57 | 0.55 / 0.50 |
| CRIMSON | 0.58 / 0.59 | 0.50 / 0.50 |
| Llama-3.1-8B | 0.61 / 0.59 | 0.64 / 0.58 |
| gemma-3-27b | 0.89 / 0.94 | 0.98 / 0.86 |
| Qwen3-32B | 0.84 / 0.90 | 0.80 / 0.70 |
| BERTScore deberta-mnli | 0.77 / 0.90 | 1.00 / 0.91 |

- GREEN·CRIMSON은 두 방향 모두 chance 근처. §E에서 보듯 CRIMSON은 certainty 오류를 **탐지는 하지만 점수에 거의 반영하지 않는다**.

### A4. negation — 방향
- 대부분 metric이 양방향 0.8 이상. Jaccard/token F1/ROUGE는 0.44–0.69. F1CheXbert는 negated→present만 0.66 / 0.67 (present→negated 0.50).

---

## B. Surface dose-response (S2) — `fig_dose_response`

P2(의미 보존 + context paraphrase)에 붙는 추가 penalty `z(Δ(P2) − Δ(P0))`를 "다시 쓴 토큰 비율" 4분위별로 본 것 (IU, Q1 → Q4; MIMIC도 같은 모양).

| Metric | Q1 (0.28) | Q2 (0.51) | Q3 (0.66) | Q4 (0.95) |
|---|---|---|---|---|
| BERTScore distilbert | 0.95 | 1.70 | 2.02 | 2.67 |
| RadCliQ-v1 | 0.95 | 1.58 | 1.95 | 2.50 |
| RadGraph | 0.87 | 1.36 | 1.68 | 2.07 |
| RaTEScore | 0.50 | 0.86 | 1.01 | 1.19 |
| GREEN | 0.28 | 0.23 | 0.52 | 0.53 |
| CRIMSON | 0.00 | 0.01 | −0.00 | 0.00 |
| gemma-3-27b judge | −0.22 | −0.27 | −0.31 | −0.18 |
| Qwen3-32B judge | −0.19 | −0.21 | −0.13 | −0.13 |

- surface 지배형 metric의 penalty는 **다시 쓴 양에 비례해 단조 증가**한다. 의미는 그대로다(NLI + 어휘 guard 통과; 사람 검증 대기).
- 같은 구간에서 통제 paired accuracy(C2 vs P2)는 거의 평평하다(BERTScore 0.61–0.69, RadCliQ 0.71–0.75, CRIMSON 0.79–0.83). 즉 **paraphrase는 의미 신호를 지우지 않고 penalty의 바닥만 올린다** → 혼동 조건(C0 vs P2)에서 역전이 생기는 메커니즘.
- GREEN만 Q1 0.80 → Q3 0.72로 떨어진다.

---

## C. 대비 검정 (report-cluster bootstrap 95% CI)

### C1. meaning-blind 기준선(Jaccard)을 넘는가 — 통제 S0, `paired acc − Jaccard paired acc`

| | IU | MIMIC |
|---|---|---|
| **유의하게 위** | BERTScore-roberta +0.04, BERTScore-deberta +0.16, RaTEScore +0.05, RadCliQ +0.10, CRIMSON +0.18, GREEN +0.22, Llama +0.15, gemma +0.29, Qwen3 +0.30 | BERTScore-distilbert +0.03, -roberta +0.07, -deberta +0.22, RaTEScore +0.07, RadCliQ +0.10, SRR-BERT +0.03, CRIMSON +0.25, GREEN +0.24, Llama +0.15, gemma +0.31, Qwen3 +0.28 |
| **구별 안 됨** (CI가 0 포함) | BERTScore-distilbert +0.03 [−0.00, 0.06], token F1 | RadGraph −0.02 [−0.04, 0.01], token F1 |
| **유의하게 아래** | **RadGraph −0.06**, **F1CheXbert −0.11**, **Temporal −0.11**, BLEU −0.07, SRR-BERT −0.03, ROUGE-L −0.02 | **F1CheXbert −0.07**, **Temporal −0.05**, ROUGE-L −0.06, BLEU −0.02 |

### C2. paraphrase 잡음에서 떨어지는가 — `S0 − S2`

| Metric | IU | MIMIC |
|---|---|---|
| GREEN | **+0.088 [0.068, 0.108]** | **+0.080 [0.061, 0.099]** |
| Llama-3.1-8B judge | +0.032 [0.015, 0.049] | +0.026 [0.011, 0.040] |
| Qwen3-32B judge | +0.018 [0.003, 0.033] | −0.017 [−0.033, −0.003] |
| gemma-3-27b judge (errors prompt, IU) | +0.202 [0.178, 0.226] | – |
| 그 외 전부 | CI가 0 포함 | CI가 0 포함 (BERTScore-roberta는 −0.04로 오히려 상승) |

---

## D. 혼합효과 모형 `z(Δ) ~ meaning × surface + (1 | report)`

- 19개 metric 중 4개는 MixedLM, 15개는 random-effects 적합이 singular여서 report-cluster robust OLS로 대체 (`model` 열에 기록).
- 계수는 문서 8 §3의 평균 차와 일치한다 (IU): meaning 주효과 — CRIMSON 0.95, GREEN 1.20, gemma 1.47, Qwen3 1.69 vs BERTScore 0.03–0.23, RadGraph 0.09, RadCliQ 0.15. surface S2 주효과 — BERTScore 1.62–1.83, RadCliQ 1.74, RadGraph 1.49 vs CRIMSON 0.00, GREEN 0.39.
- 상호작용(meaning × S2): GREEN −0.24, Llama −0.22, gemma-errors −0.67. 나머지는 |0.03| 이하 → **surface는 대부분 metric에서 의미 민감도를 바꾸지 않고 가산적으로 penalty를 더한다**.

---

## E. CRIMSON 오류 귀속 (E8 메커니즘)

CRIMSON이 출력한 오류 범주별 개수로, 각 칸에서 "오류가 1개 이상 / 기대 범주가 발화"한 비율 (IU / MIMIC).

| edit type | 기대 범주 | C0: 오류 ≥1 | C0: 기대 범주 | P0: 오류 ≥1 (오경보) |
|---|---|---|---|---|
| laterality | location | 0.92 / 0.93 | 0.91 / 0.93 | 0.05 / 0.01 |
| anatomy | location | 0.95 / 0.97 | 0.94 / 0.97 | 0.11 / 0.09 |
| severity | severity | 0.99 / 1.00 | 0.99 / 0.99 | **0.52 / 0.54** |
| measurement | measurement | 0.96 / 0.85 | 0.95 / 0.83 | **0.63 / 0.70** |
| uncertainty | certainty | 0.98 / 0.92 | 0.96 / 0.91 | **0.52 / 0.49** |
| negation | false / missing finding | 0.95 / 0.91 | 0.92 / 0.86 | 0.00 / 0.01 |
| temporal | temporal | **0.67 / 0.84** | **0.45 / 0.65** | 0.13 / 0.05 |

- **탐지와 점수의 괴리**: uncertainty flip은 91–96%에서 certainty 오류로 정확히 분류되지만 CRIMSON *점수*의 paired accuracy는 0.54–0.57이다. certainty 오류의 가중치가 낮아 점수가 거의 움직이지 않는다 (CRIMSON의 설계). "blind"가 아니라 "가중치로 무시".
- **temporal은 범주 귀속이 약하다**: 탐지 67–84%, temporal 범주로는 45–65%, 17–19%는 false finding으로 잘못 분류.
- **P0 오경보가 타입 특이적**: 단위 변환 63–70%, severity 동의어 52–54%, hedge 동의어 49–52%. LLM judge의 타입별 오경보(문서 8 §4)와 같은 세 타입이다 → 이 세 타입의 P lexicon이 "실제로는 의미를 바꾼다"고 여러 모델이 본다는 뜻이기도 하므로 **전문의 판정이 결정적**이다.
- GREEN의 오류 범주 분석은 RadEval per-sample 출력에 범주가 없어 별도 실행이 필요 (TODO).

---

## F. Robustness — 알려진 결함과 전문의 확인 대상 제외 (통제 S0 paired accuracy)

| Metric | 전체 (IU 890 / MIMIC 1,050) | measurement:unit 제외 (841 / 975) | 확인 대상 lexicon 제외 (724 / 854) | 셋 다 제외 (673 / 773) |
|---|---|---|---|---|
| Jaccard | 0.630 / 0.591 | 0.666 / 0.636 | 0.620 / 0.570 | 0.664 / 0.625 |
| BERTScore distilbert | 0.658 / 0.626 | 0.697 / 0.674 | 0.735 / 0.666 | 0.789 / 0.730 |
| BERTScore deberta-mnli | 0.790 / 0.811 | 0.813 / 0.851 | 0.833 / 0.847 | 0.865 / 0.899 |
| RadGraph | 0.568 / 0.573 | 0.573 / 0.587 | 0.601 / 0.609 | 0.609 / 0.627 |
| RaTEScore | 0.678 / 0.658 | 0.706 / 0.689 | 0.681 / 0.667 | 0.715 / 0.706 |
| RadCliQ-v1 | 0.725 / 0.690 | 0.757 / 0.734 | 0.775 / 0.715 | 0.819 / 0.772 |
| F1CheXbert | 0.520 / 0.526 | 0.521 / 0.528 | 0.525 / 0.531 | 0.527 / 0.534 |
| GREEN | 0.852 / 0.830 | 0.864 / 0.829 | 0.853 / 0.835 | 0.869 / 0.835 |
| CRIMSON | 0.809 / 0.838 | 0.813 / 0.851 | 0.805 / 0.840 | 0.808 / 0.856 |
| Llama-3.1-8B | 0.779 / 0.741 | 0.782 / 0.737 | 0.785 / 0.753 | 0.788 / 0.747 |
| gemma-3-27b | 0.917 / 0.904 | 0.935 / 0.921 | 0.914 / 0.910 | 0.937 / 0.930 |
| Qwen3-32B | 0.933 / 0.869 | 0.939 / 0.894 | 0.939 / 0.869 | 0.949 / 0.902 |

- "셋 다 제외" = measurement:unit + 어색한 negation fragment(IU 2, MIMIC 6) + 전문의 확인 대상 P lexicon 전부(최악의 경우: 전부 기각).
- 결론은 유지된다: BERTScore reversal 소멸(0.73–0.79로 오히려 더 올라감), RadGraph는 Jaccard와 같거나 아래(0.61 vs 0.66 / 0.63 vs 0.63), F1CheXbert 0.53, GREEN > CRIMSON ≈ 0.81–0.87, judge 0.75–0.95.
- embedding 계열은 확인 대상 lexicon(주로 severity)을 빼면 0.07–0.13 오른다 → severity의 "chance 미만" 결과(§A1)는 lexicon 판정에 민감하다. 본문에는 전문의 승인 후 수치를 쓴다.

### 알려진 결함 목록

| ID | 결함 | 규모 | 처리 |
|---|---|---|---|
| D-1 | measurement:unit 하위타입의 P·C 토큰 수 불일치 | IU 49 / MIMIC 75 target | 혼동(역방향) 예시로 따로 보고. §F에 제외 수치. 다음 버전에서 규칙 교체 |
| D-2 | negation N3가 `No X identified.`를 fragment로 처리 → `X identified is absent.` | IU 2 / MIMIC 6 target (1.7% / 4.0% of negation) | 생성기 v6에서 제외 규칙 추가(동결 세트는 그대로). §F에 제외 수치 |
| D-3 | 통제 S0의 type-aware surface leak (C는 원 토큰 삭제, P는 유지) | Jaccard paired acc 0.59–0.63 | meaning-blind 기준선으로 모든 표에 병기. §C1에서 기준선 대비 검정 |
| D-10 | 원문이 이미 `right sided`(하이픈 없음)인 문장에 laterality 규칙이 적용되어 `right-sided sided` 생성 | IU 2 / MIMIC 0 target (10/7 집계, `results/2_full_iu/review1007/E_defect_D10_targets.csv`) | 재생성하지 않음. Limitations 기재, IU 공개본에서 제거 |
| D-11 | S2 paraphrase의 정도 표현 drift (`large` → `significant`) | 정도 표현 multiset이 바뀐 target: IU 124/890, MIMIC 258/1,050 | P·C에 동일하게 들어가 통제 비교에는 영향이 작다. 정도 표현 보존 subset과 다른 계열 paraphraser + guard로 GREEN 결론을 재확인 (문서 13 §3.4) |
| D-12 | 초안 §4.2의 "measurement는 device 서술을 피한다"는 사실과 다름 | MIMIC measurement target의 88%가 tube·catheter 위치 | 데이터 결함이 아니라 서술 오류. 논문 §4.2·§4.4 수정 (문서 13 §3.5) |

---

## G. 그림

| 파일 | 내용 | 설계 |
|---|---|---|
| `fig2_confound_vs_controlled` | metric별 혼동(v1형, 빈 원) → 통제(S0, 찬 원) paired accuracy, corpus별 패널 | dumbbell(항목별 before→after), 1 hue 2 표현(채움/비움), chance 선 |
| `fig3_meaning_vs_surface` | 의미 효과(x) × surface 효과(y) 산점도 | 3개 범주색(검증된 팔레트 1–3번), 전 점 직접 라벨, 밀집 군집은 leader line |
| `fig_dose_response` | 다시 쓴 비율 4분위별 P2 추가 penalty | 선 + 끝점 직접 라벨, 범주색 |

- gpt-oss 재실행·추가 judge가 끝나면 `17_make_figures.py`를 다시 실행한다.
- dataviz 팔레트 검증 스크립트는 node가 없어 실행하지 못했다. 문서화된 검증 팔레트의 1–3번 슬롯(all-pairs 검증됨)만 사용했다.

---

## H. 진행 중인 확장 실험 (결과는 문서 10에 기록 예정)

| 실험 | 내용 | 상태 |
|---|---|---|
| X1b omission / insertion (MIMIC) | C: finding 문장 삭제 / 타 report의 finding 문장 추가. P: 비임상 문장(촬영 기법·비교 문구) 삭제 / 기존 문장의 재서술 추가. 같은 문장 단위 연산 | `15_generate_omission_insertion.py`, `run_oi.sh` 실행 중. IU는 비임상 문장이 29건뿐이라 제외 |
| X1c monotonicity at fixed surface (MIMIC) | 한 섹션에 서로 다른 타입의 matched edit 3개. M0=PPP, M1=CPP, M2=CCP, M3=CCC — surface 동일, 의미 변경 개수만 0→3 | `16_generate_monotonicity.py` 300 target 생성 완료(IU는 19건뿐). `run_set.sh mimicmono` 채점 중 |
| 추가 judge | gpt-oss-120b (rubric 두 corpus, errors IU), Qwen3-32B thinking, Qwen3-32B errors | `run_judges_extra.sh` 대기 (GPU 공유로 지연) |
| gpt-oss-20b 재실행 | 최종 채널 파싱 | `run_gptoss_rerun.sh` 실행 중 |

GPU 경합 대응: `scripts/gpu_wait.sh`에 파일 lock 추가(우리 큐끼리 동시에 통과해 서로 OOM 내던 문제). 다른 프로젝트(CAP) 작업은 lock을 쓰지 않으므로 재시도는 유지.
