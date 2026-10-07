# 07. 미결 사항·결정 필요·리스크

## 1. 결정이 필요한 것 (D1–D5는 10/3 현황 문서의 번호)

| # | 질문 | 권장 | 근거 |
|---|---|---|---|
| D1 | 통제 S0의 surface-only floor 0.62–0.64 (계획 기준 0.45–0.55) 수용? | **수용** + meaning-blind 기준선·tie·strict subset 병기 (논문은 이미 이 방식) | 단어 치환 설계의 잔여 비대칭. S2는 0.52–0.54로 충족. strict subset에서도 결론 유지 |
| D2 | omission/insertion 층 처리 | 부록 "통제 실패 사례" (논문 부록 M, 현재 반영) | 본문에 넣으면 공격 지점, 빼면 "왜 없느냐" |
| D3 | D-1(measurement unit) | 제외 병기만 (현재). MIMIC 재생성은 시간 남으면 | IU는 annotation 때문에 동결 |
| **D4** | **10/12 제출 vs 1월 cycle** | 사전 규칙: proprietary judge 2계열 + annotation 분석이 10/9까지 되면 10/12. 아니면 1월 (ACL 2027 마지막 cycle은 1월; commit 가능 여부는 ACL CFP 확인) | 38pP P5가 남으면 같은 리뷰어에게 같은 지적을 받음 |
| D5 | 제목 변경 유지? | 새 제목 유지 (주장이 바뀜). 재제출 양식에 사유 기재 | benchmark 이름은 유지 |
| D6 | annotation 결과를 논문에 어떻게 서술할지 | `returned/` 시트의 출처(사람 2명 독립 수행 여부) 확인 후 결정 | 10/5 메모: LLM 라벨은 LLM으로 명시하기로 했었음. 사람 라벨과 섞어 κ로 보고하지 않음 |
| D7 | 같은 리뷰어 재배정 | 유지 (기본값) | jzA1·84Wq가 3점. 38pP의 P5만 해결하면 통과 가능성 |

## 2. 제출 전 공저자 확인·준비 요청

| 항목 | 내용 |
|---|---|
| **API 키** | Claude / GPT / Gemini 중 2계열 이상. 환경변수(`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`). IU 6,230행 × rubric(+errors). `9_llm_judge.py`에 API 경로 추가 필요(현재 vLLM 전용; `envs/llm`에 openai·anthropic 패키지는 설치됨). MIMIC에는 쓰지 않음 |
| **annotation** | `data/annotation/returned/` 4개 시트의 출처·절차 확인. 논문 기재용: annotator 배경(과정·전공·경력), 비저자 여부, May annotator와 동일 인물인지, 모집 방법, 보상, 동의, PART별 소요 시간, IRB 여부(May는 미신청) |
| HF 약관 | `google/medgemma-27b-text-it`, `meta-llama/Llama-3.3-70B-Instruct`, `rajpurkarlab/ReXGradient-160K` (현재 403) — 선택 |
| 데이터 | ReXVal / ReEvalMed (PhysioNet credentialed) — 있으면 진단의 외부 증거가 결정적으로 강해짐 — 선택 |
| OpenReview | 7910 링크, 전 저자 프로필(ORCID 등), service contributor 지정(제출 후 48시간 내), 마감 시각(AoE 여부) |
| 참고문헌 | FineRadScore venue(MLHC 2024, PMLR 252)는 리뷰 정보 그대로, 미확인. 나머지는 arXiv 확인 완료 |
| PDF 육안 확인 | 서버에 렌더러 없음. Table 2·4 열 간격, Fig 1 폭, 부록 rule 표 overfull 19pt |
| 분량 | TBD(사람 검증 문단 ≈10줄, proprietary 행)를 채우면 본문 8쪽 초과 → §6.1 "Rankings change" 문단, §4.5 K1/K2 설명, Fig 3 부록 이동 중 선택 |

## 3. 알려진 결함·한계 (논문 Limitations·부록에 기재됨)

- 통제 S0 잔여 leak (D-3): probe 0.62–0.64, Jaccard 0.59–0.63. 기준선·tie·strict로 대응.
- measurement:unit 하위타입(D-1) surface 불일치; negation fragment(D-2); `right-sided sided`(D-10, IU 2건, 공개본 제거).
- omission/insertion 층 통제 실패(D-4). rule 기반 edit는 실제 생성 시스템의 오류 분포를 덮지 않음.
- S2 paraphrase 정도표현 drift(D-11) 가능; paraphraser(Qwen2.5)와 Qwen3 judge 같은 계열(D-5).
- uncertainty·severity 라벨은 한 가지 해석(REREF taxonomy는 일부 C를 benign으로 봄); 전문의 lexicon 검토 없음(D-6).
- MIMIC measurement 88%가 기구 위치(D-8); IU measurement·uncertainty 94개(D-7); monotonicity·OI 세트는 MIMIC만.
- RaTE-Eval 합성 과제 원문은 lexical 정렬로 복원(공개본에 원문 없음); RaTE-Eval은 CXR 외 모달리티 위주.
- RadEval-BERTScore 실행 불가, FP8 모델 실행 불가(nvcc), GREEN error category 분석 미완.
- 비임상 annotator 2명, 임상 중요도 미검증, proprietary judge 미완.

## 4. 리스크

| 리스크 | 판단 |
|---|---|
| API 키가 10/9까지 안 옴 | 사전 규칙상 1월 cycle. open-weight만으로 내면 38pP P5 재지적 확실 |
| annotation 출처·절차가 논문 서술과 안 맞음 | 서술을 사실대로. LLM 라벨이면 LLM으로 명시하고 사람 κ로 보고하지 않음 |
| 강한 judge 천장 → "LLM 쓰면 된다"로 읽힘 | prompt 민감도(0.93→0.34), rubric 비단조성, uncertainty 누락, 비용, 외부 타당성으로 대응 (논문 §6.3–6.4, §7) |
| severity "chance 미만"이 lexicon 판정에 민감 | 보수적 subset 병기 (0.07–0.13 상승해도 방향 같음) |
| 본문 8쪽 초과 | §2 위 후보 삭감 |
| GPU 공유 | 남은 GPU 작업 없음 (proprietary는 API) |

## 5. 1월 cycle / 저널 확장 후보

- 전문의 lexicon 승인·쌍 검증·임상 중요도 등급(jzA1 J2·J4).
- ReEvalMed·ReXVal·ReXErr·RadEvalX 데이터 직접 probe(진단의 외부 증거).
- MedGemma-27B, Llama-3.3-70B, 세 번째 corpus(ReXGradient).
- measurement unit 규칙 교체(`4.7 cm → 4.7 centimeters` vs `4.7 mm`) 후 MIMIC 재생성.
- 문장 단위 오류(누락·삽입)의 surface 통제 설계.
- GREEN error category 귀속, RadGraph entity 수준 누락 분석(E8 잔여).
