# 10/7 review re-analysis — iu

## A. Ctrl-0: win / tie / loss

| metric | win | tie | loss | paired_acc | win_among_decided |
|---|---|---|---|---|---|
| bertscore_distilbert | 0.658 | 0.000 | 0.342 | 0.658 | 0.658 |
| bertscore_roberta_large | 0.674 | 0.000 | 0.326 | 0.674 | 0.674 |
| bertscore_deberta_mnli | 0.790 | 0.000 | 0.210 | 0.790 | 0.790 |
| crimson | 0.622 | 0.375 | 0.003 | 0.809 | 0.995 |
| f1chexbert | 0.040 | 0.960 | 0.000 | 0.520 | 1.000 |
| green | 0.712 | 0.280 | 0.008 | 0.852 | 0.989 |
| bleu | 0.208 | 0.700 | 0.092 | 0.558 | 0.693 |
| rougeL | 0.302 | 0.609 | 0.089 | 0.607 | 0.773 |
| token_f1 | 0.369 | 0.538 | 0.093 | 0.638 | 0.798 |
| jaccard | 0.361 | 0.538 | 0.101 | 0.630 | 0.781 |
| radcliq | 0.725 | 0.000 | 0.275 | 0.725 | 0.725 |
| radgraph | 0.288 | 0.561 | 0.152 | 0.568 | 0.655 |
| ratescore | 0.608 | 0.140 | 0.252 | 0.678 | 0.707 |
| srrbert | 0.211 | 0.774 | 0.015 | 0.598 | 0.935 |
| temporal | 0.042 | 0.956 | 0.002 | 0.520 | 0.949 |
| gemma3_27b__errors | 0.108 | 0.876 | 0.016 | 0.546 | 0.873 |
| gemma3_27b__rubric | 0.837 | 0.160 | 0.003 | 0.917 | 0.996 |
| gptoss_120b__errors | 0.942 | 0.055 | 0.003 | 0.969 | 0.996 |
| gptoss_120b__rubric | 0.928 | 0.070 | 0.002 | 0.963 | 0.998 |
| gptoss_20b__errors | 0.872 | 0.128 | 0.000 | 0.936 | 1.000 |
| gptoss_20b__rubric | 0.936 | 0.062 | 0.002 | 0.967 | 0.998 |
| llama31_8b__rubric | 0.565 | 0.428 | 0.007 | 0.779 | 0.988 |
| llama31_8b__rubric_unit | 0.518 | 0.474 | 0.008 | 0.755 | 0.985 |
| qwen3_32b__errors | 0.772 | 0.220 | 0.008 | 0.882 | 0.990 |
| qwen3_32b__rubric | 0.876 | 0.112 | 0.011 | 0.933 | 0.987 |
| qwen3_32b__rubric_unit | 0.866 | 0.117 | 0.017 | 0.925 | 0.981 |
| qwen3_32b_think__rubric | 0.948 | 0.045 | 0.007 | 0.971 | 0.993 |

## B. Strict-matched subset (P0 and C0 exactly tied on Jaccard and token F1): n=443 of 890; by type {'temporal': 135, 'anatomy': 101, 'laterality': 71, 'severity': 67, 'negation': 36, 'measurement': 25, 'uncertainty': 8}

| metric | n_strict | Ctrl-0 all | Ctrl-0 strict | Ctrl-2 all | Ctrl-2 strict | tie_strict |
|---|---|---|---|---|---|---|
| bertscore_distilbert | 443 | 0.658 | 0.679 | 0.660 | 0.659 | 0.000 |
| bertscore_roberta_large | 443 | 0.674 | 0.691 | 0.694 | 0.688 | 0.000 |
| bertscore_deberta_mnli | 443 | 0.790 | 0.810 | 0.798 | 0.799 | 0.000 |
| crimson | 443 | 0.809 | 0.800 | 0.805 | 0.798 | 0.400 |
| f1chexbert | 443 | 0.520 | 0.512 | 0.518 | 0.508 | 0.975 |
| green | 443 | 0.852 | 0.876 | 0.764 | 0.740 | 0.235 |
| bleu | 443 | 0.558 | 0.509 | 0.552 | 0.510 | 0.973 |
| rougeL | 443 | 0.607 | 0.500 | 0.608 | 0.500 | 1.000 |
| token_f1 | 443 | 0.638 | 0.500 | 0.640 | 0.503 | 1.000 |
| jaccard | 443 | 0.630 | 0.500 | 0.625 | 0.502 | 1.000 |
| radcliq | 443 | 0.725 | 0.709 | 0.728 | 0.675 | 0.000 |
| radgraph | 443 | 0.568 | 0.525 | 0.582 | 0.526 | 0.693 |
| ratescore | 443 | 0.678 | 0.678 | 0.672 | 0.665 | 0.093 |
| srrbert | 443 | 0.598 | 0.578 | 0.598 | 0.578 | 0.817 |
| temporal | 443 | 0.520 | 0.519 | 0.520 | 0.519 | 0.962 |
| gemma3_27b__errors | 443 | 0.546 | 0.547 | 0.344 | 0.350 | 0.874 |
| gemma3_27b__rubric | 443 | 0.917 | 0.928 | 0.928 | 0.939 | 0.140 |
| gptoss_120b__errors | 443 | 0.969 | 0.960 | 0.960 | 0.962 | 0.065 |
| gptoss_120b__rubric | 443 | 0.963 | 0.984 | 0.965 | 0.985 | 0.023 |
| gptoss_20b__errors | 443 | 0.936 | 0.905 | 0.933 | 0.916 | 0.191 |
| gptoss_20b__rubric | 443 | 0.967 | 0.959 | 0.957 | 0.954 | 0.072 |
| llama31_8b__rubric | 443 | 0.779 | 0.748 | 0.747 | 0.734 | 0.490 |
| llama31_8b__rubric_unit | 443 | 0.755 | 0.734 | 0.736 | 0.716 | 0.528 |
| qwen3_32b__errors | 443 | 0.882 | 0.862 | 0.870 | 0.868 | 0.262 |
| qwen3_32b__rubric | 443 | 0.933 | 0.945 | 0.915 | 0.930 | 0.070 |
| qwen3_32b__rubric_unit | 443 | 0.925 | 0.927 | 0.915 | 0.931 | 0.097 |
| qwen3_32b_think__rubric | 443 | 0.971 | 0.982 | 0.969 | 0.976 | 0.027 |

## C. Exchange rate: one context paraphrase / one reordering, in units of one matched meaning change

| metric | paraphrase_in_meaning_changes | reorder_in_meaning_changes |
|---|---|---|
| bertscore_distilbert | 52.80 | 34.48 |
| bertscore_roberta_large | 27.14 | 21.98 |
| bertscore_deberta_mnli | 7.12 | 6.79 |
| crimson | 0.00 | 0.00 |
| f1chexbert | 0.75 | 0.25 |
| green | 0.33 | 0.21 |
| bleu | 281.76 | 51.02 |
| rougeL | 47.31 | 69.86 |
| token_f1 | 22.34 | 0.00 |
| jaccard | 17.67 | 0.00 |
| radcliq | 11.70 | 5.09 |
| radgraph | 17.55 | 3.47 |
| ratescore | 6.32 | 0.78 |
| srrbert | 0.77 | 0.05 |
| temporal | 8.02 | 0.00 |
| gemma3_27b__errors | 4.56 | 2.95 |
| gemma3_27b__rubric | -0.17 | 0.02 |
| gptoss_120b__errors | 0.04 | 0.02 |
| gptoss_120b__rubric | 0.01 | 0.01 |
| gptoss_20b__errors | 0.06 | -0.01 |
| gptoss_20b__rubric | 0.03 | -0.00 |
| llama31_8b__rubric | 0.12 | 0.55 |
| llama31_8b__rubric_unit | 0.04 | 0.50 |
| qwen3_32b__errors | 0.10 | 0.07 |
| qwen3_32b__rubric | -0.10 | -0.05 |
| qwen3_32b__rubric_unit | -0.08 | -0.05 |
| qwen3_32b_think__rubric | -0.00 | -0.01 |

## D. S2 subset whose paraphrased context keeps all degree words: n=766 of 890

| metric | n | Ctrl-0 | Ctrl-2 | Conf-P | drop(all) | drop(degree-preserving) |
|---|---|---|---|---|---|---|
| bertscore_distilbert | 766 | 0.659 | 0.664 | 0.022 | -0.001 | -0.005 |
| bertscore_roberta_large | 766 | 0.666 | 0.685 | 0.021 | -0.020 | -0.020 |
| bertscore_deberta_mnli | 766 | 0.789 | 0.798 | 0.051 | -0.008 | -0.009 |
| crimson | 766 | 0.806 | 0.802 | 0.806 | 0.005 | 0.004 |
| f1chexbert | 766 | 0.522 | 0.519 | 0.508 | 0.002 | 0.003 |
| green | 766 | 0.854 | 0.764 | 0.739 | 0.088 | 0.091 |
| bleu | 766 | 0.552 | 0.547 | 0.018 | 0.006 | 0.005 |
| rougeL | 766 | 0.599 | 0.601 | 0.021 | -0.002 | -0.002 |
| token_f1 | 766 | 0.632 | 0.635 | 0.035 | -0.002 | -0.003 |
| jaccard | 766 | 0.627 | 0.623 | 0.039 | 0.005 | 0.004 |
| radcliq | 766 | 0.718 | 0.726 | 0.054 | -0.003 | -0.008 |
| radgraph | 766 | 0.563 | 0.580 | 0.074 | -0.014 | -0.017 |
| ratescore | 766 | 0.678 | 0.672 | 0.210 | 0.006 | 0.007 |
| srrbert | 766 | 0.592 | 0.592 | 0.506 | 0.000 | 0.000 |
| temporal | 766 | 0.521 | 0.521 | 0.455 | 0.000 | 0.000 |
| gemma3_27b__errors | 766 | 0.541 | 0.341 | 0.078 | 0.202 | 0.200 |
| gemma3_27b__rubric | 766 | 0.913 | 0.928 | 0.958 | -0.011 | -0.016 |
| gptoss_120b__errors | 766 | 0.973 | 0.969 | 0.963 | 0.009 | 0.004 |
| gptoss_120b__rubric | 766 | 0.961 | 0.964 | 0.969 | -0.002 | -0.003 |
| gptoss_20b__errors | 766 | 0.943 | 0.943 | 0.933 | 0.003 | -0.001 |
| gptoss_20b__rubric | 766 | 0.969 | 0.963 | 0.968 | 0.010 | 0.007 |
| llama31_8b__rubric | 766 | 0.779 | 0.747 | 0.774 | 0.032 | 0.032 |
| llama31_8b__rubric_unit | 766 | 0.755 | 0.735 | 0.755 | 0.019 | 0.020 |
| qwen3_32b__errors | 766 | 0.888 | 0.874 | 0.836 | 0.012 | 0.014 |
| qwen3_32b__rubric | 766 | 0.935 | 0.913 | 0.961 | 0.018 | 0.022 |
| qwen3_32b__rubric_unit | 766 | 0.926 | 0.916 | 0.956 | 0.010 | 0.010 |
| qwen3_32b_think__rubric | 766 | 0.972 | 0.969 | 0.975 | 0.002 | 0.003 |

## E. Uncertainty without the 'consistent with / suspicious for / suggestive of' family; D-10 '-sided sided' targets: 2

| metric | uncertainty all (n=94) | uncertainty w/o consistent-with family (n=36) |
|---|---|---|
| bertscore_distilbert | 0.798 | 0.861 |
| bertscore_roberta_large | 0.777 | 0.972 |
| bertscore_deberta_mnli | 0.872 | 1.000 |
| crimson | 0.543 | 0.597 |
| f1chexbert | 0.500 | 0.500 |
| green | 0.553 | 0.583 |
| bleu | 0.766 | 0.778 |
| rougeL | 0.745 | 0.333 |
| token_f1 | 0.766 | 0.778 |
| jaccard | 0.777 | 0.750 |
| radcliq | 0.830 | 0.944 |
| radgraph | 0.745 | 0.764 |
| ratescore | 0.622 | 0.667 |
| srrbert | 0.739 | 0.750 |
| temporal | 0.500 | 0.500 |
| gemma3_27b__errors | 0.574 | 0.500 |
| gemma3_27b__rubric | 0.931 | 0.972 |
| gptoss_120b__errors | 0.920 | 0.944 |
| gptoss_120b__rubric | 0.888 | 1.000 |
| gptoss_20b__errors | 0.862 | 0.833 |
| gptoss_20b__rubric | 0.894 | 0.931 |
| llama31_8b__rubric | 0.622 | 0.625 |
| llama31_8b__rubric_unit | 0.580 | 0.583 |
| qwen3_32b__errors | 0.856 | 0.903 |
| qwen3_32b__rubric | 0.824 | 0.931 |
| qwen3_32b__rubric_unit | 0.819 | 0.931 |
| qwen3_32b_think__rubric | 0.878 | 1.000 |

## F. Interaction (meaning x S2) and (meaning x S1) from decomposition.csv

| metric | meaning_effect_S0 | surface_S1 | surface_S2 | interaction_S1 | interaction_S2 |
|---|---|---|---|---|---|
| bertscore_distilbert | 0.035 | 1.193 | 1.827 | 0.003 | 0.003 |
| bertscore_roberta_large | 0.065 | 1.428 | 1.763 | -0.003 | -0.003 |
| bertscore_deberta_mnli | 0.227 | 1.541 | 1.616 | -0.055 | -0.029 |
| crimson | 0.950 | 0.004 | 0.003 | -0.000 | -0.027 |
| f1chexbert | 0.152 | 0.038 | 0.114 | -0.051 | -0.017 |
| green | 1.200 | 0.256 | 0.392 | -0.142 | -0.243 |
| bleu | 0.007 | 0.351 | 1.941 | -0.003 | -0.001 |
| rougeL | 0.029 | 1.996 | 1.351 | -0.010 | -0.000 |
| token_f1 | 0.076 | 0.000 | 1.707 | 0.000 | -0.003 |
| jaccard | 0.095 | 0.000 | 1.684 | 0.000 | -0.025 |
| radcliq | 0.149 | 0.757 | 1.740 | -0.017 | -0.018 |
| radgraph | 0.085 | 0.295 | 1.492 | 0.013 | 0.005 |
| ratescore | 0.140 | 0.109 | 0.886 | -0.021 | 0.003 |
| srrbert | 0.460 | 0.022 | 0.352 | 0.003 | -0.017 |
| temporal | 0.038 | 0.000 | 0.301 | 0.000 | -0.001 |
| gemma3_27b__errors | 0.362 | 1.069 | 1.649 | -0.529 | -0.673 |
| gemma3_27b__rubric | 1.470 | 0.035 | -0.244 | -0.123 | 0.007 |
| gptoss_120b__errors | 1.859 | 0.037 | 0.066 | -0.042 | -0.061 |
| gptoss_120b__rubric | 1.831 | 0.025 | 0.023 | -0.045 | -0.026 |
| gptoss_20b__errors | 1.731 | -0.023 | 0.104 | 0.045 | -0.052 |
| gptoss_20b__rubric | 1.860 | -0.008 | 0.065 | 0.008 | -0.087 |
| llama31_8b__rubric | 1.136 | 0.627 | 0.131 | -0.465 | -0.217 |
| llama31_8b__rubric_unit | 1.088 | 0.545 | 0.042 | -0.283 | -0.181 |
| qwen3_32b__errors | 1.427 | 0.096 | 0.137 | -0.051 | 0.017 |
| qwen3_32b__rubric | 1.690 | -0.091 | -0.163 | -0.097 | -0.105 |
| qwen3_32b__rubric_unit | 1.702 | -0.078 | -0.136 | -0.115 | -0.105 |
| qwen3_32b_think__rubric | 1.864 | -0.024 | -0.002 | 0.011 | -0.020 |

### judges: CHANGED rate on uncertainty, C0 vs C2

| judge | C0 | C2 | P0 |
|---|---|---|---|
| gemma3_27b__errors | 1.00 | 1.00 | 0.84 |
| gemma3_27b__rubric | 0.68 | 0.34 | 0.04 |
| gptoss_120b__errors | 0.90 | 0.84 | 0.06 |
| gptoss_120b__rubric | 0.76 | 0.76 | 0.01 |
| gptoss_20b__errors | 0.90 | 0.87 | 0.18 |
| gptoss_20b__rubric | 0.83 | 0.78 | 0.05 |
| llama31_8b__rubric | 0.28 | 0.37 | 0.03 |
| llama31_8b__rubric_unit | 0.18 | 0.21 | 0.02 |
| qwen3_32b__errors | 0.81 | 0.79 | 0.10 |
| qwen3_32b__rubric | 0.60 | 0.29 | 0.01 |
| qwen3_32b__rubric_unit | 0.57 | 0.31 | 0.01 |
| qwen3_32b_think__rubric | 0.69 | 0.68 | 0.00 |
