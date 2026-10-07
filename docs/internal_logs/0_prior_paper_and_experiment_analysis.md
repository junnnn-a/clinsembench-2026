# 0. ARR May 제출본(ClinSemBench) — 논문·코드·데이터·결과 상세 분석

- 작성일: 2026-09-30
- 목적: ARR October 재제출을 위해, ARR May 제출본이 **실제로 무엇을 했는지**를 논문이 아닌 코드/데이터/결과 파일 기준으로 정리한다.
- 분석 대상 (모두 읽기 전용으로만 접근, 수정 없음)
  - 논문: `/home/irteam/junah-data-1/ARR_10/7910_ClinSemBench_Stress_Testi.pdf` (12쪽), `2_ClinSem.tex` — PDF와 tex 내용 일치 확인
  - 리뷰: `/home/irteam/junah-data-1/ARR_10/ClimSemBench_Review_ARR_5.md`
  - 실험: `/home/irteam/junah-data-1/2_ClinSevBench/ClinSevBench_v2` (이하 `OLD/`)
- 이번 실험 디렉토리: `/home/irteam/junah-data-1/ARR_10/2_ClimSemBench` (이하 `NEW/`)
- 관련 문서: 리뷰 분석은 `1_review_analysis.md`, audit 결과와 보완 계획은 `2_audit_findings_and_revision_plan.md`

> 표기: "논문"은 ARR May 제출본, "rebuttal"은 7/13 author response를 뜻한다.

---

## 1. 논문 요약

### 1.1 한 줄 요약
MIMIC-CXR 리포트 섹션에 규칙 기반 minimal edit을 가해 (reference, candidate) 쌍을 만들고, 각 RRG metric이 **meaning-changing edit에 meaning-preserving edit보다 큰 penalty를 주는가**를 AUROC 등으로 측정한 meta-evaluation benchmark.

### 1.2 핵심 정의
- Penalty: `Δ_m(i,t) = m(x_i, x_i) − m(x_i, x̃_{i,t})` (identity 점수 대비 하락폭)
- 모든 metric은 "클수록 reference와 일치" 방향으로 맞춘 뒤 Δ 계산
- 주 진단 지표: **meaning-change AUROC** (changed=1, preserved=0, score=Δ)
- 보조 지표: benign-over-changed inversion, edit-type blindness, penalty gap, rule-tier Spearman

### 1.3 논문이 주장한 3가지 기여
1. 480쌍/840 judgment로 검증한 minimal-pair benchmark (human-rule agreement 93.1%)
2. 폭넓은 metric audit — GREEN 최강, BERTScore는 방향이 뒤집힘(AUROC < 0.5)
3. Sensitivity card 제안 (AUROC + inversion + gap + blindness)

### 1.4 본문 주요 수치 (Table 3)

| Metric | Rule AUROC Impression | Rule AUROC Findings | Human-label AUROC (n=467) |
|---|---|---|---|
| GREEN | 0.903 [0.892, 0.914] | 0.896 [0.883, 0.908] | 0.814 [0.773, 0.858] |
| RaTEScore | 0.768 | 0.804 | 0.725 |
| RadGraph | 0.650 | 0.639 | 0.587 |
| Temporal | 0.613 | 0.609 | 0.584 |
| F1CheXbert | 0.572 | 0.581 | 0.570 |
| BERTScore | 0.221 | 0.165 | 0.274 |

- 모두 결과 파일과 일치함을 확인: `OLD/results/analysis/radeval_{impression,findings}_clean_subset200_broad/meaning_change_auroc.csv`, `OLD/results/analysis/annotation480_human_majority_auroc/human_and_rule_auroc.csv`

### 1.5 논문 구성
| 섹션 | 내용 | 비고 |
|---|---|---|
| 1 Intro | 동기, Fig.1 overview, 3 findings, 3 contributions | |
| 2 Related Work | 일반 metric / RRG metric / behavioral testing | **ReEvalMed, CRIMSON, GEMA-Score, RadFact 등 미인용** |
| 3 Benchmark Design | design goals, task def, data filtering, perturbation table, rule/QC, human validation | rule 설명이 코드와 다름 (§5 참조) |
| 4 Diagnostics | AUROC, inversion, blindness, gap, rule-tier | 정의가 코드와 다름 (§5 참조) |
| 5 Setup | metric suite, evaluation sets, implementation | BERTScore 모델 미기재 |
| 6 Results | human validation / AUROC / blindness(Fig.3) / qualitative | per-type은 5개 타입만 |
| 7 Discussion, 8 Conclusion | sensitivity card 권고 | |
| Appendix A–F | coverage, lightweight metrics, subset500 card, orientation audit, human details, repro | |

---

## 2. 실험 디렉토리 구조 (`OLD/`)

```
ClinSevBench_v2/
├── README.md, configs/strong.yaml, environment.yml, requirements.txt
├── scripts/            (52개, 핵심은 clinsev_pipeline.py 558줄)
├── scripts_rebuttal/   (11개, 7/9 작성된 초안. 실제 rebuttal은 scripts/ 쪽 수정본 사용)
├── data/
│   ├── processed/reports_mimic_txt_dir.csv     172,171 reports (report_id, path, text, findings, impression)
│   ├── minpairs/       section × N{2k,5k,20k} × seed{0,1,2} + clean + subset{5,20,200,500}
│   ├── annotation_meaning_480/                 blinded sheet, filled sheet, metadata
│   ├── external_reports/, external_minpairs/   OpenI/IU X-Ray (rebuttal)
│   ├── llm_eval/                               Llama rubric용 subset50 (rebuttal)
│   ├── stress/                                 composed stress (rebuttal, 미사용)
│   └── shards/                                 4-GPU 분할 실행용
├── results/
│   ├── fast/                   lexical metric 점수
│   ├── radeval/                RadEval metric 점수 (bertscore, f1chexbert, ratescore, temporal, radgraph, green)
│   ├── analysis/               70개 분석 폴더
│   ├── meaning_annotation_480_filled(+_overlap_details)/
│   ├── llm_rubric/             Llama-3-8B rubric 출력
│   ├── rebuttal_numbers/       rebuttal 표 원본
│   ├── metric_orientation/, paper_audits/, paper_examples/, examples/, repro/, summary/
├── figures/, tables/, logs/(113개)
├── GREEN/                      green_score 0.0.12 editable install
└── external/                   GEMA_score 코드 + gema_hf_cache (15GB, 다운로드만 하고 평가 결과 없음)
```

- 경로에 남아있는 `/home/modu37/...`는 이전 서버 경로이며 **현재 서버에는 존재하지 않는다**. 즉 MIMIC-CXR 원본 txt는 이 서버에 없고, 전처리된 `reports_mimic_txt_dir.csv`만 있다 (full text 컬럼이 있으므로 섹션 재파싱은 가능).
- `OLD/` 하위 몇몇 디렉토리의 mtime이 2026-09-30 07:42–07:56이지만, 그 시각 이후 수정된 **파일**은 없다 (디렉토리 entry만 변경됨).

### 2.1 환경
| 항목 | 값 |
|---|---|
| conda env | `clinsev` (`/opt/conda/envs/clinsev`), Python 3.11.15 |
| 주요 패키지 | torch 2.2.2, transformers 4.40.0, radeval 2.2.1, green-score 0.0.12, bert-score 0.3.13 |
| 현재 GPU | NVIDIA H200 1장 (143GB), 현재 비어 있음 |
| 논문 기재 GPU | RTX A6000 ×2, 약 45h wall-clock / 85–90 GPU-h |
| HF cache 보유 모델 | GREEN-radllama2-7b, RaTE-NER-Deberta, BioLORD-2023-C, distilbert-base-uncased, Qwen2.5-7B-Instruct, Qwen2.5-VL 계열 등 |
| API key | OPENAI / ANTHROPIC / GEMINI 환경변수 **없음**. HF token 파일은 있음 |
| vLLM | 미설치 |

---

## 3. 파이프라인 (코드 기준)

### 3.1 전체 흐름
```
prepare  →  minpairs  →  (filter_contaminated_pairs)  →  make_metric_subset
   →  fast_metrics / radeval  →  join  →  analyze / analyze_meaning_auroc
   →  annotation package → human labels → analyze_human_majority_auroc
```

### 3.2 `prepare` (섹션 추출)
- 헤더 정규식으로 FINDINGS / IMPRESSION / CONCLUSION / ... 분리
- **fallback**: `impression = impression or findings or text`, `findings = findings or impression or text`
- `min_words >= 5`, `drop_duplicates(subset=["impression"])`
- 결과 172,171 reports. **findings 텍스트와 impression 텍스트가 동일한 비율 58.1%** → `2_audit...md` D절 참조

### 3.3 `minpairs` (perturbation 생성)
- report마다 `rng = Random(seed + md5(report_id) % 100000)`, 13개 perturber를 순서대로 적용
- 각 perturber는 **첫 번째 매칭 하나만** 치환 (`replace_first`)

| 타입 | 실제 코드 동작 | 논문/rebuttal 설명과의 차이 |
|---|---|---|
| identity | 그대로 | |
| benign_format | 2문장 이상: 모든 문장 앞에 `- ` bullet. 1문장: 앞에 `Report impression: ` 접두 | findings 섹션에도 "Report impression:"이 붙음 |
| benign_sentence_order | 3문장 이상일 때 문장 shuffle | 문장 분리가 `Dr.`, `1.`, `p.m.`에서 깨짐 |
| benign_paraphrase_rule | 정규식 4개뿐 | subset200의 81%가 `There is no → No` 하나 |
| negation_flip | (a) `no/without X` → `X is present` (b) 없으면 긍정 finding 앞에 `no ` 삽입 | (b)가 비문을 만듦 |
| laterality_flip | `left→right`, `right→left`, **`bilateral→left/right`** 순서로 첫 매칭 | 논문·rebuttal은 "bilateral은 skip"이라고 기술 |
| anatomy_region_flip | 11개 구문 매핑 (upper↔lower lobe, base↔apex 등) | |
| severity_flip | `mild→severe, small→large, trace→large, moderate→mild ...` | 인접 등급이 아니라 대부분 양극단 교체 |
| uncertainty_flip | (a) `possible→definite` 등 9개 (b) 없으면 finding 앞에 `possible ` 삽입 | (b)가 80% 이상 |
| temporal_comparison_flip | `stable/unchanged→increased, improved→worsened ...` 8개 | rebuttal은 `new`, `worsened`도 trigger라 했으나 코드 매핑에 없음 |
| finding_deletion | 비부정 finding 문장 1개 삭제. 남는 게 없으면 `No acute cardiopulmonary abnormality.` | |
| false_finding_insertion | 템플릿 5개 중 하나를 끝에 append | 템플릿에 laterality·severity·size가 같이 들어 있음 |
| measurement_flip | 첫 `숫자+mm/cm`의 **단위만** 교체 | 논문은 "numeric value or unit"을 바꾼다고 기술 |

- `SEVERITY_LEVEL`은 코드상 **0–4 다섯 단계**: benign 0 / uncertainty 1 / anatomy·severity 2 / temporal·negation·laterality 3 / deletion·insertion·measurement 4

### 3.4 필터링과 subset
- `filter_contaminated_pairs.py`: identity reference에 `FINAL REPORT|REASON FOR EXAMINATION|EXAMINATION:|INDICATION:|TECHNIQUE:`가 있으면 report 통째로 제거
  - impression 5000 → 4666 reports (334 제거), findings 5000 → 4667 (333 제거)
  - clean pair 수: impression 36,488 / findings 40,941 (identity 포함)
- `make_metric_subset.py`: 타입별 `n_per_type`개를 **독립적으로** 샘플 + 해당 report의 identity 행 추가
  - subset200: 비-identity 2,400 (12타입×200) + identity 1,741(imp) / 1,727(find) = 4,141 / 4,127행
  - subset500: 8,934 / 9,183행 (measurement 등은 500개 미만)
  - 타입별 독립 샘플이라 **같은 reference에서 benign과 changed가 함께 뽑힌 경우가 드묾** → inversion 계산 쌍이 304(imp) / 334(find)개뿐

### 3.5 Metric 실행
| 논문 표기 | 실제 구현 | 확인된 설정 |
|---|---|---|
| BERTScore | RadEval `bertscore` | **`distilbert-base-uncased`, layer 5, `rescale_with_baseline=True`, idf=False** (논문 미기재) |
| F1CheXbert | RadEval `f1chexbert` | per-sample |
| RadGraph | RadEval `radgraph` | |
| RaTEScore | RadEval `ratescore` | RaTE-NER-Deberta + BioLORD |
| Temporal | RadEval `temporal` (f1temporal) | temporal 단어가 없으면 Δ=0 |
| GREEN | RadEval `green` | `StanfordAIMI/GREEN-radllama2-7b` |
| BLEU, ROUGE-L, token_f1, jaccard, clinical_* | `clinsev_pipeline.py` 자체 구현 | full clean 5k에서 실행 |

### 3.6 분석 (`cmd_analyze`, `analyze_meaning_auroc.py`)
- **AUROC**: non-identity 전체, changed(9타입)=1 vs benign(3타입)=0, score=Δ. CI는 class-stratified bootstrap 2,000회 (candidate 단위)
- **Inversion** (코드): 같은 report 안의 (benign, **critical 5타입**) 쌍 중 `benign Δ > critical Δ`인 **쌍의 비율**
- **Blindness** (코드): **critical 5타입**에 대해서만, `Δ ≤ median(benign Δ) + 1e-6`인 비율
- **Gap** (코드): `mean(critical 5타입 Δ) − mean(benign Δ)`
- **Spearman / pairwise accuracy**: 0–4 `severity_level` 사용
- `configs/strong.yaml`의 `critical_types` = negation, laterality, finding_deletion, false_finding_insertion, measurement

---

## 4. 실험 결과 인벤토리

### 4.1 본 실험 (논문에 사용)
| 실험 | 파일 | 논문 위치 |
|---|---|---|
| subset200 6-metric AUROC | `results/analysis/radeval_*_clean_subset200_broad/` | Table 3, Fig.2 |
| subset200 blindness | 같은 폴더 `blindness_rates.csv` | Fig.3 (5타입만) |
| subset500 4-metric card | `results/analysis/radeval_*_clean_subset500_core/` | Appendix C |
| full clean 5k lexical | `results/analysis/fast_*_5000_seed0_clean/` | Appendix B |
| human validation | `results/meaning_annotation_480_filled*/` | Table 2, Appendix E |
| human-label AUROC | `results/analysis/annotation480_human_majority_auroc/` | Table 3 |
| orientation audit | `results/metric_orientation/` | Appendix D |
| qualitative | `results/paper_examples/qualitative_examples_v2/` | Table 4 |

### 4.2 타입별 평균 penalty (subset200, impression) — 본문에 없던 원자료

| 타입 | BERTScore | F1CheXbert | RaTEScore | Temporal | RadGraph | GREEN |
|---|---|---|---|---|---|---|
| benign_format | 0.0725 | 0.002 | 0.049 | 0 | 0.084 | 0.006 |
| benign_sentence_order | 0.0774 | 0.008 | 0.011 | 0 | 0.104 | 0.020 |
| benign_paraphrase_rule | 0.0237 | 0.005 | 0.023 | 0 | 0.057 | 0.004 |
| negation_flip | 0.0247 | 0.069 | 0.064 | 0 | 0.124 | 0.292 |
| laterality_flip | 0.0064 | 0 | 0.044 | 0 | 0.081 | 0.263 |
| measurement_flip | 0.0036 | 0 | 0.022 | 0 | 0.064 | 0.124 |
| severity_flip | 0.0059 | 0 | 0.058 | 0 | 0.081 | 0.246 |
| uncertainty_flip | 0.0127 | 0.004 | 0.061 | 0 | 0.096 | 0.063 |
| anatomy_region_flip | 0.0101 | 0.001 | 0.053 | 0 | 0.096 | 0.254 |
| temporal_comparison_flip | 0.0121 | 0.008 | 0.049 | 0.561 | 0.087 | 0.237 |
| finding_deletion | 0.2251 | 0.172 | 0.256 | 0.256 | 0.401 | 0.417 |
| false_finding_insertion | 0.0863 | 0.098 | 0.092 | 0.317 | 0.196 | 0.277 |

- BERTScore의 큰 penalty는 **토큰이 많이 바뀌는** format / sentence_order / deletion / insertion에 집중된다.

### 4.3 Human validation 요약
| 항목 | 값 |
|---|---|
| 항목 수 / judgment 수 | 480 / 840 |
| 구성 | 12타입 × 40 (impression 20 + findings 20), overlap 180(3중) + 단일 300 |
| aggregated UNCERTAIN | 13개 (그중 11개가 uncertainty_flip) |
| human-rule agreement | 93.1% (Wilson 90.5–95.1), n=467 |
| benign→YES / changed→NO | 90.8% / 93.9% |
| Fleiss κ (3-class, overlap 180) | 0.430 |
| pairwise Cohen κ | A–B 0.558, A–C 0.406, B–C 0.336 |
| annotator | 비저자 대학원생 3명 (medical-AI/NLP), 임상 경험 없음 |
| IRB | 미신청 (checklist D4 = No) |

### 4.4 Rebuttal 기간 추가 실험 (논문 본문에는 아직 없음)
| 실험 | 결과 | 파일 | 상태 |
|---|---|---|---|
| 9타입 전체 per-type AUROC | rebuttal 표 (GREEN uncertainty 0.585/0.535 등) | `results/rebuttal_numbers/per_type_auroc/` | 사용 가능 |
| UNCERTAIN 3가지 처리 | GREEN 0.814 / 0.802 / 0.815, 순위 불변, 최대 변화 0.023 | `results/rebuttal_numbers/jzA1_uncertain_sensitivity/` | 사용 가능 |
| OpenI/IU X-Ray transfer | 3,955 reports → 7,241 sections → 18,159 pairs. GREEN 0.925(subset10, n=120), RaTEScore 0.778(n=595), RadGraph 0.715, Temporal 0.577, F1CheXbert 0.552, BERTScore 0.270 (subset50, n=600) | `results/analysis/external_openi_*_strict/` | 규모가 작고 GREEN만 subset이 다름 |
| Llama-3-8B rubric judge | rule AUROC 0.760 / 0.736 (subset50), human 0.710 | `results/llm_rubric/`, `results/analysis/llama3_8b_rubric_*` | 모델 1개, 프롬프트 1개 |
| Composed stress (format/paraphrase/long_context) | benign Δ가 전부 0 | `results/rebuttal_numbers/composed_stress_*` | **설계 결함으로 rebuttal에 미사용** (§5.3) |
| ReEvalMed 비교표 | 정성 비교 표 | `results/rebuttal_numbers/reevalmed_comparison_table.md` | 사용 가능 |
| CheXpert/NIH 텍스트 audit | free-text report 없음 | `results/rebuttal_numbers/external_asset_audit/` | 사용 불가 확인 |
| GEMA-Score | 코드·가중치 다운로드만 | `external/` | 결과 없음 |

### 4.5 기록된 실패 (logs 기준)
| 실패 | 로그 메시지 | 조치 |
|---|---|---|
| GREEN 4-GPU coexist | `CUDA out of memory` (mem fraction 0.2 제한) 8회 | H200 단독 실행으로 전환 |
| radgraph / radcliq / radgraph_radcliq | `No module named 'RadEval'` 각 5회 | `sys.modules` alias 패치로 radgraph만 해결. **RadCliQ는 끝내 결과 없음** |
| radeval_bertscore | tokenizer 로딩 오류 (`untagged enum ModelWrapper`) | 미해결, 결과 없음 |
| ratescore (full 5k) | 길이 불일치 39,616 vs 39,619 | subset으로 회피 |
| ratescore (OpenI) | `list index out of range` 2회 | `_safe` 버전에서 5개 행 제외 (n=595) |
| annotation set metric | 10개 candidate 점수 누락 (470/480) | rebuttal 때 보완했다고 기술 |

---

## 5. 논문 기술과 실제 코드/데이터의 불일치

재제출 시 반드시 코드 또는 본문 중 한쪽을 고쳐 일치시켜야 하는 항목.

### 5.1 Perturbation 규칙
| # | 논문/rebuttal 기술 | 실제 | 근거 |
|---|---|---|---|
| R1 | laterality: bilateral/ambiguous는 skip | `bilateral → left/right` 치환이 존재. full clean 5k에서 impression 9.1%, findings 6.3% | `perturb_laterality_flip` |
| R2 | measurement: value 또는 unit 변경 | 100% 단위 교체(cm↔mm)만 | `perturb_measurement_flip` |
| R3 | temporal trigger에 `new`, `worsened` 포함 | `TEMPORAL_MAP`에 없음 | |
| R4 | negation: administrative/non-finding context 회피 | 회피 로직 없음. 부정 탐지는 finding 앞 45자 window뿐 | `has_negation_near` |
| R5 | "each candidate changes a single targeted factor" | false_finding_insertion 템플릿은 finding+laterality+severity+size 동시 포함 | `FINDING_INSERT_TEMPLATES` |

### 5.2 진단 지표 정의
| # | 논문 기술 | 실제 |
|---|---|---|
| D1 | inversion = report 단위, "benign 하나가 changed 하나보다 크면" | (benign, critical) **쌍 단위 비율**, critical 5타입만 |
| D2 | blindness = 각 meaning-changing 타입 | critical 5타입만 계산 (Fig.3도 5타입) |
| D3 | penalty gap = E[Δ\|changed] − E[Δ\|preserved] | card의 gap은 critical 5타입 기준. (AUROC 표의 mean penalty는 9타입 기준이라 두 수치가 다름) |
| D4 | rule tier = 0/1/2 (benign/attribute/core) | 0–4 다섯 단계, temporal이 negation과 같은 3단계 |

### 5.3 기타
| # | 내용 |
|---|---|
| E1 | BERTScore backbone(distilbert-base-uncased, L5, baseline rescale)이 본문·부록 어디에도 없음 |
| E2 | Appendix D orientation audit은 n=470인데 human AUROC는 n=467 (본문에 설명은 있으나 혼란스러움) |
| E3 | rebuttal 데이터 구성 표(`dataset_and_rule_tables.md`)의 subset200 행은 clean 이전 파일(4,166 / 4,207행)을 가리킴. 논문 수치(4,141 / 4,127)와 다름 |
| E4 | Composed stress의 benign counterpart는 `candidate = reference`라서 identity와 동일 → benign Δ=0. stress test로 성립하지 않음 |
| E5 | annotation 샘플링이 Python `hash()`에 의존 → `PYTHONHASHSEED` 없이는 재현 불가 (저장된 metadata 파일로만 복원 가능) |
| E6 | Llama rubric은 identity 행을 모델 호출 없이 PRESERVED로 고정. 점수가 0 / 0.5 / 1 세 값뿐 |
| E7 | README는 아직 옛 thesis("clinical-severity sensitive", monotonicity)를 기술 |
| E8 | 제목/디렉토리 표기 혼재: ClinSevBench(구), ClinSemBench(현), 디렉토리명 ClimSemBench |

---

## 6. 재사용 가능한 자산

| 자산 | 위치 | 재사용 시 주의 |
|---|---|---|
| 전처리된 MIMIC 172k reports | `OLD/data/processed/reports_mimic_txt_dir.csv` | 섹션 fallback 문제로 **재파싱 필요** |
| OpenI/IU 7,241 sections | `OLD/data/external_reports/openi_iu_xray_reports.csv` | `XXXX` 비식별 토큰 포함 |
| 480쌍 human label (개별 judgment 포함) | `OLD/data/annotation_meaning_480/`, `OLD/results/meaning_annotation_480_filled/` | 구 규칙으로 만든 쌍에 대한 라벨 |
| subset200 6-metric 점수 | `OLD/results/analysis/radeval_*_clean_subset200_broad/scored_with_drops.csv` | 구 benchmark 기준 baseline으로 사용 |
| RadEval 실행 wrapper | `clinsev_pipeline.py::cmd_radeval` | `NEW/scripts/`로 복사해서 사용 |
| RadEval 2.2.1에 포함된 미사용 metric | crimson(`rajpurkarlab/medgemma-4b-it-crimson` HF 모델 지원), radcliq, srrbert, radevalbertscore, radfact_ct | CRIMSON을 API 없이 로컬 실행 가능 |
