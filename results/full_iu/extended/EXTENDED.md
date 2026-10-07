# Extended analysis — iu

## A. severity: controlled S0 paired accuracy by subtype

| metric | adjacent | extreme |
|---|---|---|
| bertscore_deberta_mnli | 0.319 | 0.723 |
| bertscore_distilbert | 0.000 | 0.138 |
| bertscore_roberta_large | 0.208 | 0.262 |
| bleu | 0.500 | 0.500 |
| crimson | 0.806 | 0.985 |
| f1chexbert | 0.500 | 0.500 |
| gemma3_27b__errors | 0.500 | 0.523 |
| gemma3_27b__rubric | 0.896 | 0.985 |
| gptoss_120b__errors | 0.903 | 0.869 |
| gptoss_120b__rubric | 0.944 | 0.992 |
| gptoss_20b__errors | 0.736 | 0.797 |
| gptoss_20b__rubric | 0.903 | 0.931 |
| green | 0.826 | 0.977 |
| jaccard | 0.708 | 0.762 |
| llama31_8b__rubric | 0.764 | 0.915 |
| llama31_8b__rubric_unit | 0.757 | 0.908 |
| qwen3_32b__errors | 0.750 | 0.838 |
| qwen3_32b__rubric | 0.917 | 0.992 |
| qwen3_32b__rubric_unit | 0.903 | 0.977 |
| qwen3_32b_think__rubric | 0.931 | 0.985 |
| radcliq | 0.306 | 0.400 |
| radgraph | 0.326 | 0.331 |
| ratescore | 0.562 | 0.738 |
| rougeL | 0.722 | 0.762 |
| srrbert | 0.507 | 0.515 |
| temporal | 0.500 | 0.500 |
| token_f1 | 0.722 | 0.762 |

## A. measurement: controlled S0 paired accuracy by subtype

| metric | unit | value |
|---|---|---|
| bertscore_deberta_mnli | 0.388 | 0.622 |
| bertscore_distilbert | 0.000 | 0.867 |
| bertscore_roberta_large | 0.020 | 0.667 |
| bleu | 0.010 | 0.500 |
| crimson | 0.745 | 0.716 |
| f1chexbert | 0.500 | 0.500 |
| gemma3_27b__errors | 0.469 | 0.511 |
| gemma3_27b__rubric | 0.612 | 0.544 |
| gptoss_120b__errors | 0.969 | 1.000 |
| gptoss_120b__rubric | 0.786 | 0.867 |
| gptoss_20b__errors | 0.990 | 1.000 |
| gptoss_20b__rubric | 0.990 | 1.000 |
| green | 0.643 | 0.811 |
| jaccard | 0.010 | 0.667 |
| llama31_8b__rubric | 0.735 | 0.567 |
| llama31_8b__rubric_unit | 0.694 | 0.600 |
| qwen3_32b__errors | 0.796 | 0.811 |
| qwen3_32b__rubric | 0.816 | 0.800 |
| qwen3_32b__rubric_unit | 0.878 | 0.756 |
| qwen3_32b_think__rubric | 0.908 | 0.933 |
| radcliq | 0.163 | 0.756 |
| radgraph | 0.490 | 0.433 |
| ratescore | 0.194 | 0.778 |
| rougeL | 0.010 | 0.667 |
| srrbert | 0.500 | 0.500 |
| temporal | 0.500 | 0.500 |
| token_f1 | 0.010 | 0.667 |

## A. negation: controlled S0 paired accuracy by subtype

| metric | negated->present | present->negated |
|---|---|---|
| bertscore_deberta_mnli | 1.000 | 1.000 |
| bertscore_distilbert | 0.738 | 0.750 |
| bertscore_roberta_large | 0.874 | 0.812 |
| bleu | 0.733 | 0.688 |
| crimson | 0.971 | 0.750 |
| f1chexbert | 0.660 | 0.500 |
| gemma3_27b__errors | 0.597 | 0.625 |
| gemma3_27b__rubric | 0.990 | 1.000 |
| gptoss_120b__errors | 0.981 | 1.000 |
| gptoss_120b__rubric | 0.985 | 1.000 |
| gptoss_20b__errors | 0.985 | 1.000 |
| gptoss_20b__rubric | 0.985 | 1.000 |
| green | 0.913 | 1.000 |
| jaccard | 0.583 | 0.531 |
| llama31_8b__rubric | 0.956 | 0.969 |
| llama31_8b__rubric_unit | 0.966 | 0.969 |
| qwen3_32b__errors | 0.947 | 1.000 |
| qwen3_32b__rubric | 0.981 | 1.000 |
| qwen3_32b__rubric_unit | 0.971 | 1.000 |
| qwen3_32b_think__rubric | 0.995 | 1.000 |
| radcliq | 0.942 | 1.000 |
| radgraph | 0.835 | 0.938 |
| ratescore | 0.767 | 0.688 |
| rougeL | 0.694 | 0.500 |
| srrbert | 0.883 | 0.844 |
| temporal | 0.549 | 0.500 |
| token_f1 | 0.694 | 0.500 |

## A. uncertainty: controlled S0 paired accuracy by subtype

| metric | definite->hedged | hedged->definite |
|---|---|---|
| bertscore_deberta_mnli | 1.000 | 0.765 |
| bertscore_distilbert | 1.000 | 0.627 |
| bertscore_roberta_large | 0.767 | 0.784 |
| bleu | 1.000 | 0.569 |
| crimson | 0.500 | 0.578 |
| f1chexbert | 0.500 | 0.500 |
| gemma3_27b__errors | 0.547 | 0.598 |
| gemma3_27b__rubric | 0.977 | 0.892 |
| gptoss_120b__errors | 0.977 | 0.873 |
| gptoss_120b__rubric | 0.872 | 0.902 |
| gptoss_20b__errors | 0.965 | 0.775 |
| gptoss_20b__rubric | 0.919 | 0.873 |
| green | 0.547 | 0.559 |
| jaccard | 0.965 | 0.618 |
| llama31_8b__rubric | 0.640 | 0.608 |
| llama31_8b__rubric_unit | 0.593 | 0.569 |
| qwen3_32b__errors | 0.895 | 0.824 |
| qwen3_32b__rubric | 0.802 | 0.843 |
| qwen3_32b__rubric_unit | 0.791 | 0.843 |
| qwen3_32b_think__rubric | 0.849 | 0.902 |
| radcliq | 0.977 | 0.706 |
| radgraph | 0.837 | 0.667 |
| ratescore | 0.593 | 0.647 |
| rougeL | 0.977 | 0.549 |
| srrbert | 0.779 | 0.706 |
| temporal | 0.500 | 0.500 |
| token_f1 | 1.000 | 0.569 |

## B. Surface dose-response (S2): extra penalty on the meaning-preserving candidate, z(D(P2) - D(P0)), by amount rewritten

| metric | Q1 (least rewritten) | Q2 | Q3 | Q4 (most rewritten) |
|---|---|---|---|---|
| bertscore_deberta_mnli | 0.85 | 1.54 | 1.84 | 2.26 |
| bertscore_distilbert | 0.95 | 1.70 | 2.02 | 2.67 |
| bertscore_roberta_large | 0.92 | 1.68 | 2.02 | 2.46 |
| bleu | 1.04 | 1.77 | 2.25 | 2.73 |
| crimson | 0.00 | 0.01 | -0.00 | 0.00 |
| f1chexbert | 0.08 | 0.17 | 0.13 | 0.07 |
| gemma3_27b__errors | 1.15 | 1.87 | 1.79 | 1.81 |
| gemma3_27b__rubric | -0.22 | -0.27 | -0.31 | -0.18 |
| gptoss_120b__errors | 0.08 | 0.07 | 0.05 | 0.07 |
| gptoss_120b__rubric | 0.04 | 0.00 | -0.00 | 0.06 |
| gptoss_20b__errors | 0.09 | 0.06 | 0.13 | 0.14 |
| gptoss_20b__rubric | 0.01 | 0.07 | 0.10 | 0.08 |
| green | 0.28 | 0.23 | 0.52 | 0.53 |
| jaccard | 1.01 | 1.58 | 1.87 | 2.30 |
| llama31_8b__rubric | 0.14 | 0.14 | 0.20 | 0.04 |
| llama31_8b__rubric_unit | 0.14 | 0.03 | 0.03 | -0.04 |
| qwen3_32b__errors | 0.27 | 0.08 | 0.17 | 0.02 |
| qwen3_32b__rubric | -0.19 | -0.21 | -0.13 | -0.13 |
| qwen3_32b__rubric_unit | -0.16 | -0.12 | -0.13 | -0.13 |
| qwen3_32b_think__rubric | 0.01 | -0.02 | -0.02 | 0.02 |
| radcliq | 0.95 | 1.58 | 1.95 | 2.50 |
| radgraph | 0.87 | 1.36 | 1.68 | 2.07 |
| ratescore | 0.50 | 0.86 | 1.01 | 1.19 |
| rougeL | 0.66 | 1.22 | 1.57 | 1.99 |
| srrbert | 0.18 | 0.36 | 0.38 | 0.49 |
| temporal | 0.17 | 0.34 | 0.32 | 0.38 |
| token_f1 | 0.95 | 1.56 | 1.92 | 2.43 |

### paired accuracy C2 vs P2 by amount rewritten

| metric | Q1 (least rewritten) | Q2 | Q3 | Q4 (most rewritten) |
|---|---|---|---|---|
| bertscore_deberta_mnli | 0.799 | 0.793 | 0.776 | 0.824 |
| bertscore_distilbert | 0.655 | 0.613 | 0.686 | 0.683 |
| bertscore_roberta_large | 0.633 | 0.696 | 0.713 | 0.738 |
| bleu | 0.544 | 0.560 | 0.525 | 0.581 |
| crimson | 0.793 | 0.792 | 0.809 | 0.826 |
| f1chexbert | 0.513 | 0.525 | 0.520 | 0.514 |
| gemma3_27b__errors | 0.382 | 0.325 | 0.332 | 0.337 |
| gemma3_27b__rubric | 0.915 | 0.931 | 0.930 | 0.934 |
| gptoss_120b__errors | 0.969 | 0.954 | 0.955 | 0.962 |
| gptoss_120b__rubric | 0.956 | 0.961 | 0.973 | 0.971 |
| gptoss_20b__errors | 0.956 | 0.940 | 0.906 | 0.931 |
| gptoss_20b__rubric | 0.969 | 0.947 | 0.953 | 0.959 |
| green | 0.801 | 0.776 | 0.720 | 0.758 |
| jaccard | 0.616 | 0.627 | 0.612 | 0.645 |
| llama31_8b__rubric | 0.749 | 0.730 | 0.756 | 0.753 |
| llama31_8b__rubric_unit | 0.749 | 0.724 | 0.729 | 0.742 |
| qwen3_32b__errors | 0.810 | 0.869 | 0.883 | 0.919 |
| qwen3_32b__rubric | 0.921 | 0.908 | 0.906 | 0.923 |
| qwen3_32b__rubric_unit | 0.937 | 0.892 | 0.908 | 0.923 |
| qwen3_32b_think__rubric | 0.954 | 0.963 | 0.980 | 0.977 |
| radcliq | 0.712 | 0.728 | 0.726 | 0.747 |
| radgraph | 0.559 | 0.565 | 0.574 | 0.631 |
| ratescore | 0.675 | 0.643 | 0.668 | 0.704 |
| rougeL | 0.598 | 0.599 | 0.583 | 0.654 |
| srrbert | 0.592 | 0.574 | 0.605 | 0.622 |
| temporal | 0.526 | 0.514 | 0.525 | 0.514 |
| token_f1 | 0.638 | 0.629 | 0.614 | 0.679 |

## C. Contrasts (report-cluster bootstrap 95% CI)

| metric | S0 | S2 | S0_minus_S2 | drop_lo | drop_hi | S0_minus_jaccard | vsJ_lo | vsJ_hi | S2_minus_jaccard | vsJ2_lo | vsJ2_hi | beats_blind_baseline_S0 | degrades_under_paraphrase |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bertscore_distilbert | 0.658 | 0.660 | -0.001 | -0.018 | 0.016 | 0.029 | -0.004 | 0.061 | 0.035 | -0.001 | 0.069 | False | False |
| bertscore_roberta_large | 0.674 | 0.694 | -0.020 | -0.042 | 0.002 | 0.044 | 0.011 | 0.079 | 0.070 | 0.036 | 0.100 | True | False |
| bertscore_deberta_mnli | 0.790 | 0.798 | -0.008 | -0.033 | 0.015 | 0.160 | 0.127 | 0.189 | 0.173 | 0.141 | 0.203 | True | False |
| crimson | 0.809 | 0.805 | 0.005 | -0.002 | 0.012 | 0.179 | 0.153 | 0.204 | 0.180 | 0.152 | 0.206 | True | False |
| f1chexbert | 0.520 | 0.518 | 0.002 | -0.001 | 0.005 | -0.110 | -0.133 | -0.087 | -0.107 | -0.129 | -0.085 | False | False |
| green | 0.852 | 0.764 | 0.088 | 0.068 | 0.108 | 0.222 | 0.198 | 0.247 | 0.139 | 0.111 | 0.167 | True | True |
| bleu | 0.558 | 0.552 | 0.006 | -0.003 | 0.015 | -0.072 | -0.092 | -0.053 | -0.072 | -0.092 | -0.053 | False | False |
| rougeL | 0.607 | 0.608 | -0.002 | -0.003 | 0.000 | -0.023 | -0.039 | -0.007 | -0.016 | -0.033 | 0.000 | False | False |
| token_f1 | 0.638 | 0.640 | -0.002 | -0.012 | 0.008 | 0.008 | -0.002 | 0.018 | 0.015 | 0.005 | 0.026 | False | False |
| jaccard | 0.630 | 0.625 | 0.005 | -0.002 | 0.012 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | False | False |
| radcliq | 0.725 | 0.728 | -0.003 | -0.028 | 0.022 | 0.095 | 0.063 | 0.125 | 0.103 | 0.071 | 0.134 | True | False |
| radgraph | 0.568 | 0.582 | -0.014 | -0.037 | 0.009 | -0.062 | -0.092 | -0.035 | -0.043 | -0.072 | -0.012 | False | False |
| ratescore | 0.678 | 0.672 | 0.006 | -0.006 | 0.018 | 0.048 | 0.019 | 0.079 | 0.048 | 0.018 | 0.078 | True | False |
| srrbert | 0.598 | 0.598 | 0.000 | 0.000 | 0.000 | -0.031 | -0.058 | -0.007 | -0.026 | -0.052 | -0.002 | False | False |
| temporal | 0.520 | 0.520 | 0.000 | 0.000 | 0.000 | -0.110 | -0.132 | -0.088 | -0.105 | -0.126 | -0.084 | False | False |
| gemma3_27b__errors | 0.546 | 0.344 | 0.202 | 0.178 | 0.226 | -0.084 | -0.108 | -0.061 | -0.280 | -0.311 | -0.249 | False | True |
| gemma3_27b__rubric | 0.917 | 0.928 | -0.011 | -0.022 | 0.001 | 0.287 | 0.265 | 0.309 | 0.303 | 0.280 | 0.327 | True | False |
| gptoss_120b__errors | 0.969 | 0.960 | 0.009 | 0.000 | 0.019 | 0.339 | 0.318 | 0.361 | 0.335 | 0.314 | 0.359 | True | False |
| gptoss_120b__rubric | 0.963 | 0.965 | -0.002 | -0.011 | 0.007 | 0.333 | 0.313 | 0.355 | 0.340 | 0.319 | 0.362 | True | False |
| gptoss_20b__errors | 0.936 | 0.933 | 0.003 | -0.007 | 0.013 | 0.306 | 0.284 | 0.329 | 0.309 | 0.286 | 0.332 | True | False |
| gptoss_20b__rubric | 0.967 | 0.957 | 0.010 | -0.001 | 0.020 | 0.337 | 0.315 | 0.359 | 0.333 | 0.310 | 0.356 | True | False |
| llama31_8b__rubric | 0.779 | 0.747 | 0.032 | 0.015 | 0.049 | 0.149 | 0.123 | 0.175 | 0.122 | 0.098 | 0.148 | True | True |
| llama31_8b__rubric_unit | 0.755 | 0.736 | 0.019 | 0.003 | 0.034 | 0.125 | 0.099 | 0.150 | 0.111 | 0.086 | 0.135 | True | True |
| qwen3_32b__errors | 0.882 | 0.870 | 0.012 | -0.007 | 0.030 | 0.252 | 0.228 | 0.277 | 0.245 | 0.218 | 0.274 | True | False |
| qwen3_32b__rubric | 0.933 | 0.915 | 0.018 | 0.003 | 0.033 | 0.303 | 0.281 | 0.326 | 0.290 | 0.264 | 0.317 | True | True |
| qwen3_32b__rubric_unit | 0.925 | 0.915 | 0.010 | -0.004 | 0.024 | 0.295 | 0.271 | 0.319 | 0.290 | 0.265 | 0.314 | True | False |
| qwen3_32b_think__rubric | 0.971 | 0.969 | 0.002 | -0.006 | 0.011 | 0.341 | 0.319 | 0.362 | 0.344 | 0.321 | 0.364 | True | False |

## D. Mixed-effects coefficients (z-scored penalty; random intercept per report)

| metric | C(surface)[T.S1] | C(surface)[T.S2] | meaning | meaning:C(surface)[T.S1] | meaning:C(surface)[T.S2] |
|---|---|---|---|---|---|
| bertscore_deberta_mnli | 1.541 | 1.616 | 0.227 | -0.055 | -0.029 |
| bertscore_distilbert | 1.193 | 1.827 | 0.035 | 0.003 | 0.003 |
| bertscore_roberta_large | 1.428 | 1.763 | 0.065 | -0.003 | -0.003 |
| bleu | 0.351 | 1.941 | 0.007 | -0.003 | -0.001 |
| crimson | 0.004 | 0.003 | 0.948 | -0.000 | -0.026 |
| f1chexbert | 0.038 | 0.114 | 0.152 | -0.051 | -0.017 |
| gemma3_27b__errors | 1.069 | 1.649 | 0.362 | -0.529 | -0.673 |
| gemma3_27b__rubric | 0.035 | -0.244 | 1.470 | -0.123 | 0.007 |
| gptoss_120b__errors | 0.037 | 0.066 | 1.859 | -0.042 | -0.061 |
| gptoss_120b__rubric | 0.025 | 0.023 | 1.831 | -0.045 | -0.026 |
| gptoss_20b__errors | -0.029 | 0.101 | 1.730 | 0.045 | -0.057 |
| gptoss_20b__rubric | -0.008 | 0.065 | 1.860 | 0.008 | -0.086 |
| green | 0.256 | 0.392 | 1.200 | -0.142 | -0.243 |
| jaccard | -0.000 | 1.684 | 0.095 | 0.000 | -0.025 |
| llama31_8b__rubric | 0.627 | 0.131 | 1.136 | -0.465 | -0.217 |
| llama31_8b__rubric_unit | 0.545 | 0.042 | 1.088 | -0.283 | -0.181 |
| qwen3_32b__errors | 0.096 | 0.137 | 1.427 | -0.051 | 0.017 |
| qwen3_32b__rubric | -0.091 | -0.163 | 1.690 | -0.097 | -0.105 |
| qwen3_32b__rubric_unit | -0.078 | -0.136 | 1.702 | -0.115 | -0.105 |
| qwen3_32b_think__rubric | -0.024 | -0.002 | 1.864 | 0.011 | -0.020 |
| radcliq | 0.757 | 1.740 | 0.149 | -0.017 | -0.018 |
| radgraph | 0.295 | 1.492 | 0.085 | 0.013 | 0.005 |
| ratescore | 0.109 | 0.886 | 0.140 | -0.021 | 0.003 |
| rougeL | 1.996 | 1.351 | 0.029 | -0.010 | -0.000 |
| srrbert | 0.022 | 0.352 | 0.460 | 0.003 | -0.017 |
| temporal | 0.000 | 0.301 | 0.038 | -0.000 | -0.001 |
| token_f1 | -0.000 | 1.707 | 0.076 | 0.000 | -0.003 |

## E. CRIMSON error attribution — share of candidates with >=1 error (any / expected category / only other categories)

| cell | edit_type | n | any_error | expected_category_fired | only_other_category |
|---|---|---|---|---|---|
| P0 | anatomy | 150 | 0.107 | 0.107 | 0.000 |
| P0 | laterality | 146 | 0.048 | 0.041 | 0.007 |
| P0 | measurement | 94 | 0.628 | 0.628 | 0.000 |
| P0 | negation | 119 | 0.000 | 0.000 | 0.000 |
| P0 | severity | 137 | 0.518 | 0.518 | 0.000 |
| P0 | temporal | 150 | 0.133 | 0.127 | 0.007 |
| P0 | uncertainty | 94 | 0.521 | 0.521 | 0.000 |
| C0 | anatomy | 150 | 0.947 | 0.940 | 0.007 |
| C0 | laterality | 146 | 0.918 | 0.911 | 0.007 |
| C0 | measurement | 94 | 0.957 | 0.947 | 0.011 |
| C0 | negation | 119 | 0.950 | 0.916 | 0.034 |
| C0 | severity | 137 | 0.993 | 0.985 | 0.007 |
| C0 | temporal | 150 | 0.673 | 0.453 | 0.220 |
| C0 | uncertainty | 94 | 0.979 | 0.957 | 0.021 |

### C0: which category fires (share of candidates)

| edit_type | false_findings | missing_findings | location_errors | severity_errors | descriptor_errors | measurement_errors | certainty_errors | unspecific_errors | overinterpretation_errors | temporal_errors |
|---|---|---|---|---|---|---|---|---|---|---|
| anatomy | 0.01 | 0.01 | 0.94 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| laterality | 0.00 | 0.00 | 0.91 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.00 | 0.00 |
| measurement | 0.00 | 0.00 | 0.00 | 0.01 | 0.00 | 0.95 | 0.00 | 0.00 | 0.00 | 0.00 |
| negation | 0.80 | 0.12 | 0.01 | 0.01 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 |
| severity | 0.01 | 0.00 | 0.00 | 0.99 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| temporal | 0.17 | 0.01 | 0.00 | 0.01 | 0.04 | 0.00 | 0.00 | 0.00 | 0.00 | 0.45 |
| uncertainty | 0.00 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.96 | 0.00 | 0.01 | 0.00 |

## F. Robustness: controlled S0 paired accuracy on target subsets

| metric | all targets (n=890) | excl. P lexicon pending expert review (n=724) | excl. all three (n=673) | excl. awkward negation fragments (n=888) | excl. measurement:unit (P edit larger than C) (n=841) |
|---|---|---|---|---|---|
| bertscore_deberta_mnli | 0.790 | 0.833 | 0.865 | 0.789 | 0.813 |
| bertscore_distilbert | 0.658 | 0.735 | 0.789 | 0.659 | 0.697 |
| bertscore_roberta_large | 0.674 | 0.753 | 0.805 | 0.673 | 0.712 |
| bleu | 0.558 | 0.580 | 0.621 | 0.557 | 0.590 |
| crimson | 0.809 | 0.805 | 0.808 | 0.809 | 0.813 |
| f1chexbert | 0.520 | 0.525 | 0.527 | 0.520 | 0.521 |
| gemma3_27b__errors | 0.546 | 0.534 | 0.539 | 0.546 | 0.551 |
| gemma3_27b__rubric | 0.917 | 0.914 | 0.937 | 0.917 | 0.935 |
| gptoss_120b__errors | 0.969 | 0.990 | 0.992 | 0.969 | 0.969 |
| gptoss_120b__rubric | 0.963 | 0.966 | 0.979 | 0.963 | 0.973 |
| gptoss_20b__errors | 0.936 | 0.962 | 0.960 | 0.936 | 0.933 |
| gptoss_20b__rubric | 0.967 | 0.980 | 0.979 | 0.967 | 0.966 |
| green | 0.852 | 0.853 | 0.869 | 0.853 | 0.864 |
| jaccard | 0.630 | 0.620 | 0.664 | 0.630 | 0.666 |
| llama31_8b__rubric | 0.779 | 0.785 | 0.788 | 0.779 | 0.782 |
| llama31_8b__rubric_unit | 0.755 | 0.760 | 0.765 | 0.755 | 0.759 |
| qwen3_32b__errors | 0.882 | 0.897 | 0.906 | 0.883 | 0.887 |
| qwen3_32b__rubric | 0.933 | 0.939 | 0.949 | 0.934 | 0.939 |
| qwen3_32b__rubric_unit | 0.925 | 0.934 | 0.940 | 0.926 | 0.927 |
| qwen3_32b_think__rubric | 0.971 | 0.979 | 0.984 | 0.971 | 0.974 |
| radcliq | 0.725 | 0.775 | 0.819 | 0.724 | 0.757 |
| radgraph | 0.568 | 0.601 | 0.609 | 0.568 | 0.573 |
| ratescore | 0.678 | 0.681 | 0.715 | 0.677 | 0.706 |
| rougeL | 0.607 | 0.577 | 0.617 | 0.606 | 0.641 |
| srrbert | 0.598 | 0.612 | 0.619 | 0.597 | 0.604 |
| temporal | 0.520 | 0.524 | 0.526 | 0.520 | 0.521 |
| token_f1 | 0.638 | 0.633 | 0.678 | 0.637 | 0.674 |
