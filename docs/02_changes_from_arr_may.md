# 02. ARR May 제출본(7910)에서 달라진 점

근거: `docs/internal_logs/0_prior_paper_and_experiment_analysis.md`(코드·결과 감사), `1_review_analysis.md`, `2_audit_findings_and_revision_plan.md`, `3_experiment_plan.md`, `13_review_1007_response.md`. 이전 제출본 PDF·tex·리뷰 전문은 `docs/prior_submission/`.

## 0. 한 줄 요약

ARR May 논문의 headline("GREEN 최강, BERTScore는 방향이 뒤집힘")은 AC가 "이미 알려진 사실"로 판정했고, 우리 감사 결과 그 reversal은 **edit 크기 confound가 만든 artefact**였다. 재제출은 그 confound 자체를 진단하고(기존 suite의 라벨이 surface만으로 예측됨), surface를 통제한 factorial 설계로 benchmark를 다시 만들고, 통제 전후로 결론이 어떻게 바뀌는지를 보이는 논문으로 바꿨다. **이전 수치는 "통제 전 조건(v1)"의 증거로만 쓰고, 벤치마크·metric 채점·judge·검증을 전부 다시 했다.**

## 1. 왜 다시 했는가 — ARR May 제출본 감사 결과

리뷰어가 지적하지 않았지만 데이터를 보면 드러나는 문제 (공개 시 치명적):

| # | 문제 | 수치 |
|---|---|---|
| A | **Bag-of-words baseline이 GREEN과 같다.** 의미를 모르는 Jaccard가 human-label AUROC 0.811 (GREEN 0.814). "토큰이 하나라도 바뀌었나" 0/1만으로 0.81–0.83 | benign 3타입 중 format·sentence_order는 토큰 bag을 안 바꾸고(불변 88–100%), changed 9타입은 100% 바꿈 |
| B | **BERTScore reversal은 edit 크기 confound.** BERTScore penalty와 edit 토큰 수의 Spearman 0.81–0.87. benign은 4–46토큰, changed는 1토큰 | AC의 "이미 알려진 사실"이라는 평가와 정확히 맞닿음 |
| C | 규칙이 만든 비문·off-spec candidate: negation `no` 삽입형 63%(그중 94%가 명사구 중간), uncertainty `possible` 삽입형 81%, laterality bilateral 치환 9%(논문은 skip이라 기술), measurement는 단위 교체만(논문은 value/unit), severity 80%가 양극단, false insertion은 finding+laterality+severity+size 동시 포함 | LLM metric이 의미가 아니라 부자연스러움에 반응할 수 있음 |
| D | **Impression/Findings 섹션이 분리되어 있지 않음.** `prepare`의 fallback(findings = findings or impression or text) 때문에 58.1%의 report에서 두 섹션 텍스트가 동일. Table 3의 두 열은 독립 실험이 아님 | 행정 헤더 오염 334/5000도 같은 원인 |
| E | Human validation 480쌍 중 300쌍이 1인 판단(rule 일치 86%); 93.1%는 3중(98.3%)과 단일의 혼합. benign 만장일치 53%. UNCERTAIN 기준이 annotator마다 다름 | |
| F | 논문–코드 불일치: inversion/blindness/gap이 critical 5타입만 계산, rule tier 0–4(논문 0–2), BERTScore backbone 미기재, 부록 수치(n=500, visual-necessity 등)의 원천 파일 없음, 샘플링이 Python `hash()` 의존 | 전부 해소 |

리뷰의 구조적 문제: headline이 약함(AC·38pP), ReEvalMed 등 선행연구 미인용(38pP P1), "LLM에게 너무 쉽다"에 답 못함(P2, P5: 최신 LLM 부재가 post-rebuttal 핵심 우려), 단일 corpus(J1, W1), 공개 자료 없음(Software 1점 × 2).

## 2. 프레이밍 변화

| | ARR May (v1) | ARR October (v2) |
|---|---|---|
| 제목 | ClinSemBench: Stress-Testing Radiology Report Metrics with Minimal Pairs | **Surface or Semantics? Disentangling What Radiology Report Metrics Measure with Factorial Minimal Pairs** (benchmark 이름 유지; 변경 사유를 재제출 양식에 기재 — 결정 D5) |
| Headline | GREEN 최강, BERTScore reversed | perturbation 메타평가는 surface와 의미를 혼동하고, 혼동의 방향은 benign edit 구성이 정한다. surface를 고정하면 의미 민감도에 대한 결론이 바뀐다 |
| v1 결과의 위치 | 주 결과 | "통제 전" 조건(진단 증거). 우리 세트 안에서 v1형(C0 vs P1)·ReEvalMed형(C0 vs P2) 혼동을 같은 target으로 재현 |
| 기여 | (1) 480쌍 검증 benchmark (2) metric audit (3) sensitivity card | (1) **진단**: 공개 suite 포함 라벨이 surface만으로 예측됨 + 두 가지 통제(meaning-blind baseline, surface-only predictability) 제안 (2) **설계**: 위치·형태 matched factorial minimal pair + fixed-surface monotonicity 세트 (3) **통제 하에서 바뀌는 결론** |
| 주 지표 | pooled AUROC (changed 9타입 vs benign 3타입) | **paired accuracy** (같은 target에서 Δ(C) > Δ(P), 동점 0.5) + AUROC. report-cluster bootstrap |
| 보조 지표 | inversion, blindness, gap, rule-tier Spearman, sensitivity card | 의미 효과 × surface 효과 분해, win/tie/loss, strict-matched subset, 환율(paraphrase 1회 = 의미 변경 몇 회), fixed-surface monotonicity τ, 외부 타당성 ρ |
| "clinical" | clinical severity 주장 | **text-level semantic test**로만. 임상 중요도 주장 없음(38pP P4 동의). 전문의 검증은 저널 확장 |
| 선행연구 | ReEvalMed·CRIMSON·GEMA 등 미인용 | ReEvalMed, Beyond Scalar Scores, RadSEM, RadOT-Eval, CRIMSON, REREF 포지셔닝. REREF(의미 보존 재작성에 대한 민감도)와의 차이를 "표면을 고정했을 때 의미 민감도"로 명시 |

## 3. 데이터·설계·채점 변화

| 항목 | ARR May | ARR October |
|---|---|---|
| corpus | MIMIC-CXR만 (섹션 혼재) | **IU X-Ray(공개 트랙: judge·annotation·release) + MIMIC-CXR(로컬 트랙)**. 섹션 fallback 제거, 행정 헤더 분리, 문장 분리기 교체(`Dr.`, `a.m.`, 소수점, 번호 목록), 비식별 토큰 문장 제외 |
| 평가 세트 | subset200 / subset500 / full 5k가 실험마다 다름 (84Wq W3) | corpus당 **하나**: IU 890, MIMIC 1,050 target. 타입당 150, 패턴 상한 15%, report당 상한, hashlib seed |
| perturbation | 12타입, report마다 첫 매칭 하나 치환. benign = format / sentence_order / paraphrase_rule(정규식 4개, 81%가 `There is no → No`) | **7타입 × (P 의미 보존, C 의미 변경) matched 쌍**: 같은 문장, 같은 위치, 같은 surface 연산("C = P의 benign 변환 + flip" 또는 둘 다 1토큰 치환). anatomy, laterality, measurement(value/unit), negation(7 템플릿, 삽입형 금지), severity(adjacent/extreme), temporal, uncertainty(hedged↔definite 치환만). deletion/insertion은 같은 위치 치환이 불가 → 별도 층(통제 실패, 부록) |
| surface 잡음 | benign 타입이 곧 surface 변형 | **S0 / S1(문장 재배열) / S2(나머지 문장 LLM paraphrase + NLI 검증)** 3단계와 교차 → 6칸. 혼동 조건 2종과 통제 조건 3종을 한 세트에서 |
| shortcut 검증 | 없음 (Appendix B에 token_f1 Spearman 한 줄) | **surface-only 분류기 AUROC를 Table 1에** (v1 0.92–0.96, RaTE-Eval 0.89, 우리 혼동 1.00/0.98, 통제 S0 0.62–0.64, S2 0.52–0.54). meaning-blind baseline(Jaccard, token F1)을 모든 표 맨 위에 |
| metric | 6 (BERTScore distilbert, F1CheXbert, RadGraph, RaTEScore, Temporal, GREEN) + lexical | **15**: + BERTScore RoBERTa-L·DeBERTa-MNLI, SRR-BERT, RadCliQ-v1, **CRIMSON** (38pP P3). backbone·버전 전부 기재 |
| LLM judge | rebuttal에서 Llama-3-8B rubric 1개 (0/0.5/1 세 값, identity 하드코딩) | **6구성** (Llama-3.1-8B, Gemma-3-27B, Qwen3-32B ±thinking, gpt-oss-20b/120b) × prompt 3종, 확신도 연속 점수, identity도 모델 통과, 추론 채널 분리 파싱. **proprietary 2계열은 키 대기** |
| 사람 검증 | 3명, 480쌍 중 300쌍 단일, overlap 180 | 2명 **전수 이중** annotation PART1 504쌍(7타입 × 6칸 × 12) + PART2 204쌍(치환 패턴별), 칸·타입 blind, UNCERTAIN 기준·사유 필수. **회수됨, 미분석** |
| monotonicity | rule tier 0–4 Spearman | **고정 surface 사다리** M0(PPP)→M3(CCC): 모든 칸이 같은 세 위치를 편집. 대조군 K1·K2(기존 "오류 늘수록 edit 늘어나는" 사다리) |
| 외부 타당성 | 없음 (jzA1 J3) | RaTE-Eval Task 1·2 전문의 평점과의 metric 순위 상관: Ctrl-0 ρ 0.72 vs Conf-R 0.41 / Conf-P 0.29 |
| 공개 | 없음 (Software 1점) | 익명 repo 계획: 코드, IU 쌍·점수·judge 출력, MIMIC reconstruction script, rule 표 (미작성) |
| 통계 | candidate 단위 bootstrap | report-cluster bootstrap 1,000회, 쌍 비교, 기준선 대비 검정 |

## 4. 삭제·강등한 것

| 항목 | 처리 | 이유 |
|---|---|---|
| sensitivity card (기여 3) | 삭제 | novelty 없음 |
| inversion / blindness / rule-tier Spearman | 삭제 (tie 비율·strict subset·환율로 대체) | 정의가 코드와 달랐고 critical 5타입에만 계산됨 |
| composed stress (rebuttal) | 삭제 | benign counterpart가 identity와 동일(설계 결함) |
| finding_deletion / false_finding_insertion | 본문 제외, 부록 "통제 실패한 문장 단위 층" | 같은 위치 치환 불가. surface-only floor 0.89 |
| Khorasani 2003 인용 | 인용 안 함 | 본문에서 쓰지 않음 |
| "clinical severity" 서술 | 전부 제거 | text-level test |

## 5. 작업 중 바뀐 결정 (시간순)

1. 9/30 계획: shortcut floor 목표 0.45–0.55 → 10/1 Gate 1에서 S2만 충족(0.52–0.54), S0는 0.60–0.64. 단어 치환 설계의 잔여 비대칭(C는 원 토큰 삭제, P는 유지)으로 판단해 **수용 + 기준선 병기**로 진행(결정 D1, 사용자 승인 대기).
2. 10/1: 생성기 v1→v2 shape matching → v4(measurement 숫자 양쪽 변경) → v5(`target_negated` 플래그) → v6(negation fragment 제외). full 세트는 v5.
3. 10/3: 추가 세트(monotonicity, omission/insertion), gpt-oss 추론 채널 파싱 버그 발견 → 재실행(수치 차이 ≤0.01).
4. 10/5: **전문의 검증 포기** 확정. 대학원생 PART2(치환 패턴 검증)로 대체. 임상 중요도 주장 삭제.
5. 10/7 외부 리뷰 반영: headline을 "Jaccard를 못 이긴다"에서 "label·graph metric은 matched edit 대부분에 반응하지 않는다(tie)"로 교체; 공개 suite(RaTE-Eval) probe 추가; GREEN S2 하락이 paraphrase drift 탓이 아님을 두 가지로 확인; `rubric_unit` prompt로 judge 단위 변환 false alarm 원인 분리; errors prompt에서 gpt-oss가 가장 monotone → "judge는 grading 못 한다"를 "출력 형식의 성질"로 정정; 외부 타당성 문단 추가; 본문–표 불일치 10곳 수정.

## 6. 알려진 결함 (논문에 그대로 기재, `docs/internal_logs/9_extended_analysis.md` §F)

| ID | 내용 | 규모 | 처리 |
|---|---|---|---|
| D-1 | measurement:unit 하위타입 P 2토큰 / C 1토큰 → surface 불일치 | IU 49 / MIMIC 75 | 따로 보고, robustness 제외 |
| D-2 | 어색한 negation fragment | IU 2 / MIMIC 6 | 제외 수치 병기 |
| D-3 | 통제 S0 잔여 leak (probe 0.62–0.64, Jaccard 0.59–0.63) | 전체 | 기준선 병기, tie·strict subset |
| D-4 | omission/insertion 층 통제 실패 | 300 | 부록 |
| D-5 | S2 paraphraser(Qwen2.5)와 Qwen3 judge 같은 계열 | – | 표시 + 대체 paraphraser로 확인 |
| D-6 | P 치환 lexicon 전문의 미승인 | anatomy 33%, severity 66–69%, uncertainty 24–31% | 보수적 subset 병기, annotator PART2 |
| D-7/8 | IU measurement·uncertainty 94개; MIMIC measurement 88%가 기구 위치 | – | 본문 명시 |
| D-10 | `right-sided sided` 생성 | IU 2 | Limitations, 공개본 제거 |
| D-11 | S2 paraphrase 정도표현 drift | IU 124 / MIMIC 258 | P·C 동일 영향. 보존 subset으로 GREEN 결론 확인 |
| D-12 | 초안의 "measurement는 device 서술을 피한다"는 오기 | – | §4.2 수정 |
