# 1. ARR May 리뷰 분석

- 작성일: 2026-09-30
- 원본: `/home/irteam/junah-data-1/ARR_10/ClimSemBench_Review_ARR_5.md`
- Submission 7910, Preferred venue EMNLP, Long paper, Resources and Evaluation

---

## 1. 점수 요약

| | Reviewer jzA1 | Reviewer 84Wq | Reviewer 38pP | Meta (AC XnAy) |
|---|---|---|---|---|
| Overall | 3 (Findings) | 3 (Findings) | **2 (Resubmit)** | **2 (Resubmit)** |
| Soundness | 3 | 3 | 2.5 | – |
| Excitement | 2 | 3.5 | 2 | – |
| Confidence | 4 | 4 | 4 | – |
| Reproducibility | 5 | 3 | 5 | – |
| Datasets | 2 | 4 | 2 | – |
| Software | 1 | 4 | 1 | – |
| 성향 | 임상(영상의학) 관점 | benchmark 구성·분석 관점 | LLM-as-metric·novelty 관점 | novelty·impact |

- Soundness는 통과선이지만 **Excitement가 낮다** (2 / 3.5 / 2). 탈락 사유는 방법의 오류가 아니라 "새롭지 않다 + 최신 metric/LLM이 없다"이다.
- Software 점수 1이 두 명 → 코드/데이터 공개가 없다고 인식됨.

## 2. Meta-review 핵심

> "Overall, the novelty and impact of this work is pretty limited, and the finding that BERTScore is sensitive to surface changes is pretty well established already."

요구 사항 2가지
1. 리뷰어들이 제안한 fine-grained 분석을 논문에 반영
2. 더 최신 metric (38pP 제안)과 **더 최신 모델** 추가

→ 논문의 headline(abstract·TLDR·contribution 2)이 "BERTScore reversal"이었는데, AC는 바로 그 점을 "이미 알려진 사실"로 판단했다. **headline을 바꿔야 한다.**

---

## 3. 리뷰어별 지적 사항과 rebuttal 대응 현황

상태 표기: ✅ rebuttal에서 데이터로 대응 / 🟡 말로만 대응 / ❌ 미대응

### 3.1 Reviewer jzA1 (Overall 3)
| # | 지적 | rebuttal 대응 | 상태 | 재제출 시 필요한 것 |
|---|---|---|---|---|
| J1 | MIMIC 단일 기관. 다른 공개 corpus로 일반화 필요 | OpenI transfer check | ✅(약함) | 본문에 정식 cross-corpus 실험. GREEN도 같은 subset으로 |
| J2 | 의미 변화마다 임상적 중요도가 다름 (laterality·negation ≫ measurement·severity·uncertainty). clinical significance가 더 중요 | "construct가 다르다"고 설명 | 🟡 | 임상의 annotation 또는 최소한 clinical-significance tier를 외부 근거로 부여 |
| J3 | construct validity: 어떤 metric이 임상의 품질 평가와 가장 상관이 높은가 | 정의상 불가하다고 답변 | 🟡 | ReXVal / RadEvalX 등 radiologist error annotation과의 연결 분석 |
| J4 | 대학원생 annotator는 임상 경험 없음 | text-level 과제라 적절하다고 설명 | 🟡 | 영상의학과 전문의(공저자 가능성) subset 검증 |
| J5 | rule trigger 상세 필요 (uncertainty 표현 다양성 등) | trigger 목록 제시 | ✅ | 전체 rule 표를 부록에. **단 실제 코드와 일치시켜야 함** (`0_...md` §5.1) |
| J6 | UNCERTAIN 제외 근거. 양쪽으로 묶거나 multi-valued κ | 3가지 처리 + 3-class Fleiss κ | ✅ | 본문 반영 |
| J7 | uncertainty 낮은 agreement는 자연스러움 (Khorasani 2003 인용 제안) | 인용 약속 | ✅ | 인용 추가 |
| J8 | data release가 aggregate만인 것으로 보임 | per-example 공개 약속 | 🟡 | 실제 release 패키지(코드 + reconstruction script + 개별 judgment) 준비, 익명 repo 링크 |
| J9 | Impression/Findings 표기 (이탤릭 또는 대문자) | 수정 약속 | ✅ | 반영 |

### 3.2 Reviewer 84Wq (Overall 3, 가장 우호적)
| # | 지적 | rebuttal 대응 | 상태 | 재제출 시 필요한 것 |
|---|---|---|---|---|
| W1 | 단일 데이터셋. RadGraph 등은 MIMIC으로 개발되어 유리할 수 있음 | OpenI transfer | ✅(약함) | J1과 동일. 추가 corpus 고려 |
| W2 | perturbation-level breakdown과 failure mode 분석 부족 | 9타입 × 6 metric AUROC 표 | ✅ | 본문 메인 표/그림으로 승격 + 왜 실패하는지 메커니즘 분석 |
| W3 | 데이터 구성 혼란 (subset500, subset200, 5k, 2400, 36k/40k) | 계층 설명 | ✅ | **평가 세트를 하나로 통일**하는 것이 근본 해결 |

### 3.3 Reviewer 38pP (Overall 2, 결정적)
| # | 지적 | rebuttal 대응 | 상태 | 재제출 시 필요한 것 |
|---|---|---|---|---|
| P1 | ReEvalMed와 겹침. 무엇이 새로운 failure mode/결론인지 | 정성 비교표 | 🟡 | related work에 인용 + 차별점을 **실험으로** 보임 |
| P2 | edit이 local·explicit해서 LLM evaluator에게 너무 쉬움 | Llama-3-8B 0.76으로 "saturate 안 됨" 주장 | 🟡 | 강한 LLM으로 실제 검증. 쉬우면 더 어려운 tier 필요 |
| P3 | metric suite 불완전: CRIMSON, FineRadScore, RadEval 전체, CheXbert 변형, 여러 LLM backbone/prompt | Llama rubric 1개 추가 | ❌(대부분) | metric 확장 |
| P4 | clinical 해석 제한. text-level semantic sensitivity test로 framing | 동의 | ✅ | framing 수정 |
| **P5** | **(post-rebuttal) 최신 LLM 부재가 핵심 우려로 남음.** Gemini 3.1 Pro, Claude Opus, GPT-5.5, MedGemma, Qwen3.7 등 proprietary + open-weight 평가 요구 | – | ❌ | **재제출의 최우선 과제** |

---

## 4. 리뷰에서 드러난 구조적 문제

### 4.1 Headline이 약하다
- "BERTScore가 reversed"는 AC와 38pP 모두 "unsurprising / well established"로 평가.
- 게다가 audit 결과(`2_...md` B절) 이 reversal은 **edit 크기 차이에서 오는 artefact**다. benign은 4–46 토큰이 바뀌고 changed는 1 토큰이 바뀐다. 리뷰어가 데이터를 직접 보면 바로 지적할 수 있는 약점이다.

### 4.2 Novelty 포지셔닝이 없다
- 논문은 ReEvalMed를 인용하지 않았고 related work에 최신 meta-evaluation 연구가 빠져 있다.
- rebuttal에서 주장한 차별점 3가지 (deterministic single-factor 생성, identity-normalized penalty + inversion/blindness, 480쌍 human validation)는 "엔지니어링 차이"로 읽힌다. **새로운 결론**이 필요하다.

### 4.3 "LLM에게 너무 쉽다"는 의심에 답하지 못했다
- Llama-3-8B(2024)는 38pP가 명시적으로 "구식"이라고 지적.
- 실제로 강한 LLM이 0.95+를 기록하면 benchmark가 saturate된 것이므로, 그 경우를 대비한 **hard tier**가 있어야 한다.

### 4.4 임상 타당성
- jzA1(Confidence 4, 임상 배경)은 "clinical significance가 더 중요"하다고 봄. 저자 목록에 영상의학과 전문의로 보이는 공저자가 있다면 소규모라도 radiologist 검증을 넣는 것이 가장 효과적인 대응이다. (공저자의 역할은 사용자 확인 필요)

### 4.5 공개 자료
- Software 1점이 두 명. "We will release"만으로는 부족하고, 제출 시점에 익명 저장소가 있어야 한다.

---

## 5. 재제출 시 유의 사항 (ARR 절차)

- ARR resubmission은 이전 리뷰에 대한 **revision note(변경 사항 설명)** 를 요구하며, 같은 리뷰어/AC에게 재배정을 요청할 수 있다. May 제출본은 "This is not a resubmission"으로 표기되어 있었다.
- 재배정 요청 여부는 전략적 선택이다.
  - 같은 리뷰어 유지: jzA1·84Wq(둘 다 3점)는 우호적. 38pP의 P5만 해결하면 통과 가능성이 높다.
  - 새 리뷰어 요청: 38pP를 피할 수 있지만 3점 두 명도 잃는다.
  - 권장: **같은 리뷰어 유지** + P5를 정면으로 해결. (최종 결정은 사용자)
- 정확한 October cycle 마감일과 resubmission 양식은 ARR 공식 페이지에서 확인 필요.
