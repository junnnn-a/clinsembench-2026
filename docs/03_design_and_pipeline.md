# 03. 설계와 파이프라인 (실제로 실행한 설정)

## 1. 설계

### 1.1 칸과 비교

한 report 섹션의 target 문장 s(타입별 trigger 보유)에서 6칸 + identity:

| | S0 최소 | S1 문장 재배열 (토큰 bag 유지) | S2 나머지 문장 paraphrase (토큰 bag 변경) |
|---|---|---|---|
| **P** 의미 보존 | P0: s에 benign 치환 | P1: P0 + 재배열 | P2: P0 + 문맥 paraphrase |
| **C** 의미 변경 | C0: s의 같은 슬롯에 flip | C1: P1과 동일 문맥 + flip | C2: P2와 동일 문맥 + flip |

같은 열의 P와 C는 target 슬롯 하나만 다르다(같은 surface 연산, 같은 토큰 수 변화).

| 조건 (논문 표기) | 비교 | 의미 |
|---|---|---|
| **Ctrl-0** | C0 vs P0 | 국소 edit의 의미 민감도 (통제) |
| Ctrl-1 | C1 vs P1 | 재배열 잡음 속 (통제) |
| **Ctrl-2** | C2 vs P2 | paraphrase 잡음 속 (통제, judge용 hard tier) |
| **Conf-R** | C0 vs P1 | v1형 혼동 재현 (benign = 재배열·서식) |
| **Conf-P** | C0 vs P2 | ReEvalMed형 혼동 재현 (benign = 자유 재작성) |
| surface 효과 | P1 vs P0, P2 vs P0 | 의미 같을 때 surface만의 penalty |

### 1.2 Edit 규칙 (7타입; 원본 `scripts/3_generate_factorial_pairs.py`, 부록 A)

| 타입 | trigger | P (보존) | C (변경) | 하위타입 |
|---|---|---|---|---|
| laterality | left/right + 병변 명사·lobe (bilateral·기구 문장 제외) | `left` → `left-sided`, `LLL`, `on the left` | 같은 변환 + 반대쪽 (`right-sided`, `RLL`) | – |
| anatomy | side+lobe, lung bases, bibasilar, perihilar … | 약어·동의 표현 (`bases of the lungs`, `basal`, `parahilar`) | upper↔lower, apex, apical, peripheral | region |
| measurement | `숫자 cm/mm` 1회 | 단위 변환 (`4.7 cm → 47 mm`) | 값 2배/½ (`→ 94 mm`) / 10배 단위 오류 (`→ 47 cm`, **D-1**) | value / unit |
| negation | 7 문장 템플릿 (`No X is seen`, `There is no X`, `without X`, `no evidence of X`, `X is seen` …) | 동형 재서술 (`No X seen.`, `X is absent.`, `X is not seen`) | 긍/부정 반전 (`X is seen.`, `X is present.`) | negated→present / present→negated |
| severity | trace/minimal/mild/small/moderate/large/severe/marked + finding | 동급 동의어 (`slight`, `small-sized`, `marked↔severe`) | 인접 등급 (`mild→moderate`) / 양극단 (`mild→severe`) | adjacent / extreme |
| temporal | stable, unchanged, improved, worsened, increased … (기구 문장 제외) | 동의어 (`stable↔unchanged`, `better`, `progressed`) | 방향 반전 (`unchanged→increased`, `improved→worsened`) | – |
| uncertainty | may/could represent, likely, possible, cannot be excluded, consistent with, suggestive of … | 동급 hedge 동의어 (`might`, `probably`, `compatible↔consistent`) | hedged→definite (`clearly represents`, `definite`) / definite→hedged | 방향 2종 |

- Shape matching: (a) C = P의 benign 변환 + flip, (b) 둘 다 1토큰 치환, (c) 비대칭 불가피(negation·uncertainty 일부)하면 반대 방향 변형을 함께 두고 샘플링에서 균형(`shape_sign`).
- 샘플링(`4_sample_targets.py`): 타입당 150(IU는 공급 한계로 94–150), 패턴 상한 15%, report당 상한, 비부정 문장 우선, hashlib seed. 섹션은 3문장 이상(S1·S2 생성 조건).
- 경계선 P 패턴은 `needs_expert_review` 플래그(anatomy 33%, severity 66–69%, uncertainty 24–31%) → 보수적 subset.

### 1.3 S2 paraphrase (`5_paraphrase_context.py`)
- 생성: Qwen2.5-7B-Instruct, temperature 0.8, 문장당 4후보. 검증: cross-encoder/nli-deberta-v3-large 양방향 entailment ≥0.8 + 어휘 guard(숫자·좌우·단위·부정 불변) + edit ≥2토큰. 통과 후보 중 가장 많이 바뀐 것 채택. 실패 시 원문 유지(`kept_original`). 비식별 토큰 문장은 그대로.
- 채택률: IU 91.9%, MIMIC 92.2%. target당 문맥 ≈3–4문장 중 ≈3개가 paraphrase.
- 대체 paraphraser(10/7): Llama-3.1-8B-Instruct + `--degree_guard`(정도표현 보존), IU 301 target, 채택 86.3%.

### 1.4 Shortcut floor (`6_shortcut_floor.py`)
(reference, candidate)만 보는 feature 10개(Jaccard drop, token-F1 drop, difflib ratio, char ratio, #edit tokens, edit 비율, 길이 비율, |길이 차|, bag 변화, 숫자 변화) → 로지스틱 회귀, report 단위 5-fold GroupKFold AUROC. 라벨이 surface로 예측되는 정도. 같은 분류기를 v1 subset200·v1 human 480쌍·RaTE-Eval 합성 과제에 적용(`13_x3_audit_existing_benchmarks.py`, `22_probe_public_suites.py`).

### 1.5 Scorer

| 그룹 | 항목 | 구현 |
|---|---|---|
| meaning-blind baseline | Jaccard, token F1 | 자체 구현 (v1 복사) |
| lexical | BLEU, ROUGE-L | 자체 구현 |
| embedding | BERTScore DistilBERT-L5 rescaled (= v1 설정), RoBERTa-large L17 rescaled, DeBERTa-xlarge-MNLI | RadEval / bert_score 0.3.13 |
| clinical non-LLM | F1CheXbert, Temporal F1 (Libra), SRR-BERT, RadGraph F1, RaTEScore, RadCliQ-v1 | RadEval 2.2.1 per-sample |
| LLM metric | GREEN (RadLlama2-7B), CRIMSON (MedGemma-4B-it-crimson; radeval prompt·채점 + vLLM 배치 생성, greedy, rep. penalty 1.1) | `7_score_metrics.py`, `10_crimson.py` |
| LLM judge | Llama-3.1-8B-Instruct, Gemma-3-27B-it, Qwen3-32B (no-think / thinking), gpt-oss-20b, gpt-oss-120b. temperature 0, vLLM 0.30 | `9_llm_judge.py` |

Prompt: `rubric`(같은 임상 소견을 말하는가 → JSON {label, confidence}; 점수 = PRESERVED 확신도), `errors`(임상적 불일치 나열 + `ERROR_COUNT: n`; 점수 = 1/(1+n)), `rubric_unit`(rubric + 단위 변환·약어는 benign 명시). 추론 모델은 최종 채널만 파싱(미파싱 ≤0.5% → 결측). identity도 모델 통과.

Penalty: Δ = s(identity) − s(cell), 전 scorer "높을수록 reference에 가까움"으로 정렬(RadCliQ는 반전).

### 1.6 통계 (`8_analyze_factorial.py`)
- 주 지표 **paired accuracy** = 같은 target에서 1[Δ(C) > Δ(P)] (+0.5 동점). chance 0.5. 보조 AUROC, gap, z-scored 의미·surface 효과(혼합효과/cluster-robust OLS).
- CI: **report-cluster bootstrap 1,000회**. metric 간·조건 간 차이는 paired bootstrap. 기준선(Jaccard) 대비 유의성 → Table 2 기호(↓ 아래, ∘ 구별 안 됨, 무표시 위).
- 10/7 추가: win/tie/loss, strict-matched subset(P0·C0의 Jaccard·token F1이 정확히 같은 target: IU 443, MIMIC 486 → 기준선 0.50), 환율 = (Δ(P2) − Δ(P0)) / (Δ(C0) − Δ(P0)).

### 1.7 확장 세트
- **Fixed-surface monotonicity** (`16_generate_monotonicity.py`, MIMIC 300): 한 섹션에서 서로 다른 타입 matched edit 3개(다른 문장). M0=p1p2p3, M1=c1p2p3, M2=c1c2p3, M3=c1c2c3 — surface 동일, 의미 변경 수만 0→3. 대조 K1=c1만, K2=c1c2만(기존 사다리). 지표: 단계 정확도, strict/weak monotone 비율, within-target Kendall τ, "benign 3 > error 1" 비율.
- **Omission/insertion** (`15_generate_omission_insertion.py`, MIMIC 300): C 소견 문장 삭제 / 타 report 소견 문장 추가, P 비임상 문장 삭제 / 기존 문장 재서술 추가. floor 0.89 → 통제 실패, 부록.
- **외부 타당성** (`23_external_validity.py`): RaTE-Eval Task 1(문장 441쌍, 전문의 오류 수)·Task 2(문단 370쌍, 0–5점)에 scorer 채점 → scorer별 Kendall τ → 우리 열(Ctrl/Conf/mono τ)과의 scorer 간 Spearman ρ(permutation p).

## 2. 스크립트 (번호 = 대체로 실행 순서)

| 파일 | 역할 | env |
|---|---|---|
| `0_audit_prior_experiment.py`, `1_audit_trivial_baseline_human_labels.py` | v1 감사 (OLD 읽기 전용) | clinsev |
| `2_prepare_corpora.py` | 섹션 재파싱, 문장 분리, deid 플래그 → `data/corpus/{iu,mimic}_sections.csv` | clinsev |
| `3_generate_factorial_pairs.py` | 7타입 P/C 후보 전수 생성 → `data/pairs/{iu,mimic}_factorial_S0S1.csv` | clinsev (MIMIC은 multiprocessing) |
| `4_sample_targets.py` | 샘플링 → `{tag}_{corpus}_targets.csv`, `_S0S1.csv` | clinsev |
| `5_paraphrase_context.py` | S2 → `{tag}_{corpus}_S2.csv`, `_all.csv`, `_paraphrase_log.csv` | **llm** |
| `6_shortcut_floor.py` | surface-only 분류기 | clinsev |
| `7_score_metrics.py` | metric 채점, 그룹별 CSV(재개 가능) | clinsev |
| `9_llm_judge.py`, `10_crimson.py` | judge / CRIMSON | **llm** |
| `8_analyze_factorial.py`, `11_judge_cells.py` | 주 분석 → `analysis/` | clinsev |
| `12_make_annotation_package.py`, `19_make_supplementary_annotation.py` | PART1 / PART2 시트 | llm |
| `13_x3_audit_existing_benchmarks.py`, `22_probe_public_suites.py` | 기존 benchmark probe (v1, RaTE-Eval) | clinsev |
| `14_extended_analysis.py`, `14_subtype_mechanism_robustness.py` | 하위타입·dose-response·대비·혼합효과·CRIMSON 귀속·robustness | llm (statsmodels) |
| `15_generate_omission_insertion.py`, `16_generate_monotonicity.py`, `18_analyze_monotonicity.py` | 확장 세트 | llm / clinsev |
| `21_review_reanalysis.py`, `23_external_validity.py`, `24_review_followup.py`, `25_merge_iualt.py` | 10/7 리뷰 대응 | clinsev |
| `17_make_figures.py`, `20_make_paper_tables.py` | 그림, 표 + `numbers.tex` | clinsev |
| `run_full.sh` | IU+MIMIC full 전체 큐 (paraphrase → floor → metric 병렬 → CRIMSON → judge) | |
| `run_set.sh <tag>` | 세트별 범용 큐 (`NO_LLM`, `NO_JUDGES`, `ONE_JUDGE`, `SKIP_GREEN`) | |
| `run_review_1007*.sh`, `run_review_final.sh`, `run_review_sets*.sh` | 10/7 추가 실험 큐 (LLM 작업은 단일 순차 큐) | |
| `env_llm.sh`, `gpu_wait.sh` | vLLM 환경변수, GPU 여유 메모리 대기 + 파일 lock | |

## 3. 재현 순서 (IU full)

```bash
ROOT=/home/irteam/junah-data-1/ARR_10/2_ClimSemBench; cd $ROOT
CPY=/opt/conda/envs/clinsev/bin/python
$CPY scripts/2_prepare_corpora.py
$CPY scripts/3_generate_factorial_pairs.py --corpus iu
$CPY scripts/4_sample_targets.py --corpus iu --tag full --n_per_type 150 --pattern_cap 0.15
source scripts/env_llm.sh; $PY scripts/5_paraphrase_context.py --corpus iu --tag full --gpu_mem 0.15
$CPY scripts/6_shortcut_floor.py --pairs_csv data/pairs/full_iu_all.csv --out_csv results/2_full_iu/shortcut_floor_all.csv
$CPY scripts/7_score_metrics.py --pairs data/pairs/full_iu_all.csv --out results/2_full_iu/scores --metrics lexical,bertscore,f1chexbert,srrbert,radgraph,ratescore,temporal,radcliq,green --batch_size 16
$PY scripts/10_crimson.py --pairs data/pairs/full_iu_all.csv --out results/2_full_iu/scores --gpu_mem 0.12
for m in "openai/gpt-oss-20b gptoss_20b --reasoning low" "meta-llama/Llama-3.1-8B-Instruct llama31_8b" "google/gemma-3-27b-it gemma3_27b" "Qwen/Qwen3-32B qwen3_32b --no_think"; do set -- $m; $PY scripts/9_llm_judge.py --pairs data/pairs/full_iu_all.csv --out results/2_full_iu/judges --model $1 --tag $2 --prompt rubric "${@:3}"; done
$CPY scripts/8_analyze_factorial.py --pairs data/pairs/full_iu_all.csv --scores results/2_full_iu/scores results/2_full_iu/judges --out results/2_full_iu/analysis
$CPY scripts/11_judge_cells.py --pairs data/pairs/full_iu_all.csv --judges results/2_full_iu/judges --out results/2_full_iu/analysis
$PY scripts/14_extended_analysis.py --corpus iu mimic
$CPY scripts/21_review_reanalysis.py; $CPY scripts/22_probe_public_suites.py; $CPY scripts/23_external_validity.py --analyze; $CPY scripts/24_review_followup.py
$CPY scripts/20_make_paper_tables.py; $CPY scripts/17_make_figures.py
cd docs/paper && /home/irteam/junah-data-1/ARR_10/1_CAP/paper/tectonic -X compile main.tex
```
실제로는 `scripts/run_full.sh` → `run_full_mopup.sh` → `run_full_until_complete.sh`(10/2 완료) → `run_gptoss_rerun.sh`(10/3) → `run_judges_extra.sh`, `run_oi.sh`, `run_set.sh mimicmono`(10/3) → `run_review_1007*.sh`, `run_review_sets*.sh`, `run_review_final.sh`(10/7)로 실행했다. 인자는 각 셸에 있다.

## 4. 환경과 서버 특이사항

| 항목 | 내용 |
|---|---|
| metric env | `/opt/conda/envs/clinsev`: Python 3.11, torch 2.2.2+cu121, transformers 4.40.0, radeval 2.2.1, bert-score 0.3.13, green_score 0.0.12(editable, OLD 디렉토리), sacrebleu 2.6, rouge_score 0.1.2, scikit-learn 1.8, pandas 3.0 |
| LLM env | `envs/llm`: Python 3.12, vLLM 0.30.0, torch 2.13+cu130, transformers 5.18, openai 3.22 / anthropic 1.10 (API judge용, 미사용) |
| LLM env 필수 설정 (`env_llm.sh`) | `LD_LIBRARY_PATH=envs/llm/lib`(시스템 libstdc++ 구버전), `CC=envs/llm/bin/gcc`(시스템 gcc 없음), `VLLM_USE_FLASHINFER_SAMPLER=0`(nvcc 없음), `KV_GB=16`(GPU 공유 중 프로파일링 실패 우회), `OMP_NUM_THREADS=8` |
| HF cache | `/home/irteam/hf_cache` (`HF_HOME`, offline) |
| GPU | H200 143GB 1장, **CAP 프로젝트와 공유** → vLLM 초기화 실패·OOM 다수. `gpu_wait.sh`(여유 메모리 대기 + lock) 사용. 두 vLLM 엔진을 동시에 띄우면 먼저 뜬 것이 warm-up 뒤 멈춤 → LLM 작업은 단일 순차 큐 |
| CPU | 컨테이너 **quota 8코어** (`nproc`은 128). 채점 프로세스가 스레드 190개씩 띄워 throttle → `OMP_NUM_THREADS=8`, 병렬 축소 |
| 세션 제한 | 백그라운드 작업 1시간 제한 → `nohup bash scripts/run_*.sh`, 로그의 `ALL_DONE`/`EXIT=`로 확인 |
| 속도 참고 | CRIMSON(HF 순차) 40쌍 30분 → vLLM 배치로 교체. gpt-oss-20b rubric 6,230행 ≈ 수십 분. Gemma-3-27B는 eager 모드에서 warm-up 후 멈춤 4회 → `VLLM_EAGER=0` |

## 5. 실행 중 발견·수정한 버그

| 버그 | 영향 | 조치 |
|---|---|---|
| gpt-oss 출력에 harmony 추론 채널 포함, 파서가 전체에서 JSON·키워드 검색 (`unchanged`에 매칭), errors prompt 11%가 `ERROR_COUNT` 없이 0 처리 | rubric 0.3–0.9% 행, errors 신뢰 불가 | `assistantfinal` 이후만 파싱, max_tokens 4096, 재실행 (`judges_superseded/`). 재실행 수치 차이 ≤0.01 |
| 생성기 v1(규칙 그대로 + P 추가) 통제 S0 floor 0.657 | P/C 모양 불일치 | shape matching (v2→v4) |
| measurement unit 변형 토큰 수 불일치 (D-1) | IU 49 / MIMIC 75 | 제외 병기 (세트 동결) |
| `gpu_wait`에 lock 없어 우리 큐끼리 동시에 통과 → 서로 OOM | 10/3 | 파일 lock + hold |
| 확장 분석의 변수명 `C`가 patsy `C()`를 가림; 혼합효과 singular 15/19 | – | 변수명 변경, cluster-robust OLS 대체 |
| 초안 서술 오류: uncertainty "82–93% 탐지"(실은 paired acc), interaction "±0.03", "measurement는 device 서술을 피한다" | 본문 | 10/7 정정 |
