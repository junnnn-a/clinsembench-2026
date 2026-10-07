# 12. 논문 초안 v0 메모 (2026-10-07)

- 초안: `docs/paper/main.tex` → `docs/paper/main.pdf` (17쪽: 본문 8쪽 + Limitations·Ethics·참고문헌 + 부록)
- 빌드: `cd docs/paper && /home/irteam/junah-data-1/ARR_10/1_CAP/paper/tectonic -X compile main.tex` (acl.sty, acl_natbib.bst는 1_CAP/paper에서 복사)
- 표: `scripts/20_make_paper_tables.py` → `docs/paper/tables/*.tex`. **본문 표의 수치는 전부 이 스크립트가 결과 CSV에서 생성**한다. 본문 문장 속 수치는 손으로 옮겼으므로 결과가 바뀌면 다시 대조해야 한다
- 그림: `scripts/17_make_figures.py` → `docs/paper/figures/*.pdf`

## 1. 구성

| 절 | 내용 | 표·그림 |
|---|---|---|
| 1 Intro | v1에서 Jaccard = GREEN이었다는 관찰 → 혼동 → 설계 → 기여 3개 | Fig 1 (6칸 예시, IU 실제 문장) |
| 2 Related | metric / perturbation 메타평가(ReEvalMed, Beyond Scalar Scores, RadSEM, RadOT-Eval, REREF) / shortcut·contrast set | |
| 3 Diagnosis | surface-only probe, v1 0.92–0.96 / human 0.83, 방향이 구성에 의존 | Table 1 |
| 4 Design | 칸·비교, matched edit, S2 paraphrase, corpus, monotonicity 세트, 라벨 검증(**TBD**) | |
| 5 Setup | metric 15, judge 6, 통계 | |
| 6 Results | 6.1 혼동↔통제, 6.2 두 축, 6.3 judge, 6.4 monotonicity, 6.5 타입 | Table 2–4, Fig 2–3 |
| 7 Discussion | 권고 2가지 (meaning-blind baseline, surface-only predictability) | |
| 부록 A–I | rule 표, 세트 구성, 타입·하위타입, robustness, 분해·dose-response, judge 타입·prompt, CRIMSON 귀속, 통제 실패한 누락·삽입 층, prompt·구현 | |

조건 이름: `Ctrl-0/1/2` (같은 행 비교), `Conf-R` (C0 vs P1, 재배열형), `Conf-P` (C0 vs P2, paraphrase형).

## 2. TBD로 남긴 곳 (빨간 `[TBD: ...]`)

| 위치 | 필요한 것 |
|---|---|
| §4.6 Validation of Labels | 사람 annotation 결과 전체 (칸별 일치율, κ, 패턴 유지 규칙 적용 결과, 검증 세트 기준 주 결과) |
| §5 LLM judges, Table 2 캡션 | proprietary judge 2개 계열 이상 (IU) |
| Limitations | annotator 관련 문장, proprietary 결과 |
| Ethics | annotator 모집·보상·동의·심의 여부 |
| 부록 I | annotation 지침·배경·시간·일치도 표 |

TBD를 채우면 본문이 8쪽을 넘는다. 현재 본문은 8쪽을 정확히 채우고 Limitations가 8쪽 끝에서 시작한다. 사람 검증 문단(약 10줄)과 proprietary 행이 들어가면 약 15–20줄을 줄여야 한다. 후보: §6.5(타입)를 부록으로, Related의 shortcut 문단 축약.

## 3. 제출 전 반드시 확인할 것

### 참고문헌 (`references.bib`에 `VERIFY` 표시)
- arXiv 번호만 알고 **저자·정식 제목을 모르는 6건**: ReEvalMed(2510.00280), Beyond Scalar Scores(2606.18797), RadSEM(2606.17062), CRIMSON(2603.06183), REREF(2609.19093), RadOT-Eval(2606.08769). 저자 칸에 임시 문자열이 들어 있다. **그대로 제출하면 안 된다**
- 기억으로 적어 확인이 필요한 것: Khorasani 2003, RadEval, SRR-BERT, temporal F1 출처(Bannur 2023이 맞는지), FineRadScore, Gemma 3 / Qwen3 / Llama 3 / gpt-oss 보고서
- 본문에서 이 논문들에 대해 한 서술(예: "ReEvalMed 저자들이 surface 차이를 언급했으나 통제하지 않았다", "RadSEM이 동의어 치환을 썼다", ReEvalMed의 BLEU 78.5 vs 41.9)은 문서 3 §1.3에 사용자가 정리한 내용을 그대로 옮긴 것이다. **원문 대조 필요**

### 본문 수치
- 문장 속 수치는 10/3 재분석 결과 기준. 표와 어긋나는 곳이 없는지 최종 대조 필요
- "15 metrics": Jaccard, token F1, BLEU, ROUGE-L, BERTScore ×3, F1CheXbert, temporal F1, SRR-BERT, RadGraph, RaTEScore, RadCliQ, GREEN, CRIMSON = 15 ✔. "six LLM judges" = 6개 설정(Qwen3 thinking 포함) ✔
- "1,940 targets" = 890 + 1,050 ✔

### 새로 발견한 결함 (문서 9 §F 목록에 추가)
| ID | 내용 | 처리 |
|---|---|---|
| D-10 | 원문이 이미 `right sided`인 문장에 laterality 규칙이 적용되어 `right-sided sided`가 생김 (하이픈 없는 표기를 제외 조건이 놓침) | 건수 집계 후 robustness 제외 목록에 추가. 생성기에 제외 규칙 추가 |
| D-11 | S2 paraphrase가 `No large pleural effusion` → `No significant pleural effusion`처럼 정도 표현을 바꾼 사례. NLI·어휘 guard가 못 잡음 | P와 C에 동일하게 들어가므로 통제 비교에는 영향이 작지만, Conf-P와 surface 효과 추정에는 잡음. Limitations에 기재함. 사람 검증에서 P2 칸 일치율로 규모 확인 예정 |

## 4. 제목

초안 제목은 `Surface or Semantics? Disentangling What Radiology Report Metrics Measure with Factorial Minimal Pairs`. 주장이 바뀌어 제목을 바꿨고 benchmark 이름 `ClinSemBench`은 유지했다. 재제출 양식에 제목 변경 사유를 적어야 한다. 원래 제목을 유지하려면 `\title`만 바꾸면 된다 (사용자 결정 D5).

## 5. 아직 안 한 것

- revision note (리뷰 지적별 point-by-point). 재료는 문서 3 §8
- release 패키지 (익명 repo)
- PDF를 눈으로 확인하지 못했다: 이 서버에 PDF 렌더러가 없어 쪽수·텍스트 추출로만 점검했다. **표 배치와 그림 크기는 직접 열어 확인 필요**
- 부록 rule 표에 overfull 경고(약 19pt)가 남아 있다
- checklist 답변


## 6. 10/7 리뷰 반영 후 상태 (v1)

- 리뷰 대응 내역과 결정은 `docs/13_review_1007_response.md`. v0는 `docs/paper/main_v0_1007.tex`로 보존.
- 구성 변경: Table 2에 `tie`·`strict` 열, Table 1에 RaTE-Eval 행(우리 세트는 IU/MIMIC 한 행), Table 3(judge 칸별)은 부록으로, Table 4는 본문 12행 요약 + 부록 전체판(errors prompt judge 포함). Fig 2는 부록, Fig 3은 1-panel(IU)·부록에 2-panel. §6.1 끝에 "Controlled scores track radiologist agreement" 문단. 부록 신설: All Comparisons and Outcome Shares, Robustness of the Paraphrase Layer, RaTE-Eval(합성 과제 표 + 외부 타당성 표), Monotonicity: All Scorers, rubric-unit 표.
- 본문 수치는 전부 10/7 재분석(`8`·`11`·`14`·`18`·`21`·`23`·`24`) 기준. Qwen3-thinking MIMIC이 채워지면서 바뀐 표 수치는 그 행뿐.
- 참고문헌: `VERIFY` 문구 제거, 6건 + RadEval·SRR·FineRadScore·Libra(Temporal F1 출처)·Gemma 3·Qwen3·Llama 3·gpt-oss 확인. Khorasani 2003은 인용하지 않음.
- 남은 TBD는 사람 검증(§4.6, Limitations, Ethics, 부록 I)과 proprietary judge(§5, Table 2 caption, Limitations)뿐.
- 분량: TBD를 채우면 다시 넘친다. 후보 삭감: §6.1 "Rankings change" 문단, §4.5 K1/K2 설명 축약, Fig 3을 부록으로.
- 아직 안 한 것: revision note, release 패키지(D-10 2건 제거), checklist, PDF 육안 확인(표 2·4의 열 간격, 부록 rule 표 overfull 19pt).
