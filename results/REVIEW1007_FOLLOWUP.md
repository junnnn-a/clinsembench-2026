# 10/7 review — follow-up analyses of the GPU experiments

## A. S2 robustness: Llama-3.1-8B paraphraser + degree-word guard, 301 IU targets (context sentences with an accepted paraphrase: 86.3%)

| metric | n | Ctrl-0 (orig run) | Ctrl-2 orig paraphraser | Ctrl-2 alt paraphraser | drop orig | drop alt | drop alt lo | drop alt hi | Conf-P orig | Conf-P alt |
|---|---|---|---|---|---|---|---|---|---|---|
| bertscore_distilbert | 301 | 0.648 | 0.641 | 0.638 | 0.007 | 0.010 | -0.023 | 0.044 | 0.010 | 0.033 |
| bertscore_roberta_large | 301 | 0.664 | 0.698 | 0.678 | -0.033 | -0.013 | -0.054 | 0.026 | 0.013 | 0.043 |
| bertscore_deberta_mnli | 301 | 0.784 | 0.784 | 0.784 | 0.000 | 0.000 | -0.039 | 0.040 | 0.050 | 0.076 |
| crimson | 301 | 0.776 | 0.776 | 0.789 | 0.000 | -0.013 | -0.024 | -0.003 | 0.777 | 0.779 |
| f1chexbert | 301 | 0.517 | 0.513 | 0.515 | 0.003 | 0.002 | -0.005 | 0.008 | 0.500 | 0.477 |
| green | 301 | 0.826 | 0.731 | 0.749 | 0.095 | 0.076 | 0.041 | 0.111 | 0.694 | 0.689 |
| bleu | 301 | 0.550 | 0.542 | 0.548 | 0.008 | 0.002 | -0.015 | 0.020 | 0.008 | 0.032 |
| rougeL | 301 | 0.581 | 0.583 | 0.583 | -0.002 | -0.002 | -0.005 | 0.000 | 0.012 | 0.038 |
| token_f1 | 301 | 0.615 | 0.616 | 0.618 | -0.002 | -0.003 | -0.019 | 0.014 | 0.017 | 0.040 |
| jaccard | 301 | 0.601 | 0.593 | 0.593 | 0.008 | 0.008 | -0.008 | 0.024 | 0.017 | 0.043 |
| radcliq | 301 | 0.714 | 0.701 | 0.704 | 0.013 | 0.010 | -0.040 | 0.056 | 0.040 | 0.060 |
| radgraph | 301 | 0.565 | 0.571 | 0.535 | -0.007 | 0.030 | -0.010 | 0.069 | 0.061 | 0.073 |
| ratescore | 301 | 0.653 | 0.646 | 0.653 | 0.007 | 0.000 | -0.024 | 0.023 | 0.183 | 0.146 |
| srrbert | 301 | 0.605 | 0.605 | 0.605 | 0.000 | 0.000 | 0.000 | 0.000 | 0.518 | 0.513 |
| temporal | 301 | 0.513 | 0.513 | 0.513 | 0.000 | 0.000 | 0.000 | 0.000 | 0.420 | 0.400 |

## B. rubric vs rubric_unit (prompt states that unit conversion and abbreviation are benign)

### iu

| judge | prompt | P0 meas (all) | P0 meas:value | C0 meas | P0 all types | P0 w/o meas | C0 all types | C2 all types | Ctrl-0 | Ctrl-2 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma3_27b | rubric | 0.87 | 0.91 | 1.00 | 0.21 | 0.14 | 0.93 | 0.84 | 0.92 | 0.93 |
| gemma3_27b | rubric_unit | 0.27 | 0.16 | 0.83 | 0.11 | 0.10 | 0.90 | 0.82 | 0.94 | 0.93 |
| llama31_8b | rubric | 0.84 | 0.87 | 0.97 | 0.17 | 0.09 | 0.69 | 0.71 | 0.78 | 0.75 |
| llama31_8b | rubric_unit | 0.54 | 0.51 | 0.80 | 0.10 | 0.05 | 0.59 | 0.58 | 0.76 | 0.74 |
| qwen3_32b | rubric | 0.27 | 0.16 | 0.88 | 0.11 | 0.09 | 0.93 | 0.83 | 0.93 | 0.91 |
| qwen3_32b | rubric_unit | 0.14 | 0.07 | 0.80 | 0.09 | 0.08 | 0.92 | 0.83 | 0.92 | 0.92 |

### mimic

| judge | prompt | P0 meas (all) | P0 meas:value | C0 meas | P0 all types | P0 w/o meas | C0 all types | C2 all types | Ctrl-0 | Ctrl-2 |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma3_27b | rubric | 0.85 | 0.84 | 0.99 | 0.29 | 0.20 | 0.94 | 0.81 | 0.90 | 0.91 |
| gemma3_27b | rubric_unit | 0.12 | 0.11 | 0.81 | 0.15 | 0.16 | 0.90 | 0.77 | 0.92 | 0.92 |
| qwen3_32b | rubric | 0.96 | 0.95 | 0.99 | 0.26 | 0.14 | 0.94 | 0.82 | 0.87 | 0.89 |
| qwen3_32b | rubric_unit | 0.70 | 0.59 | 0.95 | 0.20 | 0.12 | 0.93 | 0.80 | 0.88 | 0.88 |

## C. RaTE-Eval synthetic task: share of triplets where the opposite rewrite is penalised more than the synonym rewrite

| metric | n | paired_acc | win | tie | loss |
|---|---|---|---|---|---|
| bleu | 739 | 0.115 | 0.114 | 0.003 | 0.884 |
| rougeL | 739 | 0.119 | 0.115 | 0.008 | 0.877 |
| token_f1 | 739 | 0.139 | 0.131 | 0.015 | 0.854 |
| bertscore_distilbert | 739 | 0.143 | 0.143 | 0.000 | 0.857 |
| jaccard | 739 | 0.147 | 0.138 | 0.019 | 0.843 |
| bertscore_roberta_large | 739 | 0.183 | 0.183 | 0.000 | 0.817 |
| radcliq | 739 | 0.422 | 0.422 | 0.000 | 0.578 |
| bertscore_deberta_mnli | 739 | 0.440 | 0.440 | 0.000 | 0.560 |
| radgraph | 739 | 0.472 | 0.353 | 0.237 | 0.410 |
| temporal | 739 | 0.493 | 0.042 | 0.903 | 0.055 |
| ratescore | 739 | 0.519 | 0.483 | 0.072 | 0.445 |
| f1chexbert | 739 | 0.519 | 0.054 | 0.930 | 0.016 |
| srrbert | 739 | 0.545 | 0.116 | 0.857 | 0.027 |
| crimson | 739 | 0.898 | 0.801 | 0.194 | 0.005 |
| gptoss_20b__rubric | 739 | 0.989 | 0.980 | 0.019 | 0.001 |
