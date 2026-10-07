# 작업 로그 원본 (9/30 – 10/7, 시간순)

실험 진행 중 작성한 내부 문서를 그대로 옮긴 것. 결정의 근거와 실패 기록이 모두 들어 있다. 요약본은 `docs/01`–`07`.

| 파일 | 날짜 | 내용 |
|---|---|---|
| `0_prior_paper_and_experiment_analysis.md` | 9/30 | ARR May 제출본을 코드·데이터·결과 파일 기준으로 감사: 실제 파이프라인, 결과 인벤토리, 논문–코드 불일치 |
| `1_review_analysis.md` | 9/30 | 리뷰 3건 + 메타리뷰 분석, 지적별 rebuttal 대응 현황 |
| `2_audit_findings_and_revision_plan.md` | 9/30 | **감사 결과 A–F**(bag-of-words baseline = GREEN, BERTScore reversal = edit 크기 confound, 비문 규칙, 섹션 fallback, 검증 구조) + 첫 보완 계획 E1–E9 |
| `3_experiment_plan.md` | 9/30 (10/1 갱신) | **확정 계획서**: 주장, factorial 설계(칸·조건·규칙·제약·규모), X1–X6, 일정, Gate 1·2, ARR·PhysioNet 규정 확인 |
| `4_e1_x1_pilot_build_log.md` | 10/1 | 환경 구축(vLLM 우회책), 코퍼스 재구축 통계, 생성기 v1→v4 shape matching, pilot shortcut floor, S2 paraphrase |
| `5_gate1_pilot_results.md` | 10/1 | Gate 1 GO 판정, pilot 결과(혼동 vs 통제, 분해, judge 칸별) |
| `6_x5_annotation_package.md` | 10/1 (10/5 갱신) | 사람 검증 패키지 설계 (전문의 층은 폐기) |
| `7_x3_existing_benchmark_audit.md` | 10/1 | v1·우리 세트 surface probe Table 3 초안 |
| `8_full_results.md` | 10/3 (10/7 정정) | **full 세트 주 결과**: 혼동 vs 통제, 분해, judge 칸별·타입별, prompt 민감도, gpt-oss 파싱 버그·재실행, 실패 기록 |
| `9_extended_analysis.md` | 10/3 | 하위타입, dose-response, 대비 검정, 혼합효과, CRIMSON 오류 귀속, robustness, **결함 목록 D-1~D-12** |
| `10_status_1003.md` | 10/3 (10/5 주석) | 중간 종합 현황, monotonicity·OI 결과, 준비 요청 A·B, 결정 D1–D5 |
| `11_annotation_handover.md` | 10/5 | annotator 2명 전달 안내 v2 (전문의 없는 설계), 회수 후 분석 규칙(사전 고정), 논문 기재 항목 |
| `12_paper_draft_notes.md` | 10/7 | 논문 초안 v0/v1 메모: 구성, TBD, 확인 사항, 제목 |
| `13_review_1007_response.md` | 10/7 | **10/7 외부 리뷰 대응**: 지적별 결정, 새 실험 결과(RaTE-Eval probe, tie·strict, 환율, S2 robustness, rubric_unit, errors×mono, 외부 타당성), 논문 수정 내역, 서버 문제 |

주의: `5`의 gpt-oss-20b 수치는 옛 파서 결과(차이 ≤0.01, `8` §6). `8` §3·§4의 일부 수치는 10/7 재분석으로 갱신됐고 최종은 `paper/tables/`와 `docs/04`.
