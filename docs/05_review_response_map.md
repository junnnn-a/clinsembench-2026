# 05. ARR May 리뷰 → 재제출 대응 매핑

- 점수: jzA1 3 (Soundness 3, 임상 관점) / 84Wq 3 (Soundness 3, 가장 우호적) / 38pP **2** (Soundness 2.5, LLM-as-metric·novelty 관점) / **Meta 2 resubmit**. Software 1점 × 2. 리뷰 전문: `docs/prior_submission/ARR_May_reviews_7910.md`.
- Meta-review 요지: "novelty·impact 제한, BERTScore가 surface change에 민감하다는 것은 이미 알려진 사실". 요구 (1) fine-grained 분석 반영 (2) 최신 metric·최신 모델 추가.
- revision note(point-by-point)는 아직 미작성. 아래 표가 재료.

## Meta-review / AC

| 요구 | 대응 | 논문 위치 |
|---|---|---|
| novelty 제한, BERTScore는 알려진 사실 | headline 교체: reversal이 edit 크기 artefact임을 보이고(진단), 통제 설계로 "통제하면 무엇이 바뀌는가"를 기여로 | §1, §3, §6.1 |
| fine-grained 분석 | 타입별 표 본문 §6.5 + 하위타입(부록 C), CRIMSON 오류 귀속(부록 L), dose-response(부록 E) | §6.5, 부록 |
| 최신 metric | CRIMSON(2026), RadCliQ, SRR-BERT, BERTScore 3종 backbone | §5 |
| 최신 모델 | Qwen3-32B(±thinking), Gemma-3-27B, gpt-oss-20b/120b, Llama-3.1-8B. **proprietary 2계열은 키 대기(TBD)** | §5, §6.3 |

## Reviewer 38pP (결정적, OA 2)

| # | 지적 | 대응 |
|---|---|---|
| P1 | ReEvalMed와 겹침; 새로운 failure mode·결론이 무엇인가 | ReEvalMed를 인용·비교(§2), 그 공개 표가 surface 혼동을 보임을 분석(§3), 같은 혼동을 우리 세트의 Conf-P로 재현. 새 결론: 혼동 방향이 구성에 의존, 통제 시 BERTScore reversal 소멸·label/graph metric tie·GREEN paraphrase 취약·fixed-surface monotonicity 반례 |
| P2 | edit이 local·explicit해서 LLM에게 너무 쉬움 | 그렇다고 답함: 추론 judge는 Ctrl-0·Ctrl-2에서 0.95–0.97. 그것을 **통제 조건에서 처음** 보임. 남는 실패를 명시(중간급 모델의 단위 변환·severity 동의어 오경보, paraphrase 속 uncertainty 누락, prompt 민감도, rubric judge의 비단조성). S2가 hard tier |
| P3 | metric suite 불완전 (CRIMSON, FineRadScore, RadEval 전체, CheXbert 변형, LLM backbone/prompt) | 15 metric + judge 6구성 × prompt 3종. FineRadScore·GEMA·RadEval-BERTScore 제외 사유 Limitations |
| P4 | clinical 해석 제한 → text-level semantic test로 framing | 동의. 전면 적용. "clinical"을 주장에 쓰지 않음 |
| **P5** | (post-rebuttal) 최신 LLM 부재 — Gemini·Claude·GPT·MedGemma·Qwen3 | open-weight 최신 계열 완료. **proprietary 2계열 필요 (Gate 2)**. MedGemma-27B는 HF 403 |

## Reviewer jzA1 (임상, OA 3)

| # | 지적 | 대응 |
|---|---|---|
| J1 | MIMIC 단일 기관 | IU X-Ray를 공개 주 트랙으로, MIMIC은 로컬 트랙. 두 corpus 결과 일치 |
| J2 | 의미 변화마다 임상 중요도 다름 | **실험으로 답하지 않음** (전문의 검증 포기, 10/5). 임상 중요도 주장 없음, Limitations에 저널 확장 명시 |
| J3 | construct validity: 어느 metric이 임상의 평가와 상관 높은가 | RaTE-Eval 전문의 평점(Task 1·2)과의 외부 타당성: 통제 열의 metric 순위가 전문의 순위와 일치(ρ 0.72), 혼동 열은 불일치 (§6.1 끝, 부록 I) |
| J4 | annotator 임상 경험 없음 | 비임상 annotator 2명 전수 이중 annotation. Limitations 명시. 전문의는 저널 확장 |
| J5 | rule trigger 상세 | 부록 A rule 표 (코드와 일치) |
| J6·J7 | UNCERTAIN 처리, κ | 지침에 UNCERTAIN 기준 명시, 3-class/2-class κ와 처리 3가지 보고 예정(annotation 분석 후). Khorasani 인용은 하지 않음 |
| J8 | per-example 공개 | 익명 repo 계획: IU 쌍·점수·judge 출력·개별 judgment (미작성) |
| J9 | 표기 | 반영 |

## Reviewer 84Wq (OA 3)

| # | 지적 | 대응 |
|---|---|---|
| W1 | 단일 데이터셋, RadGraph 등이 MIMIC에 유리 | IU + MIMIC |
| W2 | perturbation-level breakdown, failure mode 분석 | §6.5 타입별, 부록 C 하위타입, CRIMSON 오류 귀속, tie 분해, 환율 |
| W3 | 데이터 구성 혼란 (subset500/200/5k) | corpus당 세트 하나 |

## 10/7 외부 리뷰 (초안 v0에 대한 내부 검토) 반영 — `docs/internal_logs/13_review_1007_response.md`

| 지적 | 결정 |
|---|---|
| 진단 증거가 v1 하나뿐, "widely reported" 과장 | 공개 suite RaTE-Eval probe 추가(0.89), 문구 수정. ReXErr·ReXVal·RadEvalX·ReEvalMed 직접 probe는 데이터 없어 보류 |
| REREF와 겹침 | Related에 REREF 서술, 기여 3을 "표면을 고정했을 때 의미 민감도"로 좁힘 |
| uncertainty·severity 라벨이 외부 taxonomy와 충돌 | 논쟁 패턴 제외 subset 재분석, "결함"이 아니라 "scorer가 무엇을 세는가의 차이"로 서술, Limitations에 "라벨은 한 해석" |
| 통제가 깨끗하지 않은데 headline이 누수에 기댐; F1CheXbert 0.52는 tie | win/tie/loss·strict-matched subset 열 추가, headline을 "matched edit 대부분에 반응하지 않는다"로 |
| GREEN S2 하락이 drift 탓일 수 있음 | 정도표현 보존 subset + 대체 paraphraser(Llama + guard)로 재확인 → 유지 |
| judge 결론에 prompt가 섞임 | `rubric_unit` prompt, errors × monotonicity, Qwen3-thinking MIMIC 추가. "grading 못 함" → 출력 형식의 성질로 정정 |
| abstract 과장, 본문–표 불일치 10곳 | 전부 CSV 대조 수정 |
| "so what" | 외부 타당성 문단 (RaTE-Eval 전문의 평점) |
| 서지 6건 | arXiv에서 저자 전체 확인. Temporal F1 출처는 Bannur 2023이 아니라 Libra(Zhang et al., Findings ACL 2025)로 교체 |
| 수용 안 함 | 전문의 1명 lexicon 검토(사용자 결정), Table 2의 ↓ 표식 제거(통계적 사실이라 유지, 해석은 tie·strict로) |
