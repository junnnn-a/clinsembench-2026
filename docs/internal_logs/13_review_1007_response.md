# 13. 10/7 외부 리뷰 대응 기록 (2026-10-07)

초안 v0(`docs/paper/main_v0_1007.tex`로 보존)에 대해 받은 외부 리뷰의 지적별로, 무엇을 확인했고 어떻게 결정했는지 기록한다.
리뷰 원문 요지는 §1, 지적별 결정은 §2, 새 실험 결과는 §3, 논문 수정 내역은 §4, 남은 일은 §5에 있다.

- 새 스크립트: `scripts/21_review_reanalysis.py`, `22_probe_public_suites.py`, `23_external_validity.py`, `run_review_1007.sh`
- 수정한 스크립트: `5_paraphrase_context.py`(`--degree_guard`), `9_llm_judge.py`(prompt `rubric_unit`), `17_make_figures.py`, `20_make_paper_tables.py`, `run_set.sh`(`NO_LLM=1`), `env_llm.sh`(`KV_GB`)
- 새 결과: `results/2_full_{iu,mimic}/review1007/`, `results/3_x3_audit/RATE_EVAL.md`, `results/2_full_{rate1,rate2,rate3,iualt}/`, `results/4_external_validity/`
- 새 데이터: `data/external/RaTE-Eval/`(HF `Angelakeke/RaTE-Eval`, CC-BY-4.0), `data/pairs/full_{iualt,rate1,rate2,rate3}_*.csv`

## 1. 리뷰 요지

결론은 "Findings~main 경계, oral/spotlight에는 미달"이었다. 강점은 설계(위치·형태 matched pair, fixed-surface monotonicity)와 "혼동 방향이 benign edit 구성에 따라 뒤집힌다"는 발견이고, 부족한 것은 진단의 외부 증거, 라벨 검증, 실제 평가와의 연결 세 가지였다.

| # | 지적 |
|---|---|
| 1 | 진단의 정량 증거가 자기 v1 하나뿐. "widely reported reversal"은 과장 |
| 2 | REREF와 겹침(§6.2와 "For metric users"의 절반). 기여를 "표면을 통제하면 meaning 민감도 결론이 어떻게 바뀌는가"로 좁혀야 함 |
| 3 | uncertainty·severity 라벨이 외부 기준(REREF taxonomy)과 충돌. GREEN·CRIMSON의 chance는 의도된 동작일 수 있음 |
| 4 | 통제가 깨끗하지 않은데(probe 0.62–0.64, Jaccard 0.59–0.64) headline이 그 누수에 기댐. F1CheXbert 0.52는 tie 때문 |
| 5 | GREEN의 S2 하락이 표면 민감성인지 paraphrase drift(D-11)를 정당하게 잡은 것인지 구분 불가 |
| 6 | judge 결론에 prompt가 섞임(단위 변환 false alarm, "grading 못 함") |
| 7 | abstract 과장, 본문–표 불일치 10곳 |

그 밖에 선행연구 6건의 정식 서지, ReEvalMed·RadSEM·RadOT-Eval 서술 수정 두 곳, 그림 가독성, §6.5 유지 권고가 있었다.

## 2. 지적별 결정

| # | 결정 | 근거 | 상태 |
|---|---|---|---|
| 1 | **수용.** 공개 suite RaTE-Eval에 probe와 전체 metric을 적용. abstract·intro·§3·Table 1·부록에 반영. "widely reported" 삭제 | §3.1, §3.7(1) | 완료 |
| 1 | ReXErr·ReXVal·RadEvalX·ReEvalMed 직접 probe는 **보류** | 전부 PhysioNet 자격이 필요하고 서버에 없음. ReEvalMed는 원문에 "PhysioNet 제출 절차 시작"이라고만 있어 아직 받을 수 없음 | 사용자 확인 필요 |
| 2 | **수용.** Related Work에 REREF를 한 문단 비중으로 서술하고, 기여 3번과 Discussion을 "표면을 고정했을 때 meaning 민감도"로 다시 씀. §6.2에 "표면 축 순서는 REREF와 일치"라고 명시 | REREF 원문 확인: meaning-preserving 재작성만 다루고 meaning-changing edit는 없음. CRIMSON 평균 IQR 0.083, GREEN 0.245, RadCliQ 0.512, RadGraph 0.741 | 완료 |
| 3 | **부분 수용.** 전문의 검토는 하지 않음. 대신 (a) 논쟁 패턴군을 뺀 subset 재분석, (b) "결함"이 아니라 "scorer가 무엇을 세는가의 차이"로 서술 변경, (c) Limitations에 라벨이 한 가지 해석임을 명시 | 전문의 섭외 불가는 10/5 사용자 결정. REREF 원문에서 "consistent with" vs "likely represents"를 같은 확신 수준의 hedging 예로 든 것을 확인 | 완료 |
| 4 | **수용.** win/tie/loss 분해와 strict-matched subset을 Table 2에 열로 추가. "token overlap을 못 이긴다" 문단을 "대부분의 matched edit에 반응하지 않는다(tie)"로 교체 | §3.2 | 완료 |
| 5 | **수용.** (a) 정도 표현이 보존된 S2 subset 재분석, (b) 다른 계열 paraphraser(Llama-3.1-8B) + 정도 표현 guard로 301 target 재생성 후 전체 재채점 | §3.4 | 완료: 두 검사 모두 GREEN 하락 유지 |
| 6 | **수용.** (a) monotonicity set에 errors prompt judge 4개, (b) 단위 변환을 benign으로 명시한 `rubric_unit` prompt, (c) Qwen3-thinking을 MIMIC·monotonicity에 추가. "grading 못 함"은 출력 형식의 성질이라고 본문 수정 | §3.5, §3.7(2)(3)(4) | 완료: errors prompt로 gpt-oss는 가장 monotone, rubric_unit은 Gemma에서만 대부분 해소 |
| 7 | **수용.** 지적된 10곳 전부 결과 CSV와 대조해 수정 | §4.2 | 완료 |
| – | 서지 6건 + RadEval·FineRadScore | arXiv 페이지에서 저자 전체 이름까지 직접 확인해 교체. VERIFY 문구가 PDF에 찍히지 않도록 note 삭제 | 완료 |
| – | Temporal F1 출처 | RadEval README가 가리키는 출처는 Bannur 2023이 아니라 **Libra (Zhang et al., Findings of ACL 2025, pp. 17275–17303)**. 교체함 | 완료 |
| – | 그림 | Fig 2는 Table 2와 중복이라 부록으로 이동, 범례의 "v1-type" 삭제. Fig 3은 column 폭 전용 1-panel(IU)로 다시 그리고 라벨 겹침을 수동 조정. 두 corpus 판은 부록 | 완료 |
| – | §6.5 부록 이동 | 리뷰 의견대로 **본문 유지** | 완료 |
| – | D-10 | 집계 결과 IU 2건, MIMIC 0건. 재생성하지 않고 Limitations에 기재, IU 공개본에서 제거 예정 | 완료 (release 때 제거) |
| – | 외부 타당성("so what") | **수용, 범위 축소.** ReXVal·RadPref는 접근 불가라 RaTE-Eval Task 1·2의 전문의 평점으로 대체 | 완료 (§3.6): Ctrl-0 ρ 0.72 vs Conf-R 0.41 / Conf-P 0.29 |
| – | 환율 재분석 | **수용.** abstract와 §6.2, 부록 표에 반영 | 완료 (§3.3) |
| – | Proprietary judge, 사람 검증 | 변동 없음. API key와 annotation 결과가 필요 | TBD 유지 |

### 수용하지 않았거나 다르게 처리한 것

- **Radiologist 1명의 치환 패턴 검토.** 사용자 결정(10/5)에 따라 하지 않는다. 논문은 임상 유의성 주장을 하지 않고, uncertainty·severity 결과는 "라벨이 한 가지 해석"이라는 단서와 논쟁 패턴 제외 subset 결과를 함께 제시한다.
- **"F1CheXbert·Temporal F1이 Jaccard보다 유의하게 낮다"는 표식(↓).** Table 2에는 남겼다. 통계적으로는 사실이기 때문이다. 다만 본문에서는 이를 "chance보다 못하다"로 읽지 않는다고 명시하고, 해석은 tie 비율과 strict subset에 맡겼다.
- **Table 2의 "Jaccard보다 유의하게 높음" 표식.** 새 기호를 추가하지 않고 caption에 "무표시 = 유의하게 높음"이라고 썼다. `20_make_paper_tables.py`가 생성 시 이 명제가 모든 무표시 칸에서 참인지 검사한다(현재 위반 0건).

## 3. 새 실험 결과

### 3.1 공개 suite probe — RaTE-Eval (`22_probe_public_suites.py`)

RaTE-Eval Task 3은 MIMIC-IV 문장 847개에 대해 Mixtral이 쓴 synonym rewrite와 opposite rewrite를 제공한다. **공개본에는 원문 문장이 들어 있지 않다.** 원문은 Task 1의 `gt_report` 문장들과 겹치므로 TF-IDF(1–2gram) cosine으로 rewrite·opposite 양쪽에 모두 가까운 문장을 찾아 복원했다.

| subset | triplet 수 | surface-only LR AUROC | Jaccard AUROC | Jaccard paired acc | edit 비율 (rewrite / opposite) |
|---|---|---|---|---|---|
| 전체 정렬 | 847 | 0.864 | 0.188 | 0.159 | 1.14 / 0.56 |
| 확신 정렬 (논문 사용) | 739 | **0.887** | 0.166 | **0.147** | 1.07 / 0.53 |
| rewrite와 opposite가 독립적으로 같은 원문을 고른 경우 | 714 | 0.874 | 0.180 | 0.163 | 1.08 / 0.54 |

- 표면 통계만으로 라벨이 0.86–0.89로 예측된다. 방향은 ReEvalMed형(Conf-P)이다: synonym rewrite가 opposite보다 약 2배 많은 토큰을 바꾸고, Jaccard는 85%의 triplet에서 opposite를 더 높게 본다.
- 정렬 기준을 바꿔도(세 번째 행은 어느 쪽 후보에도 유리하지 않은 기준) 수치가 거의 같다.
- 한계: 원문 복원이 정렬에 의존한다. 논문 Table 1 각주와 Limitations, 부록에 명시했다.
- Task 1·2(전문의 평점)에서 표면 통계만의 Kendall τ는 0.32(문장), 0.45(문단)다. 이 과제는 서로 다른 보고서 쌍이라 표면 유사도가 실제 유사도와 상관되는 것이 정상이므로 혼동의 증거로 쓰지 않고 §3.6의 기준선으로만 쓴다.
- 이 739 triplet에 대한 metric 채점: **진행 중** (`results/2_full_rate3/`). 결과는 §3.7에 추가.

### 3.2 win/tie/loss와 strict-matched subset (`21_review_reanalysis.py` A, B)

Ctrl-0에서 P0와 C0가 정확히 같은 점수를 받는 비율(tie):

| metric | IU tie | MIMIC tie | 해석 |
|---|---|---|---|
| F1CheXbert | 0.96 | 0.94 | edit가 보이지 않음 |
| Temporal F1 | 0.96 | 0.89 | 〃 |
| SRR-BERT | 0.77 | 0.73 | 〃 |
| RadGraph F1 | 0.56 | 0.48 | 절반은 안 보이고, 나머지는 win 0.29–0.33 / loss 0.15–0.19 |
| Jaccard | 0.54 | 0.50 | |
| BERTScore·RadCliQ | 0.00 | 0.00 | tie 없음 |
| GREEN | 0.28 | 0.32 | 나머지는 거의 전부 win |
| CRIMSON | 0.38 | 0.32 | 〃 |

Strict-matched subset(P0·C0의 Jaccard와 token F1이 **정확히 같은** target; IU 443/890, MIMIC 486/1,050). 여기서는 두 baseline이 구성상 0.50이다.

| metric | Ctrl-0 strict (IU / MIMIC) | 전체 (IU / MIMIC) |
|---|---|---|
| F1CheXbert | 0.51 / 0.52 | 0.52 / 0.53 |
| RadGraph F1 | 0.53 / 0.54 | 0.57 / 0.57 |
| SRR-BERT | 0.58 / 0.60 | 0.60 / 0.62 |
| BERTScore DistilBERT | 0.68 / 0.65 | 0.66 / 0.63 |
| BERTScore RoBERTa-L | 0.69 / 0.67 | 0.67 / 0.66 |
| BERTScore DeBERTa-MNLI | 0.81 / 0.85 | 0.79 / 0.81 |
| RaTEScore | 0.68 / 0.65 | 0.68 / 0.66 |
| RadCliQ | 0.71 / 0.67 | 0.72 / 0.69 |
| GREEN | 0.88 / 0.82 | 0.85 / 0.83 |
| CRIMSON | 0.80 / 0.85 | 0.81 / 0.84 |
| judges | 0.75–0.98 | 0.74–0.97 |

**결정.** 누수를 제거해도 순서와 결론이 유지된다. 그래서 headline을 "Jaccard를 못 이긴다"에서 "label·graph 기반 metric은 matched edit의 대부분에 반응하지 않는다"로 바꿨다. 이쪽이 누수에 기대지 않고, 리뷰어가 지적한 "0.52는 tie"와도 일치한다.

### 3.3 환율 (`21_review_reanalysis.py` C)

문맥 paraphrase 1회의 penalty를 matched meaning change 1회의 penalty로 나눈 값.

| metric | IU | MIMIC |
|---|---|---|
| BLEU | 282 | 284 |
| BERTScore DistilBERT | 53 | 109 |
| BERTScore RoBERTa-L | 27 | 42 |
| Jaccard | 18 | 39 |
| RadGraph F1 | 18 | 19 |
| RadCliQ | 12 | 13 |
| BERTScore DeBERTa-MNLI | 7.1 | 9.0 |
| RaTEScore | 6.3 | 13 |
| GREEN | 0.33 | 0.6 |
| CRIMSON, judges | ≈ 0 | ≈ 0 |

리뷰의 추정(RadGraph 약 17, BERTScore 약 60, GREEN 약 0.3)과 맞는다. abstract에는 보수적으로 "RadGraph 18, BERTScore 50 이상"으로 썼다.

### 3.4 S2 robustness — GREEN 하락이 drift 때문인가

(a) **정도 표현 보존 subset** (paraphrase된 문맥의 정도 표현 multiset이 원문과 같은 target; IU 766/890, MIMIC 792/1,050)

| | 전체 | 정도 표현 보존 |
|---|---|---|
| GREEN Ctrl-0 → Ctrl-2 하락, IU | 0.088 | 0.091 |
| GREEN Ctrl-0 → Ctrl-2 하락, MIMIC | 0.080 | 0.073 |

D-11 유형의 drift가 없는 target에서도 하락 폭이 같다.

(b) **다른 계열 paraphraser + guard** (`full_iualt`, 06:30 완료; `results/2_full_iualt/analysis/ALT.md`): IU 301 target의 문맥을 Llama-3.1-8B-Instruct로 다시 paraphrase하고 정도 표현 guard를 추가. 수락률 86.3%(원래 Qwen2.5 세트 91.9%). S0·S1·identity 칸은 원래 세트와 동일 입력이라 기존 점수를 재사용했고(`25_merge_iualt.py`), S2 602쌍만 새로 채점했다.

| | Ctrl-0 | Ctrl-2 (Qwen2.5 paraphraser) | Ctrl-2 (Llama-3.1 + guard) | 하락 (Qwen2.5) | 하락 (Llama + guard) [95% CI] |
|---|---|---|---|---|---|
| GREEN | 0.826 | 0.731 | 0.749 | 0.095 | **0.076 [0.041, 0.111]** |
| RadCliQ | 0.714 | 0.701 | 0.704 | 0.013 | 0.010 [−0.040, 0.056] |
| BERTScore DeBERTa | 0.784 | 0.784 | 0.784 | 0.000 | 0.000 |
| RadGraph | 0.565 | 0.571 | 0.535 | −0.007 | 0.030 [−0.010, 0.069] |

GREEN의 하락은 paraphraser 계열과 무관하게 재현된다. (CRIMSON·judge의 alt 결과는 CRIMSON 채점이 끝나면 표에 추가; 논문 부록 표 `tab_alt`는 스크립트가 자동 생성.)

### 3.5 judge와 prompt

이미 확인한 것(재분석):

- 초안의 "uncertainty를 paraphrase 없이 82–93% 탐지"는 **틀린 수치**였다. 82–93%는 paired accuracy였다. 실제 C0 탐지율(CHANGED 비율)은 Gemma 0.68/0.76, Qwen3 0.60/0.70, Llama 0.28/0.25 (IU/MIMIC)이고, C2에서는 0.34/0.39, 0.29/0.37, 0.37/0.40이다. reasoning 모델은 C2에서 0.68–0.90이고 대체로 유지되지만 gpt-oss-20b는 MIMIC에서 0.96 → 0.79로 떨어진다. 본문을 이 수치로 교체했다.
- 초안의 "interaction이 GREEN·Llama 외 ±0.03"도 틀렸다. Qwen3 −0.11/−0.01, gpt-oss-20b −0.09/−0.13이다. 본문을 고치고 부록 표에 Interaction 열을 추가했다.
- MIMIC measurement target의 88%가 tube·catheter 위치 서술이다(IU는 9%). 초안 §4.2의 "measurement는 device 서술을 피한다"는 틀린 문장이었다(실제로 피하는 것은 laterality와 temporal). §4.2를 고치고 §4.4에 corpus 차이를 명시했다.

새로 돌리는 것: errors prompt × monotonicity (gpt-oss-20b/120b, Qwen3-32B, Gemma-3-27B), `rubric_unit` × IU(4개 judge)·MIMIC(2개), Qwen3-thinking × MIMIC·monotonicity. **진행 중.** 결과는 §3.7에 추가.

### 3.6 외부 타당성 (`23_external_validity.py`)

질문: 우리의 어느 열(Ctrl-0, Ctrl-2, Conf-R, Conf-P, fixed-surface τ)이 metric을 전문의와 같은 순서로 세우는가.
사람 기준: RaTE-Eval Task 1 test(문장 441쌍, 전문의 오류 수; CPU 사정으로 train 1,775쌍은 lexical 계열만 채점하고 분석에서는 제외)과 Task 2 test(문단 370쌍, 0–5점). 15개 metric + gpt-oss-20b를 채점해 scorer별 Kendall τ를 구하고, scorer 간 Spearman 순위상관(permutation p, bootstrap CI)을 본다. 결과: `results/4_external_validity/EXTERNAL.md`, 논문 부록 `tab_external`.

**결과 (Task 1, 16 scorer, 09:00)**

| 우리 열 | Task 1, 16 scorer: Spearman ρ [95% CI], permutation p | Task 1, judge 제외 15개 | Task 2 (문단, 14개) |
|---|---|---|---|
| Conf-R (v1형 혼동) | 0.41 [−0.12, 0.77], p=0.12 | 0.28 | −0.16 |
| Conf-P (ReEvalMed형 혼동) | 0.29 [−0.32, 0.79], p=0.27 | 0.14 | −0.37 |
| **Ctrl-0** | **0.72 [0.24, 0.94], p=0.003** | 0.66 | 0.66 |
| Ctrl-1 | 0.64, p=0.007 | 0.57 | 0.63 |
| Ctrl-2 | 0.66, p=0.007 | 0.59 | 0.67 |
| growing-surface monotonicity step | 0.01, p=0.98 | 0.18 | 0.64 |
| fixed-surface monotonicity τ | 0.56, p=0.02 | 0.53 | 0.62 |

- 통제된 비교는 scorer를 전문의와 같은 순서로 세우고, 혼동된 비교는 그렇지 못하다. 리뷰가 요구한 "so what"에 대한 직접적인 답이며, 논문 §6.1 끝에 한 문단으로 넣었다.
- 전문의 τ 자체(Task 1): gpt-oss-20b 0.38, GREEN 0.38, RadGraph 0.36, RaTEScore 0.35, RadCliQ 0.31, BERTScore-DistilBERT 0.29, CRIMSON 0.26, Jaccard 0.24, BLEU 0.12, F1CheXbert 0.08, Temporal 0.03.
- 한계: scorer 16개라 CI가 넓고, RaTE-Eval은 CXR 외 모달리티가 대부분이라 CXR 전용 scorer에 불리하다. Task 2(문단, 14 metric)에서도 같은 방향(Ctrl-0 0.66, Conf-R −0.16). Task 2에서는 growing-surface step도 0.64로 높은데, 이 과제는 서로 다른 보고서 쌍이라 표면 차이가 실제 차이와 상관되기 때문으로 본다.

주의: RaTE-Eval은 CXR 외 모달리티가 대부분이라 CXR 전용 metric(F1CheXbert, GREEN, CRIMSON)에 불리하다. metric 수가 15–20개라 순위상관의 신뢰구간이 넓다. 결과가 어느 쪽이든 그대로 보고한다.

### 3.7 진행 중 실험의 결과

#### (1) RaTE-Eval 합성 과제의 metric 결과 (`24_review_followup.py` C; `results/3_x3_audit/rate_eval_task3_metrics.csv`)

739 triplet에서 "opposite가 synonym rewrite보다 더 큰 penalty를 받는 비율"(높아야 정상).

| metric | paired acc | tie |
|---|---|---|
| BLEU | 0.12 | 0.00 |
| ROUGE-L | 0.12 | 0.01 |
| Token F1 | 0.14 | 0.01 |
| BERTScore DistilBERT | 0.14 | 0.00 |
| Jaccard | 0.15 | 0.02 |
| BERTScore RoBERTa-L | 0.18 | 0.00 |
| BERTScore DeBERTa-MNLI | 0.44 | 0.00 |
| F1CheXbert | 0.52 | 0.93 |
| SRR-BERT | 0.54 | 0.86 |

| RadCliQ | 0.42 | 0.00 |
| RadGraph F1 | 0.47 | 0.24 |
| Temporal F1 | 0.49 | 0.90 |
| RaTEScore | 0.52 | 0.07 |
| CRIMSON | 0.90 | 0.19 |
| gpt-oss-20b (rubric) | 0.99 | 0.02 |

(06:50 전체 완료; GREEN은 CXR 전용 모델이고 가장 느려 이 세트에서는 제외.) lexical·embedding metric이 전부 chance 아래이고 RadCliQ·RadGraph도 chance 아래다. 우리 v1에서 본 "BERTScore 역전"이 독립된 공개 suite에서 같은 방향(Conf-P형)으로 재현된다. CRIMSON과 gpt-oss-20b는 속지 않는다. RaTEScore가 자기 벤치마크의 합성 과제에서 0.52라는 점은 흥미롭지만, 이 세트는 CXR 외 모달리티가 대부분이고 원문 복원이 정렬에 의존하므로 논문에서는 표로만 제시하고 해석을 달지 않았다. 논문 §3과 부록 표(`tab_rate3`)에 반영.

#### (2) errors prompt × monotonicity — gpt-oss-20b (05:02 완료)

| | fixed-surface τ | 0→1 | 1→2 | 2→3 | 3 benign > 1 error |
|---|---|---|---|---|---|
| gpt-oss-20b, rubric | 0.69 | 0.96 | 0.52 | 0.56 | 0.04 |
| gpt-oss-20b, **errors** | **0.96** | 0.91 | 0.93 | 0.93 | 0.19 |
| CRIMSON (참고) | 0.88 | 0.86 | 0.83 | 0.85 | 0.15 |
| GREEN (참고) | 0.77 | 0.76 | 0.77 | 0.74 | 0.34 |

- **리뷰 지적 6이 맞았다.** 같은 모델이 prompt만 바꾸면 전체 scorer 중 가장 monotone해진다. "rubric judge는 grading을 못 한다"는 모델이 아니라 출력 형식(이진 판정 + confidence)의 성질이다. §6.4를 그렇게 고쳤고, 초안의 "judge는 분류에, enumeration metric은 grading에 강하다"는 문장은 삭제했다.
- 대가도 있다. errors prompt는 benign edit 3개(M0)에도 평균 0.18점의 penalty를 주어, "benign 3개 > 오류 1개"가 4% → 19%로 늘어난다.
- 출력 1.9%가 최종 답 없이 끝나 결측 처리되었고, 여섯 칸이 모두 있는 target은 270/300이다.
- **gpt-oss-120b errors (05:58 완료)**: τ 0.978 [0.971, 0.985], 단계 0.96 / 0.97 / 0.97, benign 3 > error 1 = 0.06 (rubric 0.02). 결측 0. 20b보다 더 monotone하고 benign penalty도 작다. 논문 §6.4·abstract에 반영.
- **Qwen3-32B errors (06:05 완료)**: τ 0.73 (rubric 0.64), 단계 0.77 / 0.73 / 0.77로 평평해졌지만, benign 3 > error 1이 0.46(rubric 0.06). 약한 모델에서는 enumeration 형식이 grading을 조금 돕는 대신 benign edit에 가짜 discrepancy를 많이 단다. 논문 §6.4에 한 문장 추가.
- **Gemma-3-27B errors (09:38 완료)**: τ 0.33 (rubric 0.58), 단계 0.47 / 0.60 / 0.68, benign 3 > error 1 = **0.98**. IU에서 본 대로 Gemma는 errors prompt에서 거의 모든 benign edit에 discrepancy를 나열해 순서가 무너진다. 요약: enumeration 형식은 강한 모델(gpt-oss)에게는 grading 능력을 주고, 약한 모델에게는 false alarm만 늘린다. §6.4에 반영.

#### (3) `rubric_unit` — 단위 변환이 benign임을 prompt에 명시 (Qwen3-32B, 07:21 완료)

| corpus | prompt | P0 measurement false alarm | (value 하위타입) | C0 measurement 탐지 | P0 전체 | Ctrl-0 | Ctrl-2 |
|---|---|---|---|---|---|---|---|
| IU | rubric | 0.27 | 0.16 | 0.88 | 0.11 | 0.93 | 0.91 |
| IU | rubric_unit | 0.14 | 0.07 | 0.80 | 0.09 | 0.92 | 0.92 |
| MIMIC | rubric | 0.96 | 0.95 | 0.99 | 0.26 | 0.87 | 0.89 |
| MIMIC | rubric_unit | 0.70 | 0.59 | 0.95 | 0.20 | 0.88 | 0.88 |

- 리뷰 가설("rubric이 measurement 변화를 changed로 명시해서 생긴 false alarm")은 **부분적으로만 맞다.** 명시 문장을 넣으면 IU에서는 절반으로 줄지만 MIMIC(대부분 tube 위치 "6 cm above the carina" → "60 mm")에서는 70%가 여전히 changed로 판정된다. 대신 실제 measurement 오류 탐지가 4–8점 떨어진다.
- **Gemma-3-27B (09:52)**: P0 measurement false alarm IU 0.87 → 0.27, MIMIC 0.85 → 0.12; C0 measurement 탐지 1.00 → 0.83, 0.99 → 0.81; Ctrl-0 0.92 → 0.94, 0.90 → 0.92. Gemma에서는 rubric 문구가 원인의 대부분이었다.
- **Llama-3.1-8B (IU, 07:30)**: false alarm 0.84 → 0.54이지만 C0 전체 탐지도 0.69 → 0.59로 떨어진다(기준이 느슨해질 뿐).
- 정리: 리뷰 가설은 Gemma에 대해서는 맞고 Qwen3에 대해서는 부분적으로만 맞다. 모든 judge에서 실제 measurement 오류 탐지가 4–19점 떨어진다. 논문 §6.3 한 문장 + 부록 표 `tab_unit`·설명 문단.

#### (4) Qwen3-32B thinking — MIMIC·monotonicity 채움 (08:02 완료)

- MIMIC paired acc: Conf-R 0.96, Conf-P 0.98, Ctrl-0 0.96, Ctrl-2 0.97 (IU 0.97 전 열과 같은 수준). P0 false alarm 0.06, C0 탐지 0.97. Table 2·3의 `--` 칸이 채워졌다.
- monotonicity(fixed-surface): τ 0.68, 단계 0.98 / 0.49 / 0.52 — 다른 rubric judge와 같은 패턴(첫 오류는 잡고 2·3번째에는 반응 없음). 본문 범위를 "0.87–0.98 / 0.49–0.61"로 갱신.
- 8·11·14·21번 스크립트를 두 corpus에 다시 돌렸다. 바뀐 표 수치는 Qwen3-thinking 행뿐이다(bootstrap seed 고정).

#### (5) 결과 파일 위치

- `results/REVIEW1007_FOLLOWUP.md` (`24_review_followup.py`): 대체 paraphraser(A), rubric_unit(B), RaTE-Eval 합성 과제 metric(C)
- `results/4_external_validity/EXTERNAL.md` (`23_external_validity.py --analyze`): 외부 타당성
- `results/2_full_mimicmono/analysis/MONO.md`: errors prompt judge 포함 monotonicity
- 부록 표 `tab_alt`, `tab_unit`, `tab_external`, `tab_rate3`, `tab_allcond`, `tab_mono`(전체)는 `20_make_paper_tables.py`가 생성. 논문은 표 파일이 있을 때만 해당 부록 문단을 포함한다(`\IfFileExists`).
- 데이터 주의: `data/pairs/full_rate1_all.csv`는 Task 1 **test 441쌍**만 담고 있고(채점 범위 축소), 원래 2,216쌍 파일은 `full_rate1full_all.csv`. `full_rate3_all.csv`(739 triplet × identity/P0/C0), `full_iualt_all.csv`(301 target × 7칸), `full_iualts2_all.csv`(그중 S2 602행).

## 4. 논문 수정 내역

### 4.1 구조

- Abstract, 기여 3번, Related Work(meta-evaluation 문단), §3(공개 suite 문단 신설), §4.6(strict-matched subset 문단 신설), §6.1(tie 문단), §6.2(환율 문단 신설), §6.3–6.5, Discussion, Limitations를 다시 썼다.
- Table 2에 `tie`, `strict` 열 추가. Table 1에 RaTE-Eval 행 추가, 우리 세트는 IU/MIMIC을 한 행에 표기. Table 3(judge 칸별 비율)은 부록으로, Table 4(monotonicity)는 본문에 12행 요약판, 부록에 전체판.
- 부록 신설: All Comparisons and Outcome Shares(Ctrl-1 포함, win/tie/loss), Robustness of the Paraphrase Layer, RaTE-Eval, Monotonicity: All Scorers.
- 본문 8쪽 제한을 맞추려고 Fig 1 예시에서 문맥 문장 하나를 `[…]`로 생략했고(caption에 명시), 중복 서술을 줄였다.

### 4.2 본문–표 불일치 수정

| 위치 | 초안 | 수정 |
|---|---|---|
| Abstract | "perfectly monotone metrics drop to τ ≤ 0.2" | "BLEU and RadGraph F1 … drop to τ < 0.2" (0.17, 0.16) |
| Abstract | "strong reasoning judges … miss certainty changes … prompt-sensitive" | reasoning judge 0.95–0.97; 실패는 "smaller and non-reasoning judges"로 한정 |
| Abstract | "widely reported reversal" | "an apparent reversal" |
| §6.4 | BLEU 0.18, 범위 0.16–0.58, "96–100%" | BLEU 0.17; DeBERTa 0.74·RadCliQ 0.58은 "신호를 유지"로 분리; 85–100% |
| §6.4 | judge 첫 단계 0.87–0.98 | 0.87–0.97, Llama 0.68 명시 |
| §6.2 | surface 1.4–2.1, RaTEScore "weak", CRIMSON > 0.9 | 1.35–2.06; RaTEScore는 중간군(0.89–1.41); CRIMSON ≥ 0.87 |
| §6.2 | interaction ±0.03 | §3.5 수치로 교체 |
| §6.3 | Gemma P0 22–29%, Qwen3 0.92 → 0.87 | 21–29%, 0.91 → 0.87; gpt-oss 0.93–0.97 |
| §6.3 | uncertainty 82–93% | C0 탐지율로 교체(§3.5) |
| §4.2 / §6.3 | device 서술 모순 | §4.2 수정, §4.4에 88% 명시 |
| §4.3 | 91.8% | 91.9% |

### 4.3 선행연구 서술 (원문 확인)

- ReEvalMed: 평균값(BLEU 78.48 vs 41.89, GREEN 74.30 vs 74.76) 확인. 저자들이 insignificant pair의 문맥을 의도적으로 줄였고("to prevent metrics from giving high scores just because the reports look similar overall"), monotonicity 역전을 "insignificant errors … often involve larger surface-level changes"로 설명한 것을 확인해 §2·§3에 반영. "not public" → "not openly distributed (controlled-access release announced)".
- RadSEM·RadOT-Eval: metric 논문이므로 metric 문단에 넣고, stress test는 meta-evaluation 문단에서 언급.
- FineRadScore의 venue(MLHC 2024, PMLR 252)는 리뷰가 준 정보를 그대로 썼고 직접 확인하지 못했다. Khorasani 2003은 본문에서 인용하지 않아 출력되지 않는다.

## 5. 남은 일 (10/7 10:00 기준)

실험은 전부 끝났다(10/7 09:52). 논문 `docs/paper/main.pdf`는 24쪽(본문 8쪽 정확히, Limitations가 9쪽에서 시작), 깨진 참조·VERIFY 문구 없음. 남은 `[TBD]` 7곳은 모두 사람 검증과 proprietary judge 관련이다.


| 항목 | 필요한 것 |
|---|---|
| 사람 검증(§4.6, Limitations, Ethics, 부록) | annotation 결과. 논문에는 TBD |
| Proprietary judge | API key 2계열 이상 (IU만) |
| ReEvalMed·ReXVal·ReXErr·RadEvalX 직접 probe | PhysioNet 자격 데이터. ReEvalMed는 저자 요청 또는 PhysioNet 공개 확인 |
| revision note, release 패키지, checklist | 실험 서사가 확정된 뒤 작성 (리뷰 권고 순서) |
| docs/8의 gpt-oss 자리표시, docs/9 결함 목록(D-10, D-11) 갱신 | 문서 작업 |

## 6. 실행 중 겪은 문제와 처리 (10/7 새벽)

| 문제 | 원인 | 처리 |
|---|---|---|
| Llama-3.1-8B paraphrase가 두 번 실패 (`No available memory for the cache blocks`, `Error in memory profiling`) | vLLM은 시작할 때 GPU 여유 메모리를 재서 KV cache 크기를 정한다. 그 사이 다른 작업(CAP, 내 채점 작업)이 메모리를 잡거나 놓으면 계산이 깨진다 | `env_llm.sh`에 `KV_GB=16` 추가, `5/9/10`번 스크립트가 `kv_cache_memory_bytes`로 고정값을 넘겨 프로파일링을 건너뜀 |
| 모든 작업이 평소의 1/5–1/10 속도 (RadGraph 쌍당 9초, vLLM 출력 250 tok/s, GPU 사용률 4–8%) | **컨테이너 CPU quota가 8코어**(`/sys/fs/cgroup/cpu.max` = 800000/100000)이고, CAP 프로젝트의 OCR 작업(paddleocr 24 shard + easyocr)이 약 6.5코어를 쓰고 있었다. 내 채점 프로세스는 각자 스레드 190여 개를 띄워 throttle을 더 키웠다 | `run_set.sh`와 `env_llm.sh`에 `OMP_NUM_THREADS=8` 등 스레드 상한 추가. 세트 채점을 병렬 4개에서 순차(`run_review_sets.sh`)로 변경. CAP 작업은 건드리지 않음 |
| 큰 judge 작업이 GPU lock 뒤에서 대기 | 작은 채점 작업 여러 개가 `gpu_wait` lock을 150초씩 번갈아 잡음 | 위 순차화로 해소 |
| 큐 우선순위 | 속도가 느려 전체 큐가 수 시간 걸림 | `run_review_1007b.sh`로 교체: errors × monotonicity(gpt-oss-120b, Qwen3) → `rubric_unit`(Gemma, Qwen3; IU·MIMIC) → Gemma errors × monotonicity → Llama `rubric_unit` → Qwen3-thinking. gpt-oss-20b `rubric_unit`은 제외(단위 변환 false alarm이 이미 1–4%라 고칠 것이 없음). 세트 채점도 축소: `iualt`는 metric + CRIMSON, `rate3`·`rate1`은 gpt-oss-20b judge만, `rate2`는 metric만 |
| vLLM 시작이 8–10분 | torch.compile과 CUDA graph 캡처가 CPU에 묶임 | `VLLM_EAGER`(기본 1)로 eager 모드 사용. 생성 속도는 CPU가 풀리면 다시 비교해 볼 것 |

| vLLM 엔진이 warm-up 직후 멈춤 (I/O·CPU 0, futex 대기; 세 번) | 다른 vLLM 엔진(CRIMSON, 다른 judge)이 같은 시간에 초기화를 시작하면 먼저 뜬 엔진이 멈춘다 | LLM 작업을 전부 하나의 순차 큐(`run_review_final.sh`)로 합치고, 다른 LLM 프로세스가 없을 때만 시작하도록 함. `GPU_HOLD=300` |

교훈: 이 서버에서 긴 작업을 걸기 전에 `cat /sys/fs/cgroup/cpu.max`와 다른 프로젝트의 CPU 사용량을 먼저 본다. GPU 메모리만 보고 병렬화하면 오히려 느려진다.
