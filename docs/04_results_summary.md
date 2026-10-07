# 04. 핵심 결과 요약

수치 출처: `paper/tables/*.tex` (= `scripts/20_make_paper_tables.py`가 `results/`의 CSV에서 생성), `results/full_{iu,mimic}/REPORT.md`, `results/mimic_monotonicity/MONO.md`, `results/external_validity/EXTERNAL.md`, `results/REVIEW1007_FOLLOWUP.md`. 표의 칸은 **IU / MIMIC**. paired accuracy(chance 0.5)가 기본 지표.

## 1. 진단 — 라벨은 surface만으로 예측된다 (Table 1)

| Benchmark / 비교 | n | surface-only LR AUROC | Jaccard AUROC | #edit tokens AUROC |
|---|---|---|---|---|
| ClinSemBench-v1 Impression (rule 라벨) | 2,400 | **0.92** | 0.85 | 0.19 |
| ClinSemBench-v1 Findings (rule 라벨) | 2,400 | **0.96** | 0.89 | 0.16 |
| ClinSemBench-v1 검증 세트 (**human 라벨**) | 467 | **0.83** | 0.81 | 0.24 |
| RaTE-Eval 합성 과제 (synonym vs opposite, 공개) | 739 | **0.89** | 0.17 | 0.21 |
| 우리 Conf-R (C0 vs P1) | 1,780 / 2,100 | 1.00 / 1.00 | 0.59 / 0.56 | 0.00 / 0.00 |
| 우리 Conf-P (C0 vs P2) | 〃 | 0.98 / 1.00 | 0.05 / 0.01 | 0.02 / 0.00 |
| **우리 Ctrl-0 (C0 vs P0)** | 〃 | **0.64 / 0.62** | 0.59 / 0.56 | 0.51 / 0.51 |
| **우리 Ctrl-2 (C2 vs P2)** | 〃 | **0.54 / 0.52** | 0.52 / 0.51 | 0.50 / 0.50 |

- v1 논문의 최고 metric(GREEN rule 0.90, human 0.81)과 같은 수치를 의미를 모르는 분류기가 낸다.
- 혼동의 방향: v1형은 "토큰 bag이 바뀌면 changed, edit 크면 benign"(Jaccard 0.85), RaTE-Eval·ReEvalMed형은 "surface 변화 크면 benign"(Jaccard 0.17). 같은 target에 P 칸만 바꿔 한 세트에서 두 방향 재현.
- ReEvalMed 공개 표: BLEU 78.5 vs 41.9, RadGraph 81.4 vs 58.6처럼 오류 쌍에 더 높은 점수 (저자도 surface 차이로 설명했으나 통제 안 함).

## 2. 혼동 vs 통제 (Table 2; `tie` = Ctrl-0에서 P0·C0 점수가 정확히 같은 비율, `strict` = Jaccard·token F1이 정확히 같은 target 443 / 486에서의 Ctrl-0)

| Metric | Conf-R | Conf-P | **Ctrl-0** | Ctrl-2 | tie | strict |
|---|---|---|---|---|---|---|
| Jaccard (meaning-blind) | 0.63 / 0.59 | 0.03 / 0.01 | 0.63 / 0.59 | 0.62 / 0.59 | 0.54 / 0.50 | 0.50 / 0.50 |
| BLEU | 0.01 / 0.01 | 0.02 / 0.00 | 0.56 / 0.57 ↓ | 0.55 / 0.56 | 0.70 / 0.63 | 0.51 / 0.50 |
| ROUGE-L | 0.00 / 0.00 | 0.02 / 0.00 | 0.61 / 0.53 ↓ | 0.61 / 0.53 | 0.61 / 0.65 | 0.50 / 0.50 |
| BERTScore (DistilBERT, v1 설정) | **0.00 / 0.00** | 0.02 / 0.00 | **0.66 / 0.63** | 0.66 / 0.62 | 0.00 / 0.00 | 0.68 / 0.65 |
| BERTScore (RoBERTa-L) | 0.01 / 0.00 | 0.02 / 0.01 | 0.67 / 0.66 | 0.69 / 0.70 | 0.00 / 0.00 | 0.69 / 0.67 |
| BERTScore (DeBERTa-MNLI) | 0.03 / 0.02 | 0.04 / 0.02 | 0.79 / 0.81 | 0.80 / 0.82 | 0.00 / 0.00 | 0.81 / 0.85 |
| F1CheXbert | 0.51 / 0.51 | 0.51 / 0.49 | 0.52 / 0.53 ↓ | 0.52 / 0.53 | **0.96 / 0.94** | 0.51 / 0.52 |
| Temporal F1 | 0.52 / 0.54 | 0.44 / 0.33 | 0.52 / 0.54 ↓ | 0.52 / 0.54 | **0.96 / 0.89** | 0.52 / 0.57 |
| SRR-BERT | 0.59 / 0.62 | 0.50 / 0.46 | 0.60 / 0.62 | 0.60 / 0.62 | 0.77 / 0.73 | 0.58 / 0.60 |
| RadGraph F1 | 0.34 / 0.27 | 0.07 / 0.04 | 0.57 / 0.57 | 0.58 / 0.58 | 0.56 / 0.48 | **0.52 / 0.54** |
| RaTEScore | 0.63 / 0.60 | 0.19 / 0.08 | 0.68 / 0.66 | 0.67 / 0.65 | 0.14 / 0.19 | 0.68 / 0.65 |
| RadCliQ-v1 | 0.09 / 0.09 | 0.05 / 0.02 | 0.72 / 0.69 | 0.73 / 0.69 | 0.00 / 0.00 | 0.71 / 0.66 |
| GREEN | 0.75 / 0.68 | 0.72 / 0.63 | **0.85 / 0.83** | **0.76 / 0.75** ∗ | 0.28 / 0.32 | 0.88 / 0.82 |
| CRIMSON | 0.81 / 0.82 | 0.81 / 0.83 | 0.81 / 0.84 | 0.80 / 0.83 | 0.38 / 0.32 | 0.80 / 0.85 |
| Llama-3.1-8B (rubric) | 0.68 / 0.62 | 0.77 / 0.72 | 0.78 / 0.74 | 0.75 / 0.72 ∗ | 0.43 / 0.49 | 0.75 / 0.70 |
| Gemma-3-27B | 0.93 / 0.93 | 0.96 / 0.96 | 0.92 / 0.90 | 0.93 / 0.91 | 0.16 / 0.17 | 0.93 / 0.89 |
| Qwen3-32B | 0.96 / 0.93 | 0.96 / 0.95 | 0.93 / 0.87 | 0.91 / 0.89 | 0.11 / 0.23 | 0.94 / 0.86 |
| Qwen3-32B (thinking) | 0.97 / 0.96 | 0.97 / 0.98 | 0.97 / 0.96 | 0.97 / 0.97 | 0.04 / 0.06 | 0.98 / 0.97 |
| gpt-oss-20b | 0.97 / 0.97 | 0.96 / 0.96 | 0.97 / 0.97 | 0.96 / 0.95 | 0.06 / 0.05 | 0.96 / 0.95 |
| gpt-oss-120b | 0.96 / 0.96 | 0.97 / 0.96 | 0.96 / 0.96 | 0.97 / 0.96 | 0.07 / 0.07 | 0.98 / 0.97 |

↓ Jaccard보다 유의하게 낮음, ∗ Ctrl-0 → Ctrl-2 유의한 하락 (report bootstrap 95%).

읽는 법
1. **BERTScore reversal은 artefact**: Conf-R 0.00 → Ctrl-0 0.63–0.66 (strict 0.65–0.68).
2. **혼동 방향이 P 칸 선택으로 뒤집힌다**: Jaccard 0.63 ↔ 0.03, RaTEScore 0.63 ↔ 0.19, RadGraph 0.34 ↔ 0.07.
3. **label·graph metric은 matched edit 대부분에 반응하지 않는다**: F1CheXbert·Temporal tie 89–96%, RadGraph는 strict subset에서 0.52–0.54(chance).
4. **GREEN은 paraphrase 잡음에서 8–9점 하락** (CI 0 제외); CRIMSON 불변. 정도표현 보존 subset(0.091 / 0.073)과 대체 paraphraser(0.076 [0.041, 0.111])에서도 유지 → drift 탓 아님.
5. judge는 혼동 조건에서 오히려 점수가 오름(P2가 "명백히 재서술"이라 쉬움) → 통제 S0가 judge에게 더 어렵다.

## 3. 의미 효과 vs surface 효과 (z-scored Δ, Fig 3) 와 환율

| 군집 | metric | 의미 (C0−P0) | surface S2 (P2−P0) | 환율 (paraphrase 1회 = 의미 변경 몇 회) IU / MIMIC |
|---|---|---|---|---|
| surface 지배 | BLEU, ROUGE, BERTScore ×3, RadGraph, RadCliQ | 0.01–0.23 | 1.35–2.06 | BLEU 282 / 284, BERTScore-DistilBERT 53 / 109, RoBERTa 27 / 42, Jaccard 18 / 39, **RadGraph 18 / 19**, RadCliQ 12 / 13, DeBERTa 7 / 9 |
| 중간 | RaTEScore, SRR-BERT, F1CheXbert, Temporal | 0.04–0.54 | 0.1–1.4 | RaTEScore 6 / 13 |
| 의미 지배 | CRIMSON, GREEN, judge | 0.87–1.69 | ≈0 (GREEN 0.39–0.59) | GREEN 0.33 / 0.6, CRIMSON·judge ≈ 0 |

- surface penalty는 다시 쓴 토큰 비율에 비례해 단조 증가(BERTScore Q1 0.95 → Q4 2.67 SD)하되 같은 구간에서 Ctrl-2 paired accuracy는 평평 → paraphrase는 의미 신호를 지우지 않고 penalty 바닥만 올린다(Conf-P 역전의 메커니즘).
- 혼합효과 상호작용: GREEN −0.24, Llama −0.22, Qwen3 −0.11/−0.01, gpt-oss-20b −0.09/−0.13, 나머지 |≤0.03|.

## 4. LLM judge 칸별 "CHANGED" 비율 (P 칸 = 오경보, C 칸 = 탐지; rubric)

| Judge | P0 | P1 | P2 | C0 | C1 | C2 |
|---|---|---|---|---|---|---|
| Llama-3.1-8B | 0.17 / 0.15 | **0.58 / 0.59** | 0.25 / 0.25 | 0.69 / 0.61 | 0.88 / 0.85 | 0.71 / 0.66 |
| Gemma-3-27B | **0.21 / 0.29** | 0.24 / 0.31 | 0.09 / 0.10 | 0.93 / 0.94 | 0.90 / 0.88 | 0.84 / 0.81 |
| Qwen3-32B | 0.11 / 0.26 | 0.06 / 0.17 | 0.02 / 0.11 | 0.93 / 0.94 | 0.86 / 0.84 | 0.83 / 0.82 |
| Qwen3-32B (thinking) | 0.03 / 0.06 | 0.02 / 0.06 | 0.03 / 0.06 | 0.96 / 0.98 | 0.96 / 0.97 | 0.95 / 0.97 |
| gpt-oss-20b | 0.03 / 0.05 | 0.03 / 0.04 | 0.07 / 0.09 | 0.96 / 0.98 | 0.96 / 0.97 | 0.95 / 0.95 |
| gpt-oss-120b | 0.06 / 0.07 | 0.07 / 0.08 | 0.07 / 0.10 | 0.97 / 0.99 | 0.96 / 0.98 | 0.97 / 0.98 |

남는 실패 (타입별)
- **단위 변환(4.7 cm → 47 mm)을 변경으로 판정**: P0 measurement 오경보 Gemma 0.87 / 0.85, Llama 0.84 / 0.48, Qwen3 0.27 / **0.96**(MIMIC은 88%가 tube 위치), gpt-oss-120b – / 0.29, gpt-oss-20b 0.01 / 0.04. `rubric_unit`(단위 변환은 benign이라고 명시)으로 Gemma는 0.27 / 0.12로 해소, Qwen3는 0.14 / 0.70으로 부분 해소, 대신 실제 measurement 오류 탐지가 4–19점 하락.
- **paraphrase 속 uncertainty flip 누락**: C2 uncertainty 탐지율 Gemma 0.34 / 0.39, Qwen3 0.29 / 0.37, Llama 0.37 / 0.40 (C0에서는 0.68 / 0.76, 0.60 / 0.70, 0.28 / 0.25). 추론 모델은 0.68–0.90 (gpt-oss-20b MIMIC 0.96 → 0.79).
- severity 동의어 오경보: Gemma 0.34 / 0.54, Qwen3 0.20 / 0.32. 문장 재배열만으로 오경보: Llama P1 0.58.
- **prompt 민감도** (Ctrl-2, IU): Gemma rubric 0.93 → errors **0.34** (P2의 99%에 "오류" 나열), Qwen3 0.92 → 0.87, gpt-oss-20b 0.96 → 0.93, gpt-oss-120b 0.97 → 0.96.

## 5. Fixed-surface monotonicity (MIMIC 300; Table 4)

| Metric | τ (고정 surface) | 0→1 | 1→2 | 2→3 | 기존 사다리 1→2 / 2→3 | benign 3개 > 오류 1개 |
|---|---|---|---|---|---|---|
| Jaccard | 0.41 | 0.60 | 0.61 | 0.63 | 0.99 / 0.99 | 0.98 |
| BLEU | **0.17** | 0.53 | 0.53 | 0.55 | **1.00 / 1.00** | **1.00** |
| BERTScore (DistilBERT) | 0.36 | 0.72 | 0.66 | 0.65 | 1.00 / 1.00 | 1.00 |
| BERTScore (DeBERTa-MNLI) | 0.74 | 0.81 | 0.83 | 0.79 | 1.00 / 1.00 | 0.85 |
| RadGraph F1 | **0.16** | 0.57 | 0.55 | 0.49 | **0.95 / 0.96** | 0.96 |
| RadCliQ-v1 | 0.58 | 0.74 | 0.77 | 0.71 | 1.00 / 0.99 | 0.97 |
| GREEN | 0.77 | 0.76 | 0.77 | 0.74 | 0.85 / 0.85 | 0.34 |
| CRIMSON | 0.88 | 0.86 | 0.83 | 0.85 | 0.83 / 0.85 | 0.15 |
| gpt-oss-20b (rubric) | 0.69 | 0.96 | 0.52 | 0.56 | 0.55 / 0.53 | 0.04 |
| gpt-oss-120b (rubric) | 0.73 | 0.97 | 0.53 | 0.60 | 0.54 / 0.59 | 0.02 |
| gpt-oss-20b (**errors**) | **0.96** | 0.91 | 0.93 | 0.93 | 0.99 / 0.99 | 0.19 |
| gpt-oss-120b (**errors**) | **0.98** | 0.96 | 0.97 | 0.97 | 0.99 / 0.99 | 0.06 |

- 기존 "오류 늘수록 edit 늘어나는" 사다리에서 완벽히 단조이던 BLEU·RadGraph·BERTScore가 surface 고정 사다리에서는 τ 0.16–0.41. ReEvalMed·RadSEM monotonicity 축에 대한 직접 반례.
- 무해한 edit 3개가 실제 오류 1개보다 더 벌점받는 비율: lexical·RadGraph·RadCliQ 0.96–1.00.
- rubric judge는 첫 오류만 잡고(0.96–0.98) 2·3번째에 반응 없음(0.49–0.61) → 이진 판정+확신도 형식의 성질. **errors prompt로 바꾸면 gpt-oss가 전 scorer 중 가장 monotone** (τ 0.96–0.98). 약한 모델은 errors prompt에서 benign에 가짜 불일치만 늘어남(Qwen3 benign>error 0.46, Gemma 0.98).

## 6. 타입별 (Ctrl-0, 주요)

- **severity에서 chance 미만**: BERTScore-DistilBERT 0.07 / 0.12, RadGraph 0.33 / 0.38, RadCliQ 0.35 / 0.31 — 동의어(`mild→slight`)를 등급 변경(`mild→moderate`)보다 더 벌점. 인접·양극단 모두. 전문의 확인 대상 lexicon 제외 시 0.07–0.13 상승(판정에 민감).
- **measurement**: 비-LLM 전부 0.24–0.50 (unit 하위타입은 D-1 결함으로 혼동 조건에 해당).
- **uncertainty**: GREEN 0.55 / 0.55, CRIMSON 0.54 / 0.57 — CRIMSON은 91–96%를 certainty 오류로 정확히 분류하지만 점수 가중치가 낮아 반영 안 됨("blind"가 아니라 "가중치로 무시"). 범용 judge는 탐지(Gemma 0.93, Qwen3 0.82–0.85).
- F1CheXbert·Temporal은 설계 범위 밖 타입에서 정확히 0.50.

## 7. Robustness (Ctrl-0)

- D-1(unit) + D-2(negation fragment) + 전문의 확인 대상 lexicon 전부 제외(IU 673 / MIMIC 773): 결론 유지. BERTScore 0.73–0.79로 오히려 상승, RadGraph 0.61 / 0.63 ≈ Jaccard, GREEN 0.87 / 0.84, judge 0.75–0.95.
- 논쟁 패턴군(uncertainty의 `consistent/compatible with`) 제외 subset, D-10 제외: 결론 불변 (`results/full_*/review1007/`).

## 8. 외부 타당성 — 우리 열이 metric을 전문의 순서로 세우는가 (RaTE-Eval; 부록 표)

| 우리 열 | Task 1 (문장 441쌍, 16 scorer) Spearman ρ [95% CI], permutation p | judge 제외 15 | Task 2 (문단 370쌍, 14) |
|---|---|---|---|
| Conf-R | 0.41 [−0.12, 0.77], p=0.12 | 0.28 | −0.16 |
| Conf-P | 0.29 [−0.32, 0.79], p=0.27 | 0.14 | −0.37 |
| **Ctrl-0** | **0.72 [0.24, 0.94], p=0.003** | 0.66 | 0.66 |
| Ctrl-2 | 0.66, p=0.007 | 0.59 | 0.67 |
| fixed-surface mono τ | 0.56, p=0.02 | 0.53 | 0.62 |

전문의 τ 자체(Task 1): gpt-oss-20b 0.38, GREEN 0.38, RadGraph 0.36, RaTEScore 0.35, RadCliQ 0.31, BERTScore-DistilBERT 0.29, CRIMSON 0.26, Jaccard 0.24, BLEU 0.12, F1CheXbert 0.08, Temporal 0.03. 한계: RaTE-Eval은 CXR 외 모달리티 위주(CXR 전용 scorer에 불리), scorer 16개라 CI 넓음.

## 9. RaTE-Eval 합성 과제에서의 metric (739 triplet; opposite가 synonym rewrite보다 더 벌점받는 비율)

BLEU 0.12, ROUGE-L 0.12, token F1 0.14, BERTScore-DistilBERT 0.14, Jaccard 0.15, RoBERTa 0.18, RadCliQ 0.42, DeBERTa 0.44, RadGraph 0.47, Temporal 0.49 (tie 0.90), RaTEScore 0.52, F1CheXbert 0.52 (tie 0.93), SRR-BERT 0.54, **CRIMSON 0.90, gpt-oss-20b 0.99**. 독립된 공개 suite에서 v1의 "BERTScore 역전"이 같은 방향(Conf-P형)으로 재현.

## 10. 세트 통계 (Table in §4)

| Corpus | Targets | Reports | Anat. | Lat. | Meas. | Neg. | Sev. | Temp. | Unc. | 패턴 수 | S2 채택 (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IU X-Ray | 890 | 714 | 150 | 146 | 94 | 119 | 137 | 150 | 94 | 47 | 91.9 |
| MIMIC-CXR | 1,050 | 1,037 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 64 | 92.2 |
