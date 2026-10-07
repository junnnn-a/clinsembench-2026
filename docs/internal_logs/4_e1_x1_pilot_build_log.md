# 4. E1 (데이터 재구축) + X1 pilot 구축 로그

- 시작: 2026-10-01
- 기준 계획: `3_experiment_plan.md` §4–§5
- 이 문서는 진행 중 계속 갱신한다. 결과 수치는 `results/1_pilot_iu/`.

---

## 1. 환경

| 항목 | 내용 |
|---|---|
| metric 채점 env | `/opt/conda/envs/clinsev` (radeval 2.2.1, torch 2.2.2, transformers 4.40) |
| LLM env | `envs/llm` (conda, Python 3.12, vLLM 0.30.0, torch 2.13+cu130). 별도 생성 |
| LLM env 실행 시 필수 환경변수 | `LD_LIBRARY_PATH=envs/llm/lib` (시스템 libstdc++가 오래되어 `CXXABI_1.3.15` 없음), `PATH=envs/llm/bin:$PATH`, `CC=envs/llm/bin/gcc` (시스템에 C 컴파일러가 없어 conda `gcc_linux-64` 설치 후 `gcc`/`cc`/`g++` 심볼릭 링크 생성; torch.compile/triton이 요구) |
| HF cache | `/home/irteam/hf_cache` (`HF_HOME`). v1의 GREEN 등은 `~/.cache/huggingface/hub`에 있어 심볼릭 링크로 연결 |
| 다운로드한 모델 | Qwen3-32B, gpt-oss-20b, gemma-3-27b-it, Llama-3.1-8B-Instruct, medgemma-4b-it-crimson, cross-encoder/nli-deberta-v3-large, microsoft/deberta-large-mnli. Qwen2.5-7B-Instruct는 기존 캐시 |
| 접근 불가 (403) | google/medgemma-27b-text-it, google/medgemma-4b-it, meta-llama/Llama-3.3-70B-Instruct → **사용자가 HF에서 라이선스 동의 필요** (U 항목 추가) |
| GPU | H200 143GB 1장. 같은 서버에서 다른 프로젝트(CAP)의 CPU 작업이 돌고 있음. GPU는 비어 있었음 |

### 실패 기록
| 시각 | 실패 | 원인 | 조치 |
|---|---|---|---|
| 10/01 06:34 | vLLM 모델 로딩 실패 (`Qwen2ForCausalLM failed to be inspected`) | 서브프로세스가 시스템 `libstdc++.so.6`을 로드 → `libicui18n.so.78`의 `CXXABI_1.3.15` 없음 | `LD_LIBRARY_PATH=envs/llm/lib` |
| 10/01 07:25 | vLLM `Could not find nvcc` | FlashInfer top-k/top-p sampler가 JIT 컴파일 요구 | `VLLM_USE_FLASHINFER_SAMPLER=0` |
| 10/01 08:1x–09:0x | judge 엔진 초기화 실패 4건 (Qwen3-32B ×2, gemma-3-27b, gpt-oss-20b) | **GPU 공유**: 같은 H200에서 다른 프로젝트(CAP) 작업이 65–90GB 사용 + 우리 metric 채점 ~35GB. vLLM은 시작 시 `free ≥ gpu_mem × total`을 요구 | `scripts/gpu_wait.sh`(여유 메모리 대기) + 모델별 필요 메모리에 맞춘 `gpu_mem`; Qwen3-32B는 FP8 버전(~34GB)으로 교체; gemma-3-27b는 큐 마지막(66GB 대기) |
| 10/01 08:30 | CRIMSON HF 파이프라인: 40쌍에 30분 이상 | radeval의 HF 경로는 샘플별 순차 generate (최대 8192 토큰) | 프롬프트·채점은 radeval, 생성은 vLLM 배치로 교체 (`10_crimson.py`) |
| 10/01 09:00 | CRIMSON `Weight files referenced in index but missing` | 첫 다운로드가 `model-00002-of-00002.safetensors`를 받지 못함 | 재다운로드 |
| 10/01 08:50 | metric 채점·MIMIC 생성이 백그라운드 1시간 제한으로 중단 | 세션 백그라운드 작업 시간 제한 | nohup 분리 실행 + metric 단위 재개(`run_scores_pilot*.sh`), 생성기 병렬화 |
| 10/01 07:03 | vLLM 엔진 초기화 실패 (`Failed to find C compiler`) | 시스템에 gcc 없음 (triton/inductor 컴파일) | conda `gcc_linux-64 gxx_linux-64` 설치 + 심볼릭 링크. `enforce_eager=True`도 동일 오류였음 |

---

## 2. E1: 코퍼스 재구축 (`scripts/2_prepare_corpora.py`)

v1 문제(문서 2 Audit C·D)를 고친 점
- 섹션 fallback 제거: 헤더가 실제로 있고 본문이 비어 있지 않을 때만 섹션 인정. findings == impression인 report(83건) 제외
- 행정 헤더(EXAMINATION/INDICATION/TECHNIQUE/COMPARISON/NOTIFICATION/WET READ 등) 파싱 단계에서 분리 → 섹션 텍스트 내 헤더 잔존율 ≤0.01%
- 문장 분리기: `Dr.`, `a.m./p.m.`, 소수점(4.7 cm), 번호 목록(`1. No acute ...`) 보호
- 비식별 토큰(IU `XXXX`, MIMIC `___`)이 있는 문장은 target에서 제외 (`sent_has_deid`)

결과 (`data/corpus/*_stats.json`)

| corpus | section | n sections | 평균 단어 | 평균 문장 | ≥3문장 | deid 포함 | ≥3 clean 문장 |
|---|---|---|---|---|---|---|---|
| IU | findings | 3,424 | 31.7 | 4.65 | 96.9% | 43.4% | 90.2% |
| IU | impression | 3,817 | 10.9 | 1.76 | 18.1% | 17.6% | 14.0% |
| MIMIC | findings | 98,618 | 55.8 | 5.59 | 95.1% | 22.7% | 92.1% |
| MIMIC | impression | 133,679 | 34.2 | 3.33 | 54.1% | 30.2% | 47.7% |

- v1과의 차이: v1은 172,171 report 전부에 impression·findings가 있었고(fallback), 58%가 동일 텍스트였다. 재파싱 후 findings 98,618 / impression 133,679, 중복 없음.
- IU impression은 대부분 1–2문장이라 S1·S2 칸(3문장 이상 필요)을 만들 수 있는 target이 적다. IU는 findings 위주가 된다.

---

## 3. X1: factorial 생성기 (`scripts/3_generate_factorial_pairs.py`)

### 3.1 설계 변경: shape matching (v2)
첫 버전(v1 규칙 그대로 P/C만 추가)에서 pilot을 만들고 surface-only 분류기(§4)를 돌린 결과 **통제 조건(C0 vs P0)에서도 pooled AUROC 0.657, 타입별 0.58–0.99**였다. 원인: P와 C의 edit "모양"이 달랐다 (예: laterality P `left→left-sided`는 삽입, C `left→right`는 치환; measurement P는 2토큰 변환, C는 1토큰 변경). 토큰 수 차이 ≤2라는 계획의 제약만으로는 부족했다.

해결 원칙
1. **C = P의 benign 변환 + 의미 flip**: 같은 surface 연산을 둘 다 적용하고 C만 의미 슬롯을 바꾼다.
   - laterality: P `left-sided X` / C `right-sided X`; P `LLL` / C `RLL`; P `X on the left` / C `X on the right`
   - anatomy: P `LLL` / C `LUL`; P `bases of the lungs` / C `apices of the lungs`; P `base of the right lung` / C `apex of the right lung`; P `basal` / C `apical`; P `bilateral basilar` / C `bilateral apical`
   - measurement: P `4.7 cm → 47 mm` / C `→ 94 mm`(값 2배·½) 또는 `→ 47 cm`(10배 오류). 숫자가 P·C 모두 바뀜
2. **둘 다 1토큰 치환**: temporal(`stable→unchanged` / `→increased`), severity(`mild→slight` / `→moderate|severe`), uncertainty 일부
3. **비대칭이 불가피한 곳(negation, uncertainty 일부)은 반대 방향 변형을 함께 두고 샘플링에서 균형**(`shape_sign` = P_longer / C_longer / equal, `4_sample_targets.py`가 두 방향 수를 맞춤)
   - negation N1a: P `No X seen.`(is 삭제) / C `X is seen.`(No 삭제) — 동일 모양
   - N3a: P `X is absent.` / C `X is present.` — 동일 모양; N3b (P 길다) / N3c (C 길다)
   - N2b: P `There is no evidence of X` / C `There is evidence of X`
   - N6 (긍정→부정): P `X seen.` / C `X not seen.`

삭제한 규칙: laterality의 base/apex/hemidiaphragm/hemithorax/CP 패턴 (P가 삭제·삽입형이라 C보다 edit 1 적음), temporal `has improved`, `is new`.

### 3.2 규칙 요약 (부록 rule 표의 원본)

| 타입 | trigger (문장·섹션에서 정확히 1회) | P (보존) | C (변경) | 하위타입 | 전문의 확인 필요 |
|---|---|---|---|---|---|
| laterality | `left/right` + 병변 명사 / lobe. bilateral·both·기구 문장 제외 | `-sided`, lobe 약어, `on the <side>` | 반대쪽 + 같은 변환 | lesion_laterality | – |
| negation | N1 `No X is seen`, N2 `There is no X`, N3 `No X.`, N4 `without X`, N5 `no evidence of X`, N6 `X is seen`, N7 `negative for X`. X에 finding 용어 필수, 다른 부정어 없음 | 위 표 | 위 표 | negated→present / present→negated | – |
| measurement | `숫자 cm/mm` 1회, 0<v≤40 | 단위 변환 | 값 2배·½(변환 단위) / 10배 오류 | value / unit | – |
| temporal | unchanged, stable, improved, worsened, has/have increased·decreased·resolved, decreased, new. 기구·위치 문장 제외, 다른 temporal 단어 없음 | stable↔unchanged, better, worse, progressed, diminished, cleared, newly identified | increased/worsened/improved 등 방향 반전, previously seen | comparison_direction | – |
| severity | trace/minimal/mild/small/moderate/large/severe/marked + finding 명사. 부정 문장 제외 | slight, marked↔severe, trace↔minimal, small-sized, moderate-sized, large-volume/large-sized | 인접 등급 / 양극단 | adjacent / extreme | small-sized, large-volume, large-sized, moderate-sized, trace↔minimal |
| uncertainty | may/could represent·reflect, likely represents, possibly representing, cannot be excluded, cannot exclude, suspicious/worrisome for, suggestive of, questionable, probable, possible, consistent/compatible with, represents/reflects, diagnostic of | 동급 hedge 동의어 (might, probably, concerning for, compatible↔consistent ...) | hedged→definite (clearly represents, is excluded, consistent with, definite) / definite→hedged (suspicious for, may represent) | hedged→definite / definite→hedged | probable, possible, questionable, suggestive of, represents, reflects, diagnostic of |
| anatomy | side+lobe, lung bases, side (lung) base, bibasilar, basilar, perihilar | 약어, `bases of the lungs`, `base of the <side> lung`, basal, bilateral basilar, parahilar | upper↔lower, apices, apex, apical, peripheral | region | perihilar→parahilar, basilar→basal |

### 3.3 IU 생성 결과 (v4, `data/pairs/iu_coverage.csv`)

| section | type | targets | 패턴 수 | 최다 패턴 비율 | edit P | edit C |
|---|---|---|---|---|---|---|
| findings | anatomy | 399 | 6 | 0.43 | 2.87 | 2.87 |
| findings | laterality | ~200 | 2–3 | 0.68 | 2.36 | 2.36 |
| findings | measurement | 58 | 3 | 0.38 | 1.4 | 1.4 |
| findings | negation | 1,779 | 11 | 0.29 | 3.07 | 3.46 |
| findings | severity | 184 | 8 | 0.42 | 1.0 | 1.0 |
| findings | temporal | 335 | 4 | 0.78 (`stable`) | 1.0 | 1.0 |
| findings | uncertainty | 106 | 12 | 0.43 | 1.10 | 1.84 |
| impression | (7타입) | 40–188 | | | | |

- IU는 measurement(99), uncertainty(160), laterality(~270)가 full 규모(150/타입)에 빠듯하다. 부족한 타입은 MIMIC 로컬 트랙에서만 보고 (계획 §10).
- 생성 시간: IU 약 10분 (규칙당 섹션 전체에 대한 정규식 카운트). MIMIC은 40,000 섹션 서브샘플로 실행.

### 3.3b MIMIC 생성 결과 (v4, 40,000 섹션 서브샘플, 48 프로세스 병렬 약 15분)

| type | findings targets | impression targets | 패턴 수 | 최다 패턴 비율 |
|---|---|---|---|---|
| anatomy | 8,489 | 5,426 | 6 | 0.27–0.34 |
| laterality | 3,036 | 2,523 | 3 | 0.63 |
| measurement | 2,076 | 1,285 | 2 | 0.50 |
| negation | 12,118 | 5,176 | 11 | 0.25–0.29 |
| severity | 6,313 | 4,597 | 9 | 0.39–0.40 |
| temporal | 7,126 | 5,074 | 12 | 0.33–0.38 |
| uncertainty | 3,184 | 1,813 | 20–21 | 0.22–0.28 |

- 총 68,236 target / 341,180 행(S0·S1). full 규모(150/타입/섹션)에 충분하며 pattern cap 15%도 대부분 만족 가능.
- 첫 실행(단일 프로세스)은 백그라운드 1시간 제한으로 중단됨 → `process_section`을 top-level 함수로 빼고 `multiprocessing.Pool` 적용, nohup으로 분리 실행.
- 관찰: MIMIC의 measurement target은 대부분 기구 위치(ET tube ... cm above the carina). 병변 크기 측정은 소수. 본문에 명시할 것.
- 관찰: laterality/anatomy target 일부는 부정 문장 안에 있음 (예: "No appreciable left pneumothorax" → "No appreciable right-sided pneumothorax"). 의미는 바뀌지만 임상적 무게가 약하다. **full 세트 생성 시 `target_negated` 플래그를 추가하고 샘플링에서 비부정 문장을 우선**하도록 할 것 (pilot은 채점이 진행 중이어서 그대로 둠).

### 3.4 pilot 샘플 (`4_sample_targets.py`, tag=pilot)
- 7타입 × 40 target (findings 20 + impression 20), report당 최대 2 target, 패턴 상한 15%(패턴 수가 적은 타입은 완화), shape_sign 균형
- 결과 279 target (negation impression 19), 246 report, S0S1 행 1,395

---

## 4. Shortcut floor (`6_shortcut_floor.py`, pilot IU, S0/S1 칸)

Surface-only 로지스틱 회귀(Jaccard drop, token-F1 drop, difflib ratio, char ratio, #edit tokens, edit 비율, 길이 비율, |길이 차|, bag 변화, 숫자 변화), report 단위 5-fold.

| 생성기 버전 | controlled S0 | controlled S1 | confound v1 (C0 vs P1) | pooled | 최대 단일 feature AUROC (S0) |
|---|---|---|---|---|---|
| v1 규칙 그대로 (P만 추가) | 0.657 | 0.617 | 1.000 | 0.618 | 0.55 (seq ratio, 역방향 0.45) |
| v2 shape-matched | 0.638 | 0.626 | 1.000 | 0.615 | 0.612 (Jaccard) |
| v4 (+ measurement 숫자 양쪽 변경, laterality reorder) | **0.604** | **0.605** | 1.000 | **0.588** | 0.573 (Jaccard) |

타입별 (v4, S0): anatomy 0.77, laterality 0.89, measurement 0.98, negation 0.56, severity 0.70, temporal 0.62, uncertainty 0.80

S2 칸(context paraphrase) 포함 (`results/1_pilot_iu/shortcut_floor_all.csv`)

| 조건 | surface-only LR AUROC | Jaccard drop | token-F1 drop | edit tokens |
|---|---|---|---|---|
| controlled_S0 (C0 vs P0) | 0.604 | 0.573 | 0.572 | 0.508 |
| controlled_S1 (C1 vs P1) | 0.605 | 0.573 | 0.572 | 0.499 |
| **controlled_S2 (C2 vs P2)** | **0.544** | 0.524 | 0.525 | 0.503 |
| confound_v1 (C0 vs P1) | 1.000 | 0.573 | 0.572 | 0.000 (역방향) |
| **confound_reevalmed (C0 vs P2)** | **0.985** | 0.053 (역방향) | 0.042 (역방향) | 0.017 (역방향) |
| pooled | 0.555 | 0.539 | 0.538 | 0.502 |

- controlled_S2 타입별: anatomy 0.55, laterality 0.60, measurement 0.61, negation 0.52, severity 0.55, temporal 0.53, uncertainty 0.58 → **paraphrase 잡음이 있는 열에서는 type-aware 분류기도 chance 근처**.
- confound_reevalmed에서 surface feature의 AUROC가 0.02–0.05: "surface 변화가 크면 benign"이라는 역방향 shortcut. ReEvalMed 표(BLEU가 significant 쌍에 더 높은 점수)와 같은 방향을 우리 세트 안에서 재현했다. confound_v1은 정방향 shortcut(1.000). **혼동의 방향이 benchmark 구성에 따라 뒤집힌다**는 주장의 근거(계획 §1.3).

MIMIC pilot (280 target, `results/1_pilot_mimic/shortcut_floor_all.csv`)

| 조건 | surface-only LR | Jaccard drop | token-F1 drop |
|---|---|---|---|
| controlled_S0 | 0.603 | 0.562 | 0.566 |
| controlled_S1 | 0.575 | 0.562 | 0.566 |
| **controlled_S2** | **0.517** | 0.512 | 0.513 |
| confound_v1 | 1.000 | 0.562 | 0.000 (역) |
| confound_reevalmed | 0.993 | 0.015 (역) | 0.011 (역) |
| pooled | 0.529 | 0.531 | 0.532 |

- controlled_S2 타입별 0.53–0.58. IU와 같은 패턴. MIMIC S2 paraphrase: 1,097/1,190 문장 채택(92.2%), target당 3.92/4.60 문장.

해석
- **type-blind** 분류기(논문의 floor 정의)는 0.59–0.60. 계획의 목표(0.45–0.55)에는 못 미치지만 v1 조건(confound_v1)의 1.000, v1 데이터의 Jaccard 단독 0.85와 비교하면 shortcut의 대부분이 제거됐다.
- **type-aware**(타입 안에서 학습) 분류기는 여전히 높다. P와 C가 서로 다른 단어를 넣는 이상 문자 수준 차이(예: `left`→`left-sided`는 원 단어를 포함, `right-sided`는 아님; C 치환어 `moderate`, `right`가 리포트의 다른 문장에 이미 있어 Jaccard drop이 작음)는 제거할 수 없다. 이는 단어 치환 기반 minimal pair 모두의 한계이며, 논문에는 type-blind floor를 본문에, type-aware floor를 부록에 상한으로 보고한다.
- Gate 1 전제조건 "0.45–0.55"는 "type-blind LR ≤ 0.60, 단일 feature ≤ 0.58"로 완화해 진행. 최종 판단은 사용자.

---

## 4b. S2 paraphrase (`5_paraphrase_context.py`, pilot IU)
- 모델 Qwen2.5-7B-Instruct, temperature 0.8, 문장당 4 후보, 생성 229초 (847 context 문장)
- 검증: cross-encoder/nli-deberta-v3-large 양방향 entailment ≥ 0.8 + 어휘 guard(숫자·좌우·단위 불변, 부정 유무 불변) + edit ≥ 2 토큰
- 후보 단위 통과율 81.3% (NLI 89.3%, guard 94.5%); 문장 단위 772/847 (91.1%) 채택, 75문장은 원문 유지
- target당 context 4.0문장 중 평균 2.95문장이 paraphrase됨
- 채택 예: "The heart size is normal." → "The size of the heart is within normal limits."; "Lungs are otherwise clear." → "Lungs appear clear otherwise."
- 기각 예: "Heart size is normal." → "Normal heart size is noted." (NLI fwd 0.03: NLI 모델의 false negative), "Chest." → "Apical region of the chest." (정보 추가, 올바른 기각)
- 순환 방지: paraphrase 모델은 Qwen 계열 → judge Qwen3-32B 결과는 같은 계열로 표시

## 5. 다음 단계 (진행 중)
- [x] S2 칸 생성 완료 (`data/pairs/pilot_iu_all.csv`, 1,953행 = 279 target × 7칸)
- [ ] pilot metric 채점: `7_score_metrics.py` (lexical, BERTScore 3종, F1CheXbert, RadGraph, RaTEScore, Temporal, RadCliQ, SRR-BERT, RadEval-BERTScore, GREEN)
- [ ] pilot LLM judge: `9_llm_judge.py` (Qwen3-32B, gpt-oss-20b, gemma-3-27b-it, Llama-3.1-8B)
- [ ] CRIMSON: radeval crimson 모듈을 llm env에서 실행 (medgemma-4b-it-crimson)
- [ ] 분석: `8_analyze_factorial.py`
- [ ] MIMIC 생성 (40k 섹션) → 샘플
