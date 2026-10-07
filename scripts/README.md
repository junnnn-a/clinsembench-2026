# scripts/

번호 = 대체로 실행 순서. 모든 스크립트는 레포 루트(`NEW = scripts/..`) 기준으로 `data/`, `results/`에 읽고 쓴다. 두 개의 env를 쓴다: **clinsev**(metric 채점·분석, `/opt/conda/envs/clinsev/bin/python`)와 **llm**(vLLM, `envs/llm/bin/python`; 반드시 `source scripts/env_llm.sh` 후 `$PY`).

| 파일 | 역할 | env |
|---|---|---|
| `0_audit_prior_experiment.py`, `1_audit_trivial_baseline_human_labels.py` | ARR May 실험 감사 (OLD 디렉토리 읽기 전용) → `results/0_audit/` | clinsev |
| `2_prepare_corpora.py` | IU(OpenI csv)·MIMIC(전처리 csv의 text 재파싱) 섹션·문장 분리, deid 플래그 → `data/corpus/` | clinsev |
| `3_generate_factorial_pairs.py` | 7타입 P/C shape-matched 후보 전수 생성 (v6) | clinsev |
| `4_sample_targets.py` | 타입당 n, 패턴 상한, report 상한, shape 균형, 비부정 우선 → `data/pairs/{tag}_{corpus}_{targets,S0S1}.csv` | clinsev |
| `5_paraphrase_context.py` | S2 문맥 paraphrase (vLLM) + NLI·어휘 guard (`--degree_guard`) → `_S2.csv`, `_all.csv`, `_paraphrase_log.csv` | llm |
| `6_shortcut_floor.py` | surface-only 로지스틱 회귀 AUROC (조건별) | clinsev |
| `7_score_metrics.py` | metric 채점 (`--metrics lexical,bertscore,f1chexbert,srrbert,radgraph,ratescore,temporal,radcliq,green`), 그룹별 CSV, 재개 가능 | clinsev |
| `8_analyze_factorial.py` | paired accuracy / AUROC / gap / z 분해, cluster bootstrap → `analysis/REPORT.md`, CSV | clinsev |
| `9_llm_judge.py` | judge (`--prompt rubric|errors|rubric_unit`, `--no_think`, `--reasoning low`), 추론 채널 분리 파싱 | llm |
| `10_crimson.py` | CRIMSON (radeval prompt·채점 + vLLM 배치) | llm |
| `11_judge_cells.py` | judge 칸별·타입별 CHANGED 비율 → `JUDGES.md` | clinsev |
| `12_make_annotation_package.py`, `19_make_supplementary_annotation.py` | PART1(504) / PART2(204) blinded 시트 + KEY | llm |
| `13_x3_audit_existing_benchmarks.py` | v1·우리 세트 surface probe → `results/3_x3_audit/TABLE3.md` | clinsev |
| `14_extended_analysis.py` | 하위타입, dose-response, 대비 검정, 혼합효과, CRIMSON 귀속, robustness → `extended/` | llm (statsmodels) |
| `14_subtype_mechanism_robustness.py` | 같은 내용의 초기판 (`analysis/FOLLOWUP.md`) | clinsev |
| `15_generate_omission_insertion.py` | 누락·삽입 층 (MIMIC) | llm |
| `16_generate_monotonicity.py`, `18_analyze_monotonicity.py` | 고정 surface monotonicity 세트·분석 → `MONO.md` | clinsev |
| `17_make_figures.py` | Fig 2 dumbbell, Fig 3 산점도, dose-response | clinsev |
| `20_make_paper_tables.py` | `docs/paper/tables/*.tex` + `numbers.tex` 매크로 (본문 수치 공급, 표식 일관성 검사) | clinsev |
| `21_review_reanalysis.py` | win/tie/loss, strict-matched subset, 환율, 정도표현 보존 subset, 논쟁 패턴 제외, Ctrl-1·interaction → `review1007/` | clinsev |
| `22_probe_public_suites.py` | RaTE-Eval Task 3 원문 복원 + probe, Task 1·2 표면 통계 τ | clinsev |
| `23_external_validity.py` | `--build`(rate1/rate2 쌍 파일) / `--analyze`(전문의 τ, scorer 간 ρ) | clinsev |
| `24_review_followup.py` | 대체 paraphraser(A), rubric_unit(B), RaTE-Eval 합성 과제 metric(C) → `results/REVIEW1007_FOLLOWUP.md` | clinsev |
| `25_merge_iualt.py` | iualt 세트: S2 행만 새로 채점하고 나머지는 IU 점수 복사 | clinsev |
| `run_full.sh` → `run_full_mopup.sh` → `run_full_until_complete.sh` | IU+MIMIC full 큐 (10/1–10/2) | |
| `run_gptoss_rerun.sh`, `run_judges_extra.sh`, `run_oi.sh`, `run_finalize_1003.sh`, `run_reanalyze_when_ready.sh` | 10/3 재실행·확장 | |
| `run_set.sh <tag>` | 세트별 범용 큐 (`NO_LLM=1`, `NO_JUDGES=1`, `ONE_JUDGE=1`, `SKIP_GREEN=1`) | |
| `run_review_1007.sh`, `run_review_1007b.sh`, `run_review_sets.sh`, `run_review_sets2.sh`, `run_review_final.sh`, `_swap_queue.sh`, `_gemma_try.sh` | 10/7 리뷰 대응 큐 (LLM 작업은 단일 순차 큐로 통합) | |
| `run_scores_pilot*.sh`, `run_judges_pilot_iu.sh`, `run_judges_queue{2,3}.sh`, `run_queue4.sh` | 10/1 pilot | |
| `env_llm.sh`, `gpu_wait.sh` | vLLM 환경변수(`KV_GB`, 스레드 상한), GPU 여유 메모리 대기 + 파일 lock | |

OLD 디렉토리(`/home/irteam/junah-data-1/2_ClinSevBench/ClinSevBench_v2`)는 `0`, `1`, `2`, `13`번이 읽기 전용으로 참조한다 (`reports_mimic_txt_dir.csv`, `openi_iu_xray_reports.csv`, v1 subset200 점수, 480쌍 human 라벨).
