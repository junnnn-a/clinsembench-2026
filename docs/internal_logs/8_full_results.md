# 8. Full 세트 결과 (X1 + X2 open-weight + X4)

- 작성: 2026-10-03
- 데이터: `data/pairs/full_{iu,mimic}_all.csv` — IU X-Ray 890 target / 6,230행, MIMIC-CXR 1,050 target / 7,350행 (target당 7칸)
- 채점: `results/2_full_{iu,mimic}/scores/*.csv` (metric), `results/2_full_{iu,mimic}/judges/*.csv` (LLM judge)
- 분석: `results/2_full_{iu,mimic}/analysis/{REPORT.md, JUDGES.md, summary_by_condition.csv, per_type.csv, decomposition.csv, judge_cells*.csv}`
- 파이프라인: `scripts/run_full.sh` → `run_full_mopup.sh` → `run_full_until_complete.sh` (10/2 04:02 `COMPLETE`), gpt-oss 재실행 `run_gptoss_rerun.sh` (10/3)
- 지표: paired accuracy (같은 target에서 Δ(C) > Δ(P), 동점 0.5), 95% CI는 report 단위 cluster bootstrap 1,000회

---

## 1. 세트 구성

| | IU X-Ray | MIMIC-CXR |
|---|---|---|
| target | 890 | 1,050 |
| report | 714 | 1,037 |
| 타입별 target | anatomy 150, laterality 146, measurement 94, negation 119, severity 137, temporal 150, uncertainty 94 | 각 150 |
| S2 paraphrase 채택률 (문장) | 2,351 / 2,560 = 91.8% | 4,083 / 4,427 = 92.2% |
| target당 paraphrase된 context 문장 | 3.03 / 4.03 | 3.93 / 4.56 |

Shortcut floor (surface-only 로지스틱 회귀 AUROC, 문서 7)

| 조건 | IU | MIMIC |
|---|---|---|
| controlled S0 | 0.643 | 0.622 |
| controlled S1 | 0.616 | 0.599 |
| controlled S2 | 0.540 | 0.523 |
| confound v1형 (C0 vs P1) | 1.000 | 1.000 |
| confound ReEvalMed형 (C0 vs P2) | 0.983 | 0.996 |

데이터 무결성: 모든 metric이 전 행 채점, 중복 uid 없음. 결측은 CRIMSON 5행씩(JSON 파싱 실패)뿐.

---

## 2. 주 결과 — 혼동 조건 vs 통제 조건 (paired accuracy [95% CI])

### IU X-Ray (n = 890)

| Metric | 혼동 v1형 | 혼동 ReEvalMed형 | 통제 S0 | 통제 S2 |
|---|---|---|---|---|
| *Jaccard (meaning-blind)* | 0.630 | 0.034 | 0.630 [0.608, 0.650] | 0.625 [0.603, 0.647] |
| *token F1 (meaning-blind)* | 0.638 | 0.030 | 0.638 [0.616, 0.659] | 0.640 [0.618, 0.661] |
| BLEU | 0.010 | 0.015 | 0.558 [0.539, 0.576] | 0.552 [0.533, 0.571] |
| ROUGE-L | 0.000 | 0.018 | 0.607 [0.586, 0.625] | 0.608 [0.588, 0.627] |
| BERTScore distilbert (v1 설정) | **0.001** | 0.019 | **0.658** [0.627, 0.691] | 0.660 [0.627, 0.692] |
| BERTScore roberta-large | 0.006 | 0.018 | 0.674 [0.643, 0.704] | 0.694 [0.662, 0.722] |
| BERTScore deberta-xlarge-mnli | 0.028 | 0.044 | 0.790 [0.763, 0.813] | 0.798 [0.769, 0.823] |
| F1CheXbert | 0.515 | 0.506 | 0.520 [0.513, 0.526] | 0.518 [0.512, 0.524] |
| Temporal | 0.520 | 0.439 | 0.520 [0.513, 0.527] | 0.520 [0.513, 0.527] |
| SRR-BERT | 0.593 | 0.502 | 0.598 [0.584, 0.612] | 0.598 [0.584, 0.612] |
| RadGraph | 0.339 | 0.067 | 0.568 [0.547, 0.590] | 0.582 [0.561, 0.603] |
| RaTEScore | 0.633 | 0.195 | 0.678 [0.650, 0.706] | 0.672 [0.646, 0.699] |
| RadCliQ-v1 | 0.088 | 0.047 | 0.725 [0.693, 0.753] | 0.728 [0.697, 0.756] |
| GREEN | 0.752 | 0.724 | 0.852 [0.837, 0.868] | 0.764 [0.743, 0.786] |
| CRIMSON (MedGemma-4B) | 0.807 | 0.808 | 0.809 [0.793, 0.825] | 0.805 [0.788, 0.821] |
| Llama-3.1-8B judge | 0.681 | 0.768 | 0.779 [0.762, 0.796] | 0.747 [0.729, 0.765] |
| gemma-3-27b judge | 0.928 | 0.958 | 0.917 [0.904, 0.928] | 0.928 [0.915, 0.938] |
| Qwen3-32B judge | 0.956 | 0.960 | 0.933 [0.921, 0.945] | 0.915 [0.901, 0.927] |
| gpt-oss-20b judge | 0.969 | 0.963 | 0.967 [0.958, 0.976] | 0.957 [0.947, 0.967] |
| gpt-oss-120b judge | 0.958 | 0.969 | 0.963 [0.954, 0.971] | 0.965 [0.957, 0.974] |
| Qwen3-32B (thinking) judge | 0.974 | 0.974 | 0.971 [0.962, 0.979] | 0.969 [0.960, 0.977] |

### MIMIC-CXR (n = 1,050)

| Metric | 혼동 v1형 | 혼동 ReEvalMed형 | 통제 S0 | 통제 S2 |
|---|---|---|---|---|
| *Jaccard* | 0.591 | 0.008 | 0.591 [0.570, 0.613] | 0.588 [0.567, 0.610] |
| *token F1* | 0.603 | 0.007 | 0.603 [0.583, 0.622] | 0.602 [0.581, 0.622] |
| BLEU | 0.005 | 0.004 | 0.570 [0.552, 0.588] | 0.563 [0.544, 0.582] |
| ROUGE-L | 0.000 | 0.003 | 0.530 [0.512, 0.546] | 0.527 [0.510, 0.544] |
| BERTScore distilbert | **0.001** | 0.005 | **0.626** [0.596, 0.654] | 0.616 [0.586, 0.645] |
| BERTScore roberta-large | 0.005 | 0.006 | 0.660 [0.631, 0.689] | 0.699 [0.672, 0.726] |
| BERTScore deberta-xlarge-mnli | 0.018 | 0.019 | 0.811 [0.787, 0.833] | 0.822 [0.800, 0.844] |
| F1CheXbert | 0.511 | 0.491 | 0.526 [0.519, 0.534] | 0.531 [0.524, 0.539] |
| Temporal | 0.541 | 0.330 | 0.541 [0.531, 0.551] | 0.537 [0.527, 0.546] |
| SRR-BERT | 0.619 | 0.463 | 0.624 [0.611, 0.638] | 0.625 [0.611, 0.639] |
| RadGraph | 0.269 | 0.037 | 0.573 [0.554, 0.596] | 0.579 [0.558, 0.600] |
| RaTEScore | 0.600 | 0.081 | 0.658 [0.632, 0.682] | 0.649 [0.623, 0.672] |
| RadCliQ-v1 | 0.089 | 0.021 | 0.690 [0.662, 0.716] | 0.687 [0.657, 0.714] |
| GREEN | 0.680 | 0.626 | 0.830 [0.815, 0.844] | 0.750 [0.731, 0.769] |
| CRIMSON | 0.822 | 0.832 | 0.838 [0.824, 0.853] | 0.831 [0.817, 0.846] |
| Llama-3.1-8B judge | 0.622 | 0.719 | 0.741 [0.724, 0.757] | 0.715 [0.699, 0.731] |
| gemma-3-27b judge | 0.934 | 0.963 | 0.904 [0.891, 0.916] | 0.905 [0.893, 0.918] |
| Qwen3-32B judge | 0.933 | 0.952 | 0.869 [0.853, 0.883] | 0.886 [0.873, 0.898] |
| gpt-oss-20b judge | 0.974 | 0.963 | 0.969 [0.961, 0.976] | 0.945 [0.934, 0.955] |
| gpt-oss-120b judge | 0.961 | 0.964 | 0.965 [0.957, 0.973] | 0.961 [0.952, 0.969] |

### 관찰 (두 corpus에서 일치)

1. **BERTScore reversal은 구성 artefact.** v1 설정(distilbert) 기준 혼동 0.001 → 통제 0.63–0.66. CI가 0.5를 포함하지 않는다.
2. **혼동의 방향이 P 칸 선택으로 뒤집힌다.** Jaccard: v1형 0.59–0.63 vs ReEvalMed형 0.01–0.03. RaTEScore: 0.60–0.63 vs 0.08–0.20. RadGraph: 0.27–0.34 vs 0.04–0.07.
3. **통제하면 순위가 바뀐다** (비-LLM, IU 통제 S0): BERTScore-deberta 0.79 > RadCliQ 0.73 > RaTEScore 0.68 > BERTScore-roberta 0.67 > BERTScore-distilbert 0.66 > token F1 0.64 ≈ Jaccard 0.63 > ROUGE-L 0.61 > SRR-BERT 0.60 > RadGraph 0.57 > BLEU 0.56 > F1CheXbert = Temporal 0.52.
   v1형 혼동에서는 RaTEScore 0.63 ≈ Jaccard 0.63 > SRR-BERT 0.59 > ... > RadCliQ 0.09 > BERTScore 0.00.
4. **meaning-blind 기준선을 못 넘는 clinical metric.** RadGraph(0.57), SRR-BERT(0.60–0.62), F1CheXbert(0.52–0.53), Temporal(0.52–0.54)는 Jaccard/token F1(0.59–0.64)과 같거나 낮다.
5. **GREEN은 surface 잡음에 따라 하락**: 통제 S0 0.85 / 0.83 → S2 0.76 / 0.75 → ReEvalMed형 0.72 / 0.63. CI가 겹치지 않는다. CRIMSON은 0.81 / 0.83으로 조건 간 차이 없음.
6. **LLM judge는 혼동 조건에서 오히려 점수가 오른다** (gemma 0.92 → 0.96, Qwen3 0.93 → 0.96): P2가 "명백히 재서술"이라 PRESERVED로 판정하기 쉽기 때문. 통제 조건(특히 S0)이 judge에게 더 어렵다.

---

## 3. 의미 효과와 surface 효과 분해 (z-scored Δ; Fig 3 원자료)

| Metric | 의미 (C0−P0) IU / MIMIC | surface S1 (P1−P0) | surface S2 (P2−P0) | 의미 @S2 (C2−P2) |
|---|---|---|---|---|
| BLEU | 0.01 / 0.01 | 0.35 / 0.23 | 1.94 / 2.04 | 0.01 / 0.01 |
| ROUGE-L | 0.03 / 0.01 | 2.00 / 2.00 | 1.35 / 1.58 | 0.03 / 0.01 |
| BERTScore distilbert | 0.04 / 0.02 | 1.19 / 1.23 | 1.83 / 2.06 | 0.04 / 0.02 |
| BERTScore roberta-large | 0.07 / 0.05 | 1.43 / 1.34 | 1.76 / 2.02 | 0.06 / 0.05 |
| BERTScore deberta-mnli | 0.23 / 0.22 | 1.54 / 1.50 | 1.62 / 1.93 | 0.20 / 0.18 |
| RadGraph | 0.09 / 0.09 | 0.30 / 0.43 | 1.49 / 1.73 | 0.09 / 0.09 |
| RadCliQ-v1 | 0.15 / 0.15 | 0.76 / 0.81 | 1.74 / 1.99 | 0.13 / 0.15 |
| RaTEScore | 0.14 / 0.11 | 0.11 / 0.10 | 0.89 / 1.41 | 0.14 / 0.11 |
| Temporal | 0.04 / 0.08 | 0.00 / 0.00 | 0.30 / 0.72 | 0.04 / 0.06 |
| F1CheXbert | 0.15 / 0.19 | 0.04 / 0.10 | 0.11 / 0.22 | 0.14 / 0.22 |
| SRR-BERT | 0.46 / 0.54 | 0.02 / 0.02 | 0.35 / 0.54 | 0.44 / 0.51 |
| GREEN | 1.20 / 1.03 | 0.26 / 0.30 | 0.39 / 0.59 | 0.96 / 0.93 |
| CRIMSON | 0.95 / 0.87 | 0.00 / 0.03 | 0.00 / 0.01 | 0.92 / 0.84 |
| Llama-3.1-8B judge | 1.14 / 1.01 | 0.63 / 0.65 | 0.13 / 0.16 | 0.92 / 0.81 |
| gemma-3-27b judge | 1.47 / 1.35 | 0.04 / 0.02 | −0.24 / −0.38 | 1.48 / 1.40 |
| Qwen3-32B judge | 1.69 / 1.40 | −0.09 / −0.18 | −0.16 / −0.31 | 1.59 / 1.39 |

- 세 군집: **surface 지배형**(BLEU, ROUGE, BERTScore, RadGraph, RadCliQ: surface가 의미의 5–200배), **둔감형**(F1CheXbert, Temporal, RaTEScore, SRR-BERT), **의미 지배형**(CRIMSON, gemma, Qwen3; GREEN·Llama-8B는 의미 효과는 크지만 surface 0.3–0.6).
- gemma·Qwen3의 surface S2가 음수: paraphrase된 P2를 P0보다 *더* PRESERVED로 판정(오경보 감소). §4 참조.

---

## 4. LLM judge 칸별 "CHANGED" 판정률 (rubric prompt)

| Judge | corpus | identity | P0 | P1 | P2 | C0 | C1 | C2 |
|---|---|---|---|---|---|---|---|---|
| Llama-3.1-8B | IU | 0.004 | 0.169 | 0.575 | 0.251 | 0.693 | 0.876 | 0.713 |
| Llama-3.1-8B | MIMIC | 0.006 | 0.150 | 0.594 | 0.250 | 0.610 | 0.849 | 0.661 |
| gemma-3-27b | IU | 0.000 | 0.215 | 0.240 | 0.087 | 0.930 | 0.900 | 0.837 |
| gemma-3-27b | MIMIC | 0.000 | 0.293 | 0.311 | 0.096 | 0.941 | 0.880 | 0.808 |
| Qwen3-32B | IU | 0.000 | 0.108 | 0.063 | 0.022 | 0.930 | 0.855 | 0.833 |
| Qwen3-32B | MIMIC | 0.000 | 0.257 | 0.173 | 0.108 | 0.939 | 0.835 | 0.823 |
| gpt-oss-20b | IU | 0.000 | 0.030 | 0.026 | 0.065 | 0.958 | 0.960 | 0.949 |
| gpt-oss-20b | MIMIC | 0.000 | 0.048 | 0.038 | 0.087 | 0.975 | 0.968 | 0.950 |
| gpt-oss-120b | IU | 0.000 | 0.057 | 0.071 | 0.073 | 0.970 | 0.960 | 0.970 |
| gpt-oss-120b | MIMIC | 0.001 | 0.070 | 0.077 | 0.104 | 0.987 | 0.977 | 0.978 |
| Qwen3-32B (thinking) | IU | 0.000 | 0.027 | 0.020 | 0.030 | 0.958 | 0.955 | 0.952 |

타입별 (IU / MIMIC)

| 현상 | 칸·타입 | Llama-8B | gemma-27b | Qwen3-32B |
|---|---|---|---|---|
| 단위 변환을 변경으로 판정 | P0 measurement | 0.84 / 0.48 | 0.87 / 0.85 | 0.27 / **0.96** |
| severity 동의어를 변경으로 판정 | P0 severity | 0.14 / 0.13 | 0.34 / 0.54 | 0.20 / 0.32 |
| temporal 동의어(stable↔unchanged 등)를 변경으로 판정 | P0 temporal | 0.04 / 0.17 | 0.21 / 0.35 | 0.10 / 0.25 |
| paraphrase 속 uncertainty flip 누락 | C2 uncertainty 탐지율 | 0.37 / 0.40 | 0.34 / 0.39 | 0.29 / 0.37 |
| paraphrase 속 laterality flip 누락 | C2 laterality 탐지율 | 0.58 / 0.55 | 0.73 / 0.71 | 0.84 / 0.84 |
| 문장 순서만 바꿔도 오경보 | P1 전체 | 0.58 / 0.59 | 0.24 / 0.31 | 0.06 / 0.17 |

- MIMIC의 measurement는 대부분 기구 위치("ET tube 5 cm above the carina")이고, Qwen3는 이 경우 단위 변환(50 mm)을 96% 변경으로 판정한다. IU(병변 크기 위주)에서는 27%.
- uncertainty flip(hedged↔definite)은 paraphrase 잡음 속에서 세 judge 모두 30–40%만 탐지. ~~S0에서는 82–93%(gemma, Qwen3)~~ **[10/7 정정]** 82–93%는 탐지율이 아니라 paired accuracy였다. S0 탐지율(CHANGED 비율)은 gemma 0.68 / 0.76, Qwen3 0.60 / 0.70, Llama 0.28 / 0.25 (IU / MIMIC)다. gemma·Qwen3는 S2에서 절반으로 떨어지므로 **S2가 hard tier로 작동**한다는 결론은 유지된다 (문서 13 §3.5).

### Prompt 민감도 — "errors" prompt (GREEN식 오류 나열), IU

| Judge | prompt | P0 오경보 | P2 오경보 | C0 탐지 | 통제 S0 paired acc | 통제 S2 paired acc |
|---|---|---|---|---|---|---|
| gemma-3-27b | rubric | 0.215 | 0.087 | 0.930 | 0.917 | 0.928 |
| gemma-3-27b | **errors** | **0.896** | **0.987** | 0.999 | **0.546** | **0.344** |
| Qwen3-32B | rubric | 0.108 | 0.022 | 0.930 | 0.933 | 0.915 |
| Qwen3-32B | errors | 0.204 | 0.244 | 0.963 | 0.882 | 0.870 |
| gpt-oss-20b | rubric | 0.030 | 0.065 | 0.958 | 0.967 | 0.957 |
| gpt-oss-20b | errors | 0.115 | 0.161 | 0.981 | 0.936 | 0.933 |
| gpt-oss-120b | rubric | 0.057 | 0.073 | 0.970 | 0.963 | 0.965 |
| gpt-oss-120b | errors | 0.048 | 0.081 | 0.987 | 0.969 | 0.960 |

- 같은 모델이 prompt만 바뀌어도 통제 S2 paired accuracy가 0.93 → 0.34로 떨어진다. errors prompt에서 gemma는 무해한 재서술의 90–99%에 "오류"를 나열한다(예: `"noted" instead of "is noted" ... could subtly affect the perceived certainty`). paraphrase된 context 문장마다 오류를 세므로 P2 평균 오류 수 2.38 > C2 1.97.
- 원출력 확인 결과 파싱 문제가 아님 (`ERROR_COUNT` 줄 100% 존재, 잘림 없음). 일부 출력은 같은 항목을 반복 나열.
- 함의: "오류를 나열하라"는 GREEN류 prompt는 surface 차이를 오류로 세게 만든다. GREEN의 S0 → S2 하락(0.85 → 0.76)과 같은 방향.

---

## 5. 타입별 통제 S0 paired accuracy (IU / MIMIC)

| Metric | anatomy | laterality | measurement | negation | severity | temporal | uncertainty |
|---|---|---|---|---|---|---|---|
| Jaccard | 0.65 / 0.66 | 0.75 / 0.83 | 0.32 / 0.25 | 0.58 / 0.53 | 0.73 / 0.68 | 0.54 / 0.48 | 0.78 / 0.71 |
| BERTScore distilbert | 0.81 / 0.86 | 0.80 / 0.85 | 0.41 / 0.37 | 0.74 / 0.75 | **0.07 / 0.12** | 0.91 / 0.61 | 0.80 / 0.82 |
| BERTScore deberta-mnli | 0.93 / 0.91 | 0.79 / 0.81 | 0.50 / 0.49 | 1.00 / 1.00 | 0.51 / 0.58 | 0.87 / 0.98 | 0.87 / 0.90 |
| F1CheXbert | 0.50 / 0.50 | 0.50 / 0.50 | 0.50 / 0.50 | 0.64 / 0.64 | 0.50 / 0.50 | 0.51 / 0.53 | 0.50 / 0.51 |
| RadGraph | 0.63 / 0.58 | 0.52 / 0.61 | 0.46 / 0.44 | 0.85 / 0.83 | **0.33 / 0.38** | 0.50 / 0.52 | 0.74 / 0.65 |
| RaTEScore | 0.71 / 0.73 | 0.71 / 0.72 | 0.47 / 0.43 | 0.76 / 0.83 | 0.65 / 0.63 | 0.74 / 0.63 | 0.62 / 0.63 |
| RadCliQ-v1 | 0.91 / 0.95 | 0.76 / 0.87 | 0.45 / 0.40 | 0.95 / 0.98 | **0.35 / 0.31** | 0.77 / 0.51 | 0.83 / 0.80 |
| SRR-BERT | 0.53 / 0.53 | 0.52 / 0.50 | 0.50 / 0.50 | 0.88 / 0.93 | 0.51 / 0.51 | 0.58 / 0.62 | 0.74 / 0.78 |
| Temporal | 0.50 / 0.50 | 0.50 / 0.50 | 0.50 / 0.50 | 0.54 / 0.58 | 0.50 / 0.50 | 0.58 / 0.70 | 0.50 / 0.50 |
| GREEN | 0.85 / 0.83 | 0.92 / 0.92 | 0.72 / 0.82 | 0.92 / 0.95 | 0.90 / 0.82 | 0.96 / 0.91 | **0.55 / 0.55** |
| CRIMSON | 0.87 / 0.92 | 0.88 / 0.94 | 0.73 / 0.72 | 0.94 / 0.93 | 0.89 / 0.89 | 0.72 / 0.89 | **0.54 / 0.57** |
| Llama-3.1-8B | 0.68 / 0.65 | 0.77 / 0.75 | 0.65 / 0.66 | 0.96 / 0.96 | 0.84 / 0.72 | 0.86 / 0.87 | 0.62 / 0.58 |
| gemma-3-27b | 0.95 / 0.91 | 0.94 / 0.96 | 0.58 / 0.72 | 0.99 / 1.00 | 0.94 / 0.85 | 0.99 / 0.97 | 0.93 / 0.92 |
| Qwen3-32B | 0.94 / 0.92 | 0.96 / 0.95 | 0.81 / 0.54 | 0.98 / 0.99 | 0.95 / 0.89 | 0.99 / 0.94 | 0.82 / 0.85 |

- **severity에서 chance 미만**: BERTScore-distilbert 0.07–0.12, RadGraph 0.33–0.38, RadCliQ 0.31–0.35. P(`mild`→`slight`, `small`→`small-sized`)를 C(`mild`→`moderate`)보다 더 벌점. embedding·graph metric은 등급 단어끼리를 가깝게, 드문 동의어를 멀게 본다. v1의 "severity blindness"보다 강한 결과(통제된 조건에서의 역전).
- **measurement는 모든 비-LLM metric이 0.24–0.50**: 단위 변환(4.7 cm → 47 mm)을 값 변경과 구별하지 못하거나 더 벌점.
- **uncertainty는 GREEN·CRIMSON도 0.54–0.57** (v1에서도 GREEN 0.59 / 0.54였음 — 통제 조건에서 재확인). 범용 judge(gemma 0.93, Qwen3 0.82–0.85)는 탐지.
- F1CheXbert·Temporal은 설계 범위(14 label / temporal 단어) 밖 타입에서 정확히 0.50.

---

## 6. gpt-oss-20b — 파싱 문제와 재실행

| 항목 | 내용 |
|---|---|
| 문제 | vLLM 출력에 harmony 형식의 추론 채널이 그대로 포함됨 (`analysis…assistantfinal{json}`). 기존 파서는 (a) 출력 전체에서 첫 JSON을 찾고 (b) JSON이 없으면 본문에 `CHANGED` 문자열이 있는지로 fallback (리포트의 "unchanged"에도 걸림) (c) 원출력을 2,000자까지만 저장 |
| 영향 (rubric) | 최종 답 없이 fallback된 행: IU 0.32%, MIMIC 0.87% (확신도 정확히 50인 행). 수치 영향은 작음 |
| 영향 (errors) | 저장 출력의 11%에 `ERROR_COUNT` 없음 (C2 28%, P2 18%). `max_tokens=1024`에서 추론이 끊긴 경우 오류 수 0으로 처리됨 → **신뢰 불가** |
| 조치 | `9_llm_judge.py`: 최종 채널(`assistantfinal` 이후)만 파싱, 최종 채널이 없으면 UNPARSED(NaN), 마지막 JSON 사용, `max_tokens` 4096, `max_model_len` 8192, 원출력 20,000자 저장, `finish_reason` 기록 |
| 재실행 | `scripts/run_gptoss_rerun.sh` — IU·MIMIC rubric, IU·MIMIC errors. 이전 파일은 `results/2_full_*/judges_superseded/`로 이동 |
| 다른 judge | Llama·gemma·Qwen3(`enable_thinking=False`)는 추론 채널이 없어 해당 없음. gemma errors는 `ERROR_COUNT` 100% 존재 |

재실행 전 수치(참고용, superseded): rubric 통제 S0 0.970 / 0.971, S2 0.952 / 0.952; 칸별 P0 0.026 / 0.050, C2 0.947 / 0.955.

재실행 결과 (10/3 완료, 10/7 기입): gpt-oss-20b rubric 통제 S0 0.967 / 0.969, S2 0.957 / 0.945 (IU / MIMIC); errors 통제 S0 0.936 / 0.922, S2 0.933 / 0.922. 최종 채널만 파싱해도 재실행 전 수치와 0.01 이내로 같다. 위 표들의 자리표시도 채웠다.

---

## 7. 실패 기록 (full 세트)

| 시각 | 실패 | 원인 | 조치 |
|---|---|---|---|
| 10/1 17:13 | IU paraphrase 엔진 초기화 실패 | 공유 GPU에서 시작 중 메모리 부족 | 재시도 루프(최대 6회) 추가, 1회 재시도로 성공 |
| 10/1 17:35 | MIMIC GREEN, MIMIC BERTScore OOM | 12개 metric 프로세스 + 다른 프로젝트 65GB로 GPU 포화 | `run_full_mopup.sh`가 순차 재채점 |
| 10/1 17:50 | IU CRIMSON 실패, gemma errors 실패 등 | 동일 | `run_full_until_complete.sh`가 완료 조건 충족까지 재실행 (1 round로 완료) |
| 10/3 | gpt-oss 추론 채널 파싱 (§6) | 파서 설계 | 재실행 |
| – | RadEval-BERTScore | tokenizers 버전 불일치 (v1과 동일 오류) | 제외 |
| – | Qwen3-32B-FP8 | `deepgemm` JIT가 nvcc 요구 | bf16 사용 |

## 8. 아직 없는 것

| 항목 | 필요 조건 |
|---|---|
| proprietary judge (Claude / GPT / Gemini), IU만 | API key (U3). Gate 2 기준상 최소 2개 계열 필요 |
| MedGemma-27b, Llama-3.3-70B judge | HF 라이선스 동의 |
| 사람 라벨 기준 결과 | annotation 회수 (문서 6) |
| X6 외부 타당성 (ReXVal) | 데이터 (U4) |
| ReEvalMed 데이터에 대한 surface-only 분류기 | 데이터 (U5) |
| E8 메커니즘 분석 (GREEN error category 일치, RadGraph 누락) | 다음 작업 |
