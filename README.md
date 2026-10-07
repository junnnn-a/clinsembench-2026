# ClinSemBench — ARR October 2026 재제출 작업 현황 (2026-10-07 기준)

**논문 (현재 제목)**: *Surface or Semantics? Disentangling What Radiology Report Metrics Measure with Factorial Minimal Pairs*
**Benchmark 이름**: ClinSemBench (ARR May 제출본과 동일. 구 ClinSevBench)
**이전 제출**: ARR May 2026, Submission 7910 "ClinSemBench: Stress-Testing Radiology Report Metrics with Minimal Pairs" (리뷰 3 / 3 / 2, meta 2 → resubmit)
**마감**: ARR October 2026 — **10월 12일** (전 저자 reviewer 등록 10월 14일)

이 폴더는 공저자 공유용으로 코드·문서·핵심 결과를 한곳에 모은 것입니다. 원본 작업 디렉토리(`ARR_10/2_ClimSemBench`)에서 MIMIC-CXR 파생 데이터(PhysioNet 규정상 재배포 불가), 모델 원출력(judge raw, 37MB), conda 환경, 로그는 제외했고, 그 외 재현에 필요한 코드·IU X-Ray 데이터·집계 결과는 모두 들어 있습니다.

---

## 1. 한 문단 요약

영상의학 판독문 생성 metric을 검증하는 perturbation suite(의미 보존 edit vs 의미 변경 edit를 만들고 후자에 더 큰 penalty를 주는 metric이 좋다는 프로토콜)는 **의미 변화와 surface 거리를 혼동**한다. 두 종류의 edit는 바꾸는 텍스트 양이 체계적으로 달라서, 의미를 보지 않는 surface 통계만으로 라벨을 맞힐 수 있다 (공개 RaTE-Eval 합성 과제 AUROC 0.89, 우리 ARR May suite 0.92–0.96, 그 human 라벨에서도 0.83). 혼동의 **방향은 benign edit를 어떻게 만들었느냐가 정한다**(재배열형이면 overlap metric이 "정방향", 자유 재작성형이면 "역방향"). ClinSemBench v2는 IU X-Ray(890 target)와 MIMIC-CXR(1,050 target)에서 **같은 target 문장의 같은 위치에 같은 surface 연산으로** 의미 보존 edit(P)와 의미 변경 edit(C)를 만들고, 이를 문맥 surface 잡음 3단계(S0 없음 / S1 문장 재배열 / S2 나머지 문장 paraphrase)와 교차한 factorial minimal-pair benchmark다. surface를 통제하면 결론이 바뀐다: BERTScore "reversal"은 사라지고(paired accuracy 0.00 → 0.63–0.66), F1CheXbert·Temporal F1은 matched 쌍의 89–96%에서 동점, RadGraph F1은 token overlap이 정확히 같은 subset에서도 chance(0.53–0.54), GREEN은 문맥 paraphrase에서 8–9점 하락(CRIMSON은 불변). 문맥 paraphrase 1회의 penalty는 RadGraph에서 matched 의미 변경 18회, BERTScore에서 50회 이상에 해당한다. surface를 고정한 monotonicity 검사에서 BLEU·RadGraph는 기존 "오류 늘수록 edit 늘어나는" 사다리의 완벽한 단조성을 잃는다(Kendall τ < 0.2). 추론형 LLM judge는 0.95–0.97로 천장에 가깝고, 오류를 나열하게 하면 가장 monotone한 scorer가 된다; 작은·비추론 judge는 paraphrase 속 확신도 변화를 놓치고 prompt에 민감하다. 통제된 비교의 metric 순위는 RaTE-Eval 전문의 평점과의 상관 순위와 일치(ρ 0.72)하고, 혼동된 비교는 그렇지 않다(0.29–0.41). 권고: perturbation 메타평가마다 meaning-blind baseline과 surface-only predictability를 함께 보고할 것.

## 2. 지금 상태 (요약)

| 항목 | 상태 |
|---|---|
| 데이터 재구축 + factorial 세트 (IU 890, MIMIC 1,050 target × 7칸) | **완료** (IU 세트는 annotation 원천이라 동결) |
| metric 15종 + LLM judge 6구성(open-weight) × prompt 3종 채점 | **완료** (GPU 실험 전부 10/7 09:52 종료) |
| 확장: fixed-surface monotonicity(MIMIC 300), 누락·삽입 층(MIMIC 300, 통제 실패 → 부록), 하위타입·dose-response·robustness | **완료** |
| 10/7 외부 리뷰 대응 실험 (공개 suite RaTE-Eval probe, strict-matched subset, 환율, 대체 paraphraser, rubric_unit prompt, 외부 타당성) | **완료** |
| 논문 v1 (`paper/main.pdf`, 24쪽: 본문 8쪽 + 부록) | **작성됨**. `[TBD]` 7곳 = 사람 검증·proprietary judge |
| **사람 annotation (A·B, PART1 504 + PART2 204쌍)** | 회수 파일이 `data/annotation/returned/`에 있음(10/7 00:35). **아직 분석·논문 반영 안 됨**. 출처 확인 필요 (§3 `07_open_issues`) |
| **Proprietary LLM judge (2계열 이상, IU만)** | **미착수** — API 키 없음. 사전 Gate 2 규칙상 제출 조건 |
| revision note, release 패키지, checklist, PDF 육안 확인 | **미착수** |

상세: [`docs/01_status_1007.md`](docs/01_status_1007.md)

## 3. 문서 안내

| 파일 | 내용 |
|---|---|
| [`docs/01_status_1007.md`](docs/01_status_1007.md) | **현재 상황**: 완료/미완/대기 항목, 남은 일, 일정 |
| [`docs/02_changes_from_arr_may.md`](docs/02_changes_from_arr_may.md) | **이전 논문(ARR May)에서 달라진 점**: 감사에서 드러난 문제, 프레이밍·설계·데이터·metric·judge·검증 대응표, 삭제한 것 |
| [`docs/03_design_and_pipeline.md`](docs/03_design_and_pipeline.md) | **실험을 어떻게 했는가**: 칸·조건 정의, edit 규칙, S2 paraphrase, shortcut floor, metric·judge 설정, 통계, 스크립트 실행 순서, 환경 |
| [`docs/04_results_summary.md`](docs/04_results_summary.md) | **핵심 결과 표** (수치 출처 명시): 진단, 혼동 vs 통제, judge, monotonicity, 환율, robustness, 외부 타당성 |
| [`docs/05_review_response_map.md`](docs/05_review_response_map.md) | ARR May 리뷰어·AC 지적 → 대응 위치. 10/7 외부 리뷰 반영 내역 |
| [`docs/06_annotation_instructions_KR.md`](docs/06_annotation_instructions_KR.md), `_EN.md` | annotator에게 준 지침 (그대로) |
| [`docs/07_open_issues.md`](docs/07_open_issues.md) | 미결 사항·결정 필요·알려진 결함·리스크 |
| `docs/internal_logs/` | 9/30–10/7 작업 로그 원본 14편 (색인 `docs/internal_logs/README.md`) |
| `docs/prior_submission/` | ARR May 제출본 PDF·tex·리뷰 전문 |

## 4. 코드·데이터·결과

| 경로 | 내용 |
|---|---|
| `scripts/` | 전체 파이프라인 (`0_audit…` ~ `25_merge_iualt.py`, 실행 셸, `env_llm.sh`, `gpu_wait.sh`). 설명 `scripts/README.md` |
| `data/pairs_iu/` | **IU X-Ray factorial 세트** `full_iu_all.csv` (890 target × 7칸, 동결본), target 목록, paraphrase 로그, 대체 paraphraser 세트 `full_iualt_all.csv` |
| `data/corpus/` | IU 섹션 코퍼스(재파싱본), 두 corpus 통계 |
| `data/annotation/` | 지침, blinded 시트, 정답 키(annotator에게 전달 금지), `returned/` 회수 시트 4개 |
| `data/rate_eval_task3_aligned.csv` | RaTE-Eval 합성 과제 원문 복원 결과 (CC-BY-4.0) |
| `results/full_iu/`, `results/full_mimic/` | 주 분석(`REPORT.md`, `JUDGES.md`, 조건별·타입별 CSV), `extended/`, `review1007/` |
| `results/mimic_monotonicity/`, `results/mimic_omission_insertion/`, `results/iu_alt_paraphraser/` | 확장 세트 분석 |
| `results/x3_benchmark_audit/`, `results/external_validity/`, `results/v1_audit/` | 기존 benchmark probe(v1·RaTE-Eval), 전문의 평점 상관, ARR May 감사 |
| `paper/` | `main.tex`(v1), `main_v0_1007.tex`, `references.bib`, `tables/*.tex`(스크립트 자동 생성), `figures/`, `main.pdf` |

**제외한 것**: MIMIC-CXR 코퍼스·쌍·점수·judge 출력(PhysioNet 파생 데이터; 원본 `data/corpus/mimic_sections.csv`, `data/pairs/full_mimic*`, `results/2_full_mimic/{scores,judges}`), IU 원점수·judge 원출력(`results/2_full_iu/{scores,judges}`, 47MB — 요청 시 전달), conda env, 로그, HF 모델.

## 5. 재현 (요약)

```bash
# env 1: metric 채점  /opt/conda/envs/clinsev (radeval 2.2.1, torch 2.2.2)   env 2: LLM  envs/llm (vLLM 0.30) — source scripts/env_llm.sh
python scripts/2_prepare_corpora.py                                   # 섹션 재파싱·문장 분리
python scripts/3_generate_factorial_pairs.py --corpus iu              # 7타입 P/C matched 쌍 후보
python scripts/4_sample_targets.py --corpus iu --tag full             # 타입별 150 target, 패턴 상한, shape 균형
$PY scripts/5_paraphrase_context.py --corpus iu --tag full            # S2 (Qwen2.5-7B + NLI 검증) → data/pairs/full_iu_all.csv
python scripts/6_shortcut_floor.py --pairs_csv data/pairs/full_iu_all.csv --out_csv results/2_full_iu/shortcut_floor_all.csv
python scripts/7_score_metrics.py --pairs data/pairs/full_iu_all.csv --out results/2_full_iu/scores --metrics lexical,bertscore,f1chexbert,srrbert,radgraph,ratescore,temporal,radcliq,green
$PY scripts/10_crimson.py --pairs ... ; $PY scripts/9_llm_judge.py --pairs ... --model Qwen/Qwen3-32B --prompt rubric
python scripts/8_analyze_factorial.py --pairs data/pairs/full_iu_all.csv --scores results/2_full_iu/scores results/2_full_iu/judges --out results/2_full_iu/analysis
python scripts/11_judge_cells.py ... ; python scripts/14_extended_analysis.py --corpus iu mimic ; python scripts/18_analyze_monotonicity.py
python scripts/21_review_reanalysis.py ; python scripts/22_probe_public_suites.py ; python scripts/23_external_validity.py --analyze ; python scripts/24_review_followup.py
python scripts/20_make_paper_tables.py ; python scripts/17_make_figures.py
cd docs/paper && tectonic -X compile main.tex
```
전체 큐는 `scripts/run_full.sh`(IU+MIMIC full), `run_set.sh <tag>`(세트별 범용), `run_review_final.sh`(10/7 추가 실험). 자세한 순서는 [`docs/03_design_and_pipeline.md`](docs/03_design_and_pipeline.md) §3.
