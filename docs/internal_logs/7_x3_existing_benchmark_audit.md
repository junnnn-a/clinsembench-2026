# 7. X3 — 기존 benchmark audit (Table 3 초안)

- 작성: 2026-10-01
- 코드: `scripts/13_x3_audit_existing_benchmarks.py` (surface-only 분류기는 `6_shortcut_floor.py`와 동일)
- 결과: `results/3_x3_audit/{table3.csv, TABLE3.md, reevalmed_published_means.csv}`
- 질문: 기존 perturbation benchmark의 라벨(meaning-changing 여부)이 **의미를 전혀 보지 않는 surface feature만으로** 얼마나 예측되는가

---

## 1. 결과

Surface-only 분류기 = (Jaccard drop, token-F1 drop, difflib ratio, char ratio, #edit tokens, edit 비율, 길이 비율, |길이 차|, bag 변화, 숫자 변화) → 로지스틱 회귀, report 단위 5-fold. AUROC 0.5 = 라벨이 surface로 예측되지 않음.

| Benchmark / 조건 | n | surface-only LR AUROC | Jaccard drop 단독 | #edit tokens 단독 | 혼동 방향 |
|---|---|---|---|---|---|
| ClinSemBench v1, impression (rule 라벨) | 2,400 | **0.917** | 0.849 | 0.186 | 토큰 bag이 바뀌면 changed, edit이 크면 benign |
| ClinSemBench v1, findings (rule 라벨) | 2,400 | **0.964** | 0.890 | 0.156 | 〃 |
| ClinSemBench v1, 480쌍 (**human 라벨**) | 467 | **0.827** | 0.811 | 0.238 | 〃 |
| Factorial IU, 혼동 v1형 (C0 vs P1) | 1,780 | 1.000 | 0.586 | 0.001 | edit이 크면 benign |
| Factorial IU, 혼동 ReEvalMed형 (C0 vs P2) | 1,780 | 0.983 | 0.053 | 0.017 | surface 변화가 크면 benign |
| **Factorial IU, 통제 S0 (C0 vs P0)** | 1,780 | **0.643** | 0.586 | 0.508 | 거의 없음 |
| **Factorial IU, 통제 S2 (C2 vs P2)** | 1,780 | **0.540** | 0.521 | 0.501 | 없음 |
| Factorial MIMIC, 혼동 v1형 | 2,100 | 1.000 | 0.558 | 0.000 | edit이 크면 benign |
| Factorial MIMIC, 혼동 ReEvalMed형 | 2,100 | 0.996 | 0.011 | 0.005 | surface 변화가 크면 benign |
| **Factorial MIMIC, 통제 S0** | 2,100 | **0.622** | 0.558 | 0.508 | 거의 없음 |
| **Factorial MIMIC, 통제 S2** | 2,100 | **0.523** | 0.513 | 0.501 | 없음 |

ReEvalMed (데이터 미보유, 공개 표의 평균 점수만 사용)

| Metric | significant-error 쌍 평균 | insignificant 쌍 평균 | 차이 | 오류 쌍에 더 높은 점수? |
|---|---|---|---|---|
| BLEU | 78.48 | 41.89 | +36.59 | 예 |
| ROUGE-L | 87.90 | 65.95 | +21.95 | 예 |
| RadGraph | 81.35 | 58.56 | +22.79 | 예 |
| BERT-F1 | 97.31 | 92.99 | +4.32 | 예 |
| GREEN | 74.30 | 74.76 | −0.46 | 아니오 |

## 2. 해석 (논문 §진단 파트의 재료)

1. **v1의 rule 라벨은 surface만으로 AUROC 0.92–0.96으로 예측된다. human 라벨도 0.83이다.** v1 논문이 보고한 최고 metric(GREEN: rule 0.90, human 0.81)과 같은 수준을 의미를 전혀 모르는 분류기가 낸다. 즉 v1의 pooled AUROC는 metric의 의미 민감도를 측정했다고 볼 수 없다.
2. **혼동의 방향은 benchmark 구성이 정한다.**
   - v1: benign이 토큰 bag을 안 바꿈 → overlap 계열(Jaccard)이 "정방향"(0.85–0.89), edit 크기에 비례하는 계열(BERTScore)은 "역방향"
   - ReEvalMed형: benign이 문장 전체 재작성 → overlap 계열 전부 "역방향"(Jaccard 0.01–0.05). ReEvalMed 공개 표에서 BLEU·ROUGE·RadGraph·BERT가 오류 쌍에 더 높은 점수를 준 것과 같은 방향
   - 같은 target, 같은 C에 P 칸만 바꿔 두 방향을 한 세트 안에서 재현 (factorial 혼동 조건 두 행)
3. **통제하면 사라진다.** S2 조건에서 0.52–0.54. S0 조건은 0.62–0.64로 잔여 비대칭이 있다 (문서 4 §4: C는 원 토큰을 지우고 P는 남기는 경향). 논문에는 이 수치를 숨기지 않고 "shortcut floor"로 표 맨 위에 둔다.
4. ReEvalMed 저자들도 "insignificant 쌍은 surface 변화가 크고 significant 쌍은 국소적"이라고 적었으나 통제하지 않았다. 우리는 (i) 그 효과의 크기를 surface-only 분류기로 정량화하고 (ii) 통제된 세트를 제공한다.

## 3. 한계와 남은 일

- ReEvalMed **데이터**에 대한 surface-only 분류기 수치는 데이터 접근(U5)이 필요하다. 접근이 안 되면 공개 표 기반 분석 + 우리 세트 내 재현으로 서술한다 (계획 Gate 2).
- RadJudge(CRIMSON) 등 다른 공개 세트: 접근·라이선스 확인되면 같은 스크립트로 한 행 추가 가능.
- pilot 대비 full 세트의 S0 floor가 0.60 → 0.62–0.64로 올랐다. 표본이 늘어 분류기가 타입별 패턴을 더 잘 학습한 것으로 보인다. S0의 잔여 leak을 타입별로 분해한 표(type-aware 상한)를 부록에 둔다: `results/2_full_{iu,mimic}/shortcut_floor_all.csv`.
