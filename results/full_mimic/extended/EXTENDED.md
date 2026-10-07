# Extended analysis — mimic

## A. severity: controlled S0 paired accuracy by subtype

| metric | adjacent | extreme |
|---|---|---|
| bertscore_deberta_mnli | 0.365 | 0.789 |
| bertscore_distilbert | 0.081 | 0.158 |
| bertscore_roberta_large | 0.189 | 0.316 |
| bleu | 0.500 | 0.500 |
| crimson | 0.831 | 0.947 |
| f1chexbert | 0.507 | 0.493 |
| gemma3_27b__rubric | 0.811 | 0.888 |
| gptoss_120b__rubric | 0.946 | 0.954 |
| gptoss_20b__errors | 0.795 | 0.691 |
| gptoss_20b__rubric | 0.912 | 0.928 |
| green | 0.824 | 0.816 |
| jaccard | 0.723 | 0.632 |
| llama31_8b__rubric | 0.635 | 0.803 |
| qwen3_32b__rubric | 0.878 | 0.895 |
| qwen3_32b__rubric_unit | 0.899 | 0.882 |
| qwen3_32b_think__rubric | 0.939 | 0.974 |
| radcliq | 0.284 | 0.342 |
| radgraph | 0.297 | 0.454 |
| ratescore | 0.527 | 0.737 |
| rougeL | 0.764 | 0.678 |
| srrbert | 0.507 | 0.520 |
| temporal | 0.500 | 0.500 |
| token_f1 | 0.764 | 0.678 |

## A. measurement: controlled S0 paired accuracy by subtype

| metric | unit | value |
|---|---|---|
| bertscore_deberta_mnli | 0.293 | 0.693 |
| bertscore_distilbert | 0.000 | 0.747 |
| bertscore_roberta_large | 0.013 | 0.547 |
| bleu | 0.013 | 0.500 |
| crimson | 0.667 | 0.773 |
| f1chexbert | 0.500 | 0.500 |
| gemma3_27b__rubric | 0.693 | 0.740 |
| gptoss_120b__rubric | 0.880 | 0.860 |
| gptoss_20b__errors | 0.967 | 0.986 |
| gptoss_20b__rubric | 0.973 | 0.987 |
| green | 0.840 | 0.800 |
| jaccard | 0.007 | 0.493 |
| llama31_8b__rubric | 0.793 | 0.520 |
| qwen3_32b__rubric | 0.540 | 0.533 |
| qwen3_32b__rubric_unit | 0.587 | 0.653 |
| qwen3_32b_think__rubric | 0.800 | 0.833 |
| radcliq | 0.107 | 0.693 |
| radgraph | 0.393 | 0.487 |
| ratescore | 0.253 | 0.600 |
| rougeL | 0.007 | 0.473 |
| srrbert | 0.493 | 0.500 |
| temporal | 0.500 | 0.500 |
| token_f1 | 0.007 | 0.473 |

## A. negation: controlled S0 paired accuracy by subtype

| metric | negated->present | present->negated |
|---|---|---|
| bertscore_deberta_mnli | 1.000 | 1.000 |
| bertscore_distilbert | 0.772 | 0.630 |
| bertscore_roberta_large | 0.935 | 0.556 |
| bleu | 0.736 | 0.593 |
| crimson | 0.947 | 0.870 |
| f1chexbert | 0.671 | 0.500 |
| gemma3_27b__rubric | 1.000 | 1.000 |
| gptoss_120b__rubric | 0.988 | 1.000 |
| gptoss_20b__errors | 0.984 | 1.000 |
| gptoss_20b__rubric | 0.992 | 1.000 |
| green | 0.947 | 0.944 |
| jaccard | 0.553 | 0.444 |
| llama31_8b__rubric | 0.963 | 0.926 |
| qwen3_32b__rubric | 0.984 | 1.000 |
| qwen3_32b__rubric_unit | 0.984 | 1.000 |
| qwen3_32b_think__rubric | 0.992 | 1.000 |
| radcliq | 0.984 | 0.963 |
| radgraph | 0.813 | 0.889 |
| ratescore | 0.858 | 0.722 |
| rougeL | 0.581 | 0.444 |
| srrbert | 0.947 | 0.870 |
| temporal | 0.602 | 0.500 |
| token_f1 | 0.581 | 0.444 |

## A. uncertainty: controlled S0 paired accuracy by subtype

| metric | definite->hedged | hedged->definite |
|---|---|---|
| bertscore_deberta_mnli | 0.909 | 0.897 |
| bertscore_distilbert | 1.000 | 0.769 |
| bertscore_roberta_large | 0.818 | 0.829 |
| bleu | 0.985 | 0.620 |
| crimson | 0.500 | 0.585 |
| f1chexbert | 0.515 | 0.504 |
| gemma3_27b__rubric | 0.864 | 0.936 |
| gptoss_120b__rubric | 0.909 | 0.957 |
| gptoss_20b__errors | 0.985 | 0.812 |
| gptoss_20b__rubric | 0.985 | 0.927 |
| green | 0.500 | 0.568 |
| jaccard | 0.924 | 0.645 |
| llama31_8b__rubric | 0.576 | 0.585 |
| qwen3_32b__rubric | 0.697 | 0.897 |
| qwen3_32b__rubric_unit | 0.712 | 0.902 |
| qwen3_32b_think__rubric | 0.939 | 0.974 |
| radcliq | 0.848 | 0.786 |
| radgraph | 0.788 | 0.615 |
| ratescore | 0.515 | 0.667 |
| rougeL | 0.530 | 0.521 |
| srrbert | 0.864 | 0.752 |
| temporal | 0.500 | 0.500 |
| token_f1 | 0.985 | 0.620 |

## B. Surface dose-response (S2): extra penalty on the meaning-preserving candidate, z(D(P2) - D(P0)), by amount rewritten

| metric | Q1 (least rewritten) | Q2 | Q3 | Q4 (most rewritten) |
|---|---|---|---|---|
| bertscore_deberta_mnli | 1.25 | 1.88 | 2.21 | 2.43 |
| bertscore_distilbert | 1.29 | 2.02 | 2.33 | 2.62 |
| bertscore_roberta_large | 1.27 | 1.97 | 2.31 | 2.55 |
| bleu | 1.27 | 1.95 | 2.33 | 2.63 |
| crimson | 0.01 | 0.01 | 0.00 | -0.00 |
| f1chexbert | 0.14 | 0.22 | 0.24 | 0.30 |
| gemma3_27b__rubric | -0.32 | -0.40 | -0.43 | -0.38 |
| gptoss_120b__rubric | 0.05 | 0.03 | 0.09 | 0.05 |
| gptoss_20b__errors | 0.11 | 0.14 | 0.10 | 0.13 |
| gptoss_20b__rubric | 0.01 | 0.10 | 0.07 | 0.14 |
| green | 0.43 | 0.64 | 0.61 | 0.69 |
| jaccard | 1.34 | 1.86 | 2.04 | 2.31 |
| llama31_8b__rubric | 0.16 | 0.21 | 0.14 | 0.15 |
| qwen3_32b__rubric | -0.27 | -0.32 | -0.35 | -0.30 |
| qwen3_32b__rubric_unit | -0.26 | -0.23 | -0.42 | -0.30 |
| qwen3_32b_think__rubric | -0.06 | 0.01 | -0.06 | 0.00 |
| radcliq | 1.38 | 1.89 | 2.21 | 2.51 |
| radgraph | 1.26 | 1.66 | 1.87 | 2.16 |
| ratescore | 0.96 | 1.34 | 1.62 | 1.74 |
| rougeL | 0.95 | 1.50 | 1.79 | 2.10 |
| srrbert | 0.41 | 0.60 | 0.57 | 0.60 |
| temporal | 0.60 | 0.75 | 0.79 | 0.74 |
| token_f1 | 1.27 | 1.86 | 2.05 | 2.37 |

### paired accuracy C2 vs P2 by amount rewritten

| metric | Q1 (least rewritten) | Q2 | Q3 | Q4 (most rewritten) |
|---|---|---|---|---|
| bertscore_deberta_mnli | 0.801 | 0.786 | 0.832 | 0.867 |
| bertscore_distilbert | 0.592 | 0.641 | 0.603 | 0.631 |
| bertscore_roberta_large | 0.650 | 0.726 | 0.664 | 0.760 |
| bleu | 0.545 | 0.550 | 0.559 | 0.599 |
| crimson | 0.782 | 0.836 | 0.818 | 0.890 |
| f1chexbert | 0.525 | 0.528 | 0.534 | 0.536 |
| gemma3_27b__rubric | 0.890 | 0.907 | 0.889 | 0.935 |
| gptoss_120b__rubric | 0.955 | 0.962 | 0.956 | 0.971 |
| gptoss_20b__errors | 0.909 | 0.934 | 0.912 | 0.933 |
| gptoss_20b__rubric | 0.935 | 0.945 | 0.952 | 0.949 |
| green | 0.713 | 0.722 | 0.752 | 0.814 |
| jaccard | 0.576 | 0.575 | 0.569 | 0.633 |
| llama31_8b__rubric | 0.695 | 0.698 | 0.725 | 0.743 |
| qwen3_32b__rubric | 0.877 | 0.889 | 0.868 | 0.909 |
| qwen3_32b__rubric_unit | 0.874 | 0.875 | 0.882 | 0.905 |
| qwen3_32b_think__rubric | 0.960 | 0.982 | 0.969 | 0.975 |
| radcliq | 0.668 | 0.677 | 0.672 | 0.730 |
| radgraph | 0.588 | 0.562 | 0.584 | 0.578 |
| ratescore | 0.637 | 0.623 | 0.664 | 0.669 |
| rougeL | 0.529 | 0.512 | 0.502 | 0.565 |
| srrbert | 0.628 | 0.607 | 0.660 | 0.603 |
| temporal | 0.531 | 0.532 | 0.542 | 0.542 |
| token_f1 | 0.588 | 0.579 | 0.582 | 0.658 |

## C. Contrasts (report-cluster bootstrap 95% CI)

| metric | S0 | S2 | S0_minus_S2 | drop_lo | drop_hi | S0_minus_jaccard | vsJ_lo | vsJ_hi | S2_minus_jaccard | vsJ2_lo | vsJ2_hi | beats_blind_baseline_S0 | degrades_under_paraphrase |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bertscore_distilbert | 0.626 | 0.616 | 0.010 | -0.008 | 0.030 | 0.034 | 0.006 | 0.065 | 0.028 | -0.003 | 0.056 | True | False |
| bertscore_roberta_large | 0.660 | 0.699 | -0.039 | -0.059 | -0.019 | 0.069 | 0.038 | 0.100 | 0.111 | 0.082 | 0.138 | True | False |
| bertscore_deberta_mnli | 0.811 | 0.822 | -0.010 | -0.030 | 0.009 | 0.220 | 0.190 | 0.248 | 0.234 | 0.207 | 0.264 | True | False |
| crimson | 0.838 | 0.831 | 0.007 | -0.002 | 0.016 | 0.246 | 0.224 | 0.271 | 0.243 | 0.220 | 0.269 | True | False |
| f1chexbert | 0.526 | 0.531 | -0.005 | -0.010 | 0.000 | -0.065 | -0.087 | -0.041 | -0.057 | -0.081 | -0.033 | False | False |
| green | 0.830 | 0.750 | 0.080 | 0.061 | 0.097 | 0.238 | 0.212 | 0.262 | 0.162 | 0.134 | 0.190 | True | True |
| bleu | 0.570 | 0.563 | 0.007 | -0.003 | 0.016 | -0.021 | -0.036 | -0.005 | -0.025 | -0.041 | -0.006 | False | False |
| rougeL | 0.530 | 0.527 | 0.002 | 0.000 | 0.005 | -0.062 | -0.079 | -0.045 | -0.061 | -0.079 | -0.043 | False | False |
| token_f1 | 0.603 | 0.602 | 0.001 | -0.009 | 0.012 | 0.011 | 0.000 | 0.023 | 0.014 | 0.002 | 0.025 | True | False |
| jaccard | 0.591 | 0.588 | 0.003 | -0.003 | 0.010 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | False | False |
| radcliq | 0.690 | 0.687 | 0.003 | -0.018 | 0.025 | 0.098 | 0.070 | 0.125 | 0.099 | 0.071 | 0.124 | True | False |
| radgraph | 0.573 | 0.579 | -0.005 | -0.029 | 0.020 | -0.018 | -0.042 | 0.010 | -0.010 | -0.037 | 0.018 | False | False |
| ratescore | 0.658 | 0.649 | 0.010 | -0.005 | 0.022 | 0.067 | 0.036 | 0.096 | 0.060 | 0.032 | 0.089 | True | False |
| srrbert | 0.624 | 0.625 | -0.000 | -0.002 | 0.001 | 0.033 | 0.008 | 0.059 | 0.037 | 0.011 | 0.063 | True | False |
| temporal | 0.541 | 0.537 | 0.004 | 0.002 | 0.008 | -0.050 | -0.076 | -0.025 | -0.051 | -0.075 | -0.029 | False | True |
| gemma3_27b__rubric | 0.904 | 0.905 | -0.001 | -0.015 | 0.013 | 0.313 | 0.291 | 0.332 | 0.317 | 0.294 | 0.341 | True | False |
| gptoss_120b__rubric | 0.965 | 0.961 | 0.004 | -0.006 | 0.013 | 0.373 | 0.352 | 0.395 | 0.373 | 0.351 | 0.394 | True | False |
| gptoss_20b__errors | 0.922 | 0.922 | 0.001 | -0.011 | 0.014 | 0.331 | 0.309 | 0.353 | 0.333 | 0.311 | 0.354 | True | False |
| gptoss_20b__rubric | 0.969 | 0.945 | 0.024 | 0.014 | 0.035 | 0.378 | 0.355 | 0.400 | 0.357 | 0.335 | 0.380 | True | True |
| llama31_8b__rubric | 0.741 | 0.715 | 0.026 | 0.013 | 0.042 | 0.150 | 0.124 | 0.177 | 0.127 | 0.102 | 0.154 | True | True |
| qwen3_32b__rubric | 0.869 | 0.886 | -0.017 | -0.034 | -0.003 | 0.277 | 0.256 | 0.299 | 0.298 | 0.274 | 0.322 | True | False |
| qwen3_32b__rubric_unit | 0.880 | 0.884 | -0.003 | -0.020 | 0.014 | 0.289 | 0.268 | 0.309 | 0.296 | 0.271 | 0.321 | True | False |
| qwen3_32b_think__rubric | 0.960 | 0.971 | -0.011 | -0.022 | -0.001 | 0.369 | 0.348 | 0.390 | 0.383 | 0.361 | 0.406 | True | False |

## D. Mixed-effects coefficients (z-scored penalty; random intercept per report)

| metric | C(surface)[T.S1] | C(surface)[T.S2] | meaning | meaning:C(surface)[T.S1] | meaning:C(surface)[T.S2] |
|---|---|---|---|---|---|
| bertscore_deberta_mnli | 1.499 | 1.934 | 0.216 | -0.068 | -0.037 |
| bertscore_distilbert | 1.229 | 2.056 | 0.019 | -0.001 | -0.000 |
| bertscore_roberta_large | 1.344 | 2.017 | 0.048 | -0.004 | -0.000 |
| bleu | 0.234 | 2.037 | 0.007 | -0.002 | -0.003 |
| crimson | 0.029 | 0.008 | 0.873 | -0.003 | -0.038 |
| f1chexbert | 0.100 | 0.224 | 0.190 | 0.003 | 0.030 |
| gemma3_27b__rubric | 0.024 | -0.384 | 1.347 | -0.175 | 0.049 |
| gptoss_120b__rubric | 0.013 | 0.056 | 1.840 | -0.032 | -0.074 |
| gptoss_20b__errors | -0.074 | 0.119 | 1.666 | 0.070 | -0.059 |
| gptoss_20b__rubric | -0.017 | 0.078 | 1.860 | 0.003 | -0.127 |
| green | 0.302 | 0.587 | 1.027 | -0.152 | -0.101 |
| jaccard | 0.000 | 1.878 | 0.048 | 0.000 | -0.013 |
| llama31_8b__rubric | 0.647 | 0.164 | 1.006 | -0.433 | -0.192 |
| qwen3_32b__rubric | -0.181 | -0.309 | 1.404 | -0.063 | -0.010 |
| qwen3_32b__rubric_unit | -0.170 | -0.302 | 1.481 | -0.069 | -0.020 |
| qwen3_32b_think__rubric | -0.024 | -0.028 | 1.827 | -0.000 | -0.002 |
| radcliq | 0.812 | 1.990 | 0.154 | -0.006 | -0.008 |
| radgraph | 0.430 | 1.734 | 0.092 | 0.004 | -0.006 |
| ratescore | 0.101 | 1.410 | 0.105 | -0.003 | 0.004 |
| rougeL | 2.000 | 1.578 | 0.007 | -0.004 | 0.000 |
| srrbert | 0.020 | 0.542 | 0.540 | 0.002 | -0.034 |
| temporal | -0.000 | 0.719 | 0.078 | -0.000 | -0.023 |
| token_f1 | 0.000 | 1.879 | 0.045 | 0.000 | -0.003 |

## E. CRIMSON error attribution — share of candidates with >=1 error (any / expected category / only other categories)

| cell | edit_type | n | any_error | expected_category_fired | only_other_category |
|---|---|---|---|---|---|
| P0 | anatomy | 150 | 0.093 | 0.087 | 0.007 |
| P0 | laterality | 150 | 0.013 | 0.013 | 0.000 |
| P0 | measurement | 150 | 0.700 | 0.693 | 0.007 |
| P0 | negation | 150 | 0.007 | 0.000 | 0.007 |
| P0 | severity | 150 | 0.540 | 0.540 | 0.000 |
| P0 | temporal | 150 | 0.053 | 0.053 | 0.000 |
| P0 | uncertainty | 150 | 0.487 | 0.480 | 0.007 |
| C0 | anatomy | 150 | 0.967 | 0.967 | 0.000 |
| C0 | laterality | 150 | 0.927 | 0.927 | 0.000 |
| C0 | measurement | 150 | 0.847 | 0.827 | 0.020 |
| C0 | negation | 150 | 0.907 | 0.860 | 0.047 |
| C0 | severity | 150 | 1.000 | 0.993 | 0.007 |
| C0 | temporal | 150 | 0.840 | 0.647 | 0.193 |
| C0 | uncertainty | 150 | 0.920 | 0.907 | 0.013 |

### C0: which category fires (share of candidates)

| edit_type | false_findings | missing_findings | location_errors | severity_errors | descriptor_errors | measurement_errors | certainty_errors | unspecific_errors | overinterpretation_errors | temporal_errors |
|---|---|---|---|---|---|---|---|---|---|---|
| anatomy | 0.00 | 0.00 | 0.97 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 |
| laterality | 0.00 | 0.00 | 0.93 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| measurement | 0.00 | 0.02 | 0.00 | 0.01 | 0.00 | 0.83 | 0.00 | 0.01 | 0.01 | 0.01 |
| negation | 0.73 | 0.14 | 0.01 | 0.03 | 0.01 | 0.00 | 0.01 | 0.01 | 0.00 | 0.01 |
| severity | 0.00 | 0.00 | 0.01 | 0.99 | 0.01 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 |
| temporal | 0.15 | 0.01 | 0.00 | 0.01 | 0.03 | 0.00 | 0.00 | 0.00 | 0.00 | 0.65 |
| uncertainty | 0.00 | 0.01 | 0.00 | 0.01 | 0.00 | 0.00 | 0.91 | 0.01 | 0.01 | 0.00 |

## F. Robustness: controlled S0 paired accuracy on target subsets

| metric | all targets (n=1050) | excl. P lexicon pending expert review (n=854) | excl. all three (n=773) | excl. awkward negation fragments (n=1044) | excl. measurement:unit (P edit larger than C) (n=975) |
|---|---|---|---|---|---|
| bertscore_deberta_mnli | 0.811 | 0.847 | 0.899 | 0.810 | 0.851 |
| bertscore_distilbert | 0.626 | 0.666 | 0.730 | 0.625 | 0.674 |
| bertscore_roberta_large | 0.660 | 0.708 | 0.774 | 0.658 | 0.710 |
| bleu | 0.570 | 0.582 | 0.635 | 0.568 | 0.613 |
| crimson | 0.838 | 0.840 | 0.856 | 0.837 | 0.851 |
| f1chexbert | 0.526 | 0.531 | 0.534 | 0.526 | 0.528 |
| gemma3_27b__rubric | 0.904 | 0.910 | 0.930 | 0.904 | 0.921 |
| gptoss_120b__rubric | 0.965 | 0.965 | 0.973 | 0.965 | 0.971 |
| gptoss_20b__errors | 0.922 | 0.941 | 0.938 | 0.922 | 0.919 |
| gptoss_20b__rubric | 0.969 | 0.972 | 0.972 | 0.969 | 0.969 |
| green | 0.830 | 0.835 | 0.835 | 0.830 | 0.829 |
| jaccard | 0.591 | 0.570 | 0.625 | 0.591 | 0.636 |
| llama31_8b__rubric | 0.741 | 0.753 | 0.747 | 0.740 | 0.737 |
| qwen3_32b__rubric | 0.869 | 0.869 | 0.902 | 0.869 | 0.894 |
| qwen3_32b__rubric_unit | 0.880 | 0.882 | 0.911 | 0.881 | 0.903 |
| qwen3_32b_think__rubric | 0.960 | 0.958 | 0.973 | 0.960 | 0.973 |
| radcliq | 0.690 | 0.715 | 0.772 | 0.688 | 0.734 |
| radgraph | 0.573 | 0.609 | 0.627 | 0.571 | 0.587 |
| ratescore | 0.658 | 0.667 | 0.706 | 0.657 | 0.689 |
| rougeL | 0.530 | 0.502 | 0.547 | 0.527 | 0.570 |
| srrbert | 0.624 | 0.629 | 0.641 | 0.623 | 0.634 |
| temporal | 0.541 | 0.550 | 0.556 | 0.541 | 0.544 |
| token_f1 | 0.603 | 0.584 | 0.637 | 0.601 | 0.649 |
