# 10/7 review re-analysis — mimic

## A. Ctrl-0: win / tie / loss

| metric | win | tie | loss | paired_acc | win_among_decided |
|---|---|---|---|---|---|
| bertscore_distilbert | 0.626 | 0.000 | 0.374 | 0.626 | 0.626 |
| bertscore_roberta_large | 0.660 | 0.000 | 0.340 | 0.660 | 0.660 |
| bertscore_deberta_mnli | 0.811 | 0.000 | 0.189 | 0.811 | 0.811 |
| crimson | 0.680 | 0.315 | 0.005 | 0.838 | 0.993 |
| f1chexbert | 0.056 | 0.940 | 0.004 | 0.526 | 0.937 |
| green | 0.671 | 0.316 | 0.012 | 0.830 | 0.982 |
| bleu | 0.253 | 0.633 | 0.113 | 0.570 | 0.691 |
| rougeL | 0.206 | 0.648 | 0.147 | 0.530 | 0.584 |
| token_f1 | 0.338 | 0.530 | 0.132 | 0.603 | 0.719 |
| jaccard | 0.339 | 0.505 | 0.156 | 0.591 | 0.685 |
| radcliq | 0.690 | 0.000 | 0.310 | 0.690 | 0.690 |
| radgraph | 0.333 | 0.480 | 0.187 | 0.573 | 0.641 |
| ratescore | 0.564 | 0.189 | 0.248 | 0.658 | 0.695 |
| srrbert | 0.260 | 0.729 | 0.011 | 0.624 | 0.958 |
| temporal | 0.095 | 0.891 | 0.013 | 0.541 | 0.877 |
| gemma3_27b__rubric | 0.817 | 0.174 | 0.009 | 0.904 | 0.990 |
| gptoss_120b__rubric | 0.930 | 0.069 | 0.001 | 0.965 | 0.999 |
| gptoss_20b__errors | 0.845 | 0.155 | 0.000 | 0.922 | 1.000 |
| gptoss_20b__rubric | 0.942 | 0.054 | 0.004 | 0.969 | 0.996 |
| llama31_8b__rubric | 0.498 | 0.487 | 0.015 | 0.741 | 0.970 |
| qwen3_32b__rubric | 0.751 | 0.234 | 0.014 | 0.869 | 0.981 |
| qwen3_32b__rubric_unit | 0.777 | 0.207 | 0.016 | 0.880 | 0.980 |
| qwen3_32b_think__rubric | 0.930 | 0.060 | 0.010 | 0.960 | 0.990 |

## B. Strict-matched subset (P0 and C0 exactly tied on Jaccard and token F1): n=486 of 1050; by type {'temporal': 128, 'anatomy': 97, 'severity': 69, 'measurement': 61, 'laterality': 50, 'uncertainty': 44, 'negation': 37}

| metric | n_strict | Ctrl-0 all | Ctrl-0 strict | Ctrl-2 all | Ctrl-2 strict | tie_strict |
|---|---|---|---|---|---|---|
| bertscore_distilbert | 486 | 0.626 | 0.652 | 0.616 | 0.628 | 0.000 |
| bertscore_roberta_large | 486 | 0.660 | 0.673 | 0.699 | 0.687 | 0.000 |
| bertscore_deberta_mnli | 486 | 0.811 | 0.850 | 0.822 | 0.835 | 0.000 |
| crimson | 486 | 0.838 | 0.852 | 0.831 | 0.840 | 0.288 |
| f1chexbert | 486 | 0.526 | 0.520 | 0.531 | 0.519 | 0.961 |
| green | 486 | 0.830 | 0.821 | 0.750 | 0.729 | 0.337 |
| bleu | 486 | 0.570 | 0.503 | 0.563 | 0.499 | 0.977 |
| rougeL | 486 | 0.530 | 0.500 | 0.527 | 0.498 | 1.000 |
| token_f1 | 486 | 0.603 | 0.500 | 0.602 | 0.499 | 1.000 |
| jaccard | 486 | 0.591 | 0.500 | 0.588 | 0.501 | 1.000 |
| radcliq | 486 | 0.690 | 0.665 | 0.687 | 0.648 | 0.000 |
| radgraph | 486 | 0.573 | 0.537 | 0.579 | 0.513 | 0.588 |
| ratescore | 486 | 0.658 | 0.645 | 0.649 | 0.639 | 0.105 |
| srrbert | 486 | 0.624 | 0.601 | 0.625 | 0.601 | 0.774 |
| temporal | 486 | 0.541 | 0.570 | 0.537 | 0.568 | 0.815 |
| gemma3_27b__rubric | 486 | 0.904 | 0.894 | 0.905 | 0.894 | 0.200 |
| gptoss_120b__rubric | 486 | 0.965 | 0.966 | 0.961 | 0.963 | 0.064 |
| gptoss_20b__errors | 486 | 0.922 | 0.883 | 0.922 | 0.899 | 0.233 |
| gptoss_20b__rubric | 486 | 0.969 | 0.954 | 0.945 | 0.948 | 0.076 |
| llama31_8b__rubric | 486 | 0.741 | 0.698 | 0.715 | 0.697 | 0.556 |
| qwen3_32b__rubric | 486 | 0.869 | 0.856 | 0.886 | 0.896 | 0.235 |
| qwen3_32b__rubric_unit | 486 | 0.880 | 0.870 | 0.884 | 0.893 | 0.202 |
| qwen3_32b_think__rubric | 486 | 0.960 | 0.965 | 0.971 | 0.976 | 0.053 |

## C. Exchange rate: one context paraphrase / one reordering, in units of one matched meaning change

| metric | paraphrase_in_meaning_changes | reorder_in_meaning_changes |
|---|---|---|
| bertscore_distilbert | 109.01 | 65.16 |
| bertscore_roberta_large | 41.76 | 27.82 |
| bertscore_deberta_mnli | 8.97 | 6.95 |
| crimson | 0.01 | 0.03 |
| f1chexbert | 1.17 | 0.52 |
| green | 0.57 | 0.29 |
| bleu | 284.30 | 32.62 |
| rougeL | 234.98 | 297.85 |
| token_f1 | 41.74 | 0.00 |
| jaccard | 39.10 | 0.00 |
| radcliq | 12.94 | 5.28 |
| radgraph | 18.79 | 4.66 |
| ratescore | 13.38 | 0.96 |
| srrbert | 1.00 | 0.04 |
| temporal | 9.24 | 0.00 |
| gemma3_27b__rubric | -0.29 | 0.02 |
| gptoss_120b__rubric | 0.03 | 0.01 |
| gptoss_20b__errors | 0.07 | -0.04 |
| gptoss_20b__rubric | 0.04 | -0.01 |
| llama31_8b__rubric | 0.16 | 0.64 |
| qwen3_32b__rubric | -0.22 | -0.13 |
| qwen3_32b__rubric_unit | -0.20 | -0.11 |
| qwen3_32b_think__rubric | -0.02 | -0.01 |

## D. S2 subset whose paraphrased context keeps all degree words: n=792 of 1050

| metric | n | Ctrl-0 | Ctrl-2 | Conf-P | drop(all) | drop(degree-preserving) |
|---|---|---|---|---|---|---|
| bertscore_distilbert | 792 | 0.616 | 0.610 | 0.006 | 0.010 | 0.006 |
| bertscore_roberta_large | 792 | 0.649 | 0.699 | 0.006 | -0.039 | -0.051 |
| bertscore_deberta_mnli | 792 | 0.801 | 0.811 | 0.025 | -0.010 | -0.010 |
| crimson | 792 | 0.841 | 0.834 | 0.836 | 0.007 | 0.007 |
| f1chexbert | 792 | 0.526 | 0.530 | 0.494 | -0.005 | -0.004 |
| green | 792 | 0.832 | 0.759 | 0.665 | 0.080 | 0.073 |
| bleu | 792 | 0.568 | 0.562 | 0.005 | 0.007 | 0.005 |
| rougeL | 792 | 0.526 | 0.524 | 0.004 | 0.002 | 0.002 |
| token_f1 | 792 | 0.599 | 0.598 | 0.009 | 0.001 | 0.001 |
| jaccard | 792 | 0.591 | 0.586 | 0.010 | 0.003 | 0.005 |
| radcliq | 792 | 0.689 | 0.689 | 0.024 | 0.003 | 0.000 |
| radgraph | 792 | 0.570 | 0.576 | 0.046 | -0.005 | -0.006 |
| ratescore | 792 | 0.652 | 0.640 | 0.102 | 0.010 | 0.012 |
| srrbert | 792 | 0.628 | 0.629 | 0.478 | -0.000 | -0.001 |
| temporal | 792 | 0.545 | 0.543 | 0.371 | 0.004 | 0.002 |
| gemma3_27b__rubric | 792 | 0.907 | 0.905 | 0.968 | -0.001 | 0.002 |
| gptoss_120b__rubric | 792 | 0.962 | 0.963 | 0.966 | 0.004 | -0.001 |
| gptoss_20b__errors | 792 | 0.924 | 0.923 | 0.901 | 0.001 | 0.001 |
| gptoss_20b__rubric | 792 | 0.966 | 0.953 | 0.965 | 0.024 | 0.013 |
| llama31_8b__rubric | 792 | 0.747 | 0.718 | 0.728 | 0.026 | 0.030 |
| qwen3_32b__rubric | 792 | 0.872 | 0.888 | 0.953 | -0.017 | -0.016 |
| qwen3_32b__rubric_unit | 792 | 0.882 | 0.886 | 0.947 | -0.003 | -0.004 |
| qwen3_32b_think__rubric | 792 | 0.960 | 0.972 | 0.980 | -0.011 | -0.012 |

## E. Uncertainty without the 'consistent with / suspicious for / suggestive of' family; D-10 '-sided sided' targets: 0

| metric | uncertainty all (n=150) | uncertainty w/o consistent-with family (n=108) |
|---|---|---|
| bertscore_distilbert | 0.820 | 0.815 |
| bertscore_roberta_large | 0.827 | 0.870 |
| bertscore_deberta_mnli | 0.900 | 0.926 |
| crimson | 0.567 | 0.569 |
| f1chexbert | 0.507 | 0.509 |
| green | 0.553 | 0.569 |
| bleu | 0.700 | 0.662 |
| rougeL | 0.523 | 0.343 |
| token_f1 | 0.700 | 0.662 |
| jaccard | 0.707 | 0.639 |
| radcliq | 0.800 | 0.824 |
| radgraph | 0.653 | 0.681 |
| ratescore | 0.633 | 0.681 |
| srrbert | 0.777 | 0.769 |
| temporal | 0.500 | 0.500 |
| gemma3_27b__rubric | 0.920 | 0.926 |
| gptoss_120b__rubric | 0.947 | 0.963 |
| gptoss_20b__errors | 0.850 | 0.815 |
| gptoss_20b__rubric | 0.940 | 0.949 |
| llama31_8b__rubric | 0.583 | 0.588 |
| qwen3_32b__rubric | 0.853 | 0.880 |
| qwen3_32b__rubric_unit | 0.860 | 0.894 |
| qwen3_32b_think__rubric | 0.967 | 0.995 |

## F. Interaction (meaning x S2) and (meaning x S1) from decomposition.csv

| metric | meaning_effect_S0 | surface_S1 | surface_S2 | interaction_S1 | interaction_S2 |
|---|---|---|---|---|---|
| bertscore_distilbert | 0.019 | 1.229 | 2.056 | -0.001 | -0.000 |
| bertscore_roberta_large | 0.048 | 1.344 | 2.017 | -0.004 | -0.000 |
| bertscore_deberta_mnli | 0.216 | 1.499 | 1.934 | -0.068 | -0.037 |
| crimson | 0.873 | 0.029 | 0.008 | -0.008 | -0.038 |
| f1chexbert | 0.190 | 0.100 | 0.224 | 0.003 | 0.030 |
| green | 1.027 | 0.302 | 0.588 | -0.152 | -0.101 |
| bleu | 0.007 | 0.234 | 2.037 | -0.002 | -0.003 |
| rougeL | 0.007 | 2.000 | 1.578 | -0.004 | 0.000 |
| token_f1 | 0.045 | 0.000 | 1.879 | 0.000 | -0.003 |
| jaccard | 0.048 | 0.000 | 1.878 | 0.000 | -0.013 |
| radcliq | 0.154 | 0.812 | 1.990 | -0.006 | -0.008 |
| radgraph | 0.092 | 0.431 | 1.734 | 0.004 | -0.006 |
| ratescore | 0.105 | 0.101 | 1.410 | -0.003 | 0.004 |
| srrbert | 0.540 | 0.020 | 0.542 | 0.002 | -0.034 |
| temporal | 0.078 | 0.000 | 0.719 | 0.000 | -0.023 |
| gemma3_27b__rubric | 1.347 | 0.024 | -0.384 | -0.175 | 0.049 |
| gptoss_120b__rubric | 1.841 | 0.013 | 0.056 | -0.032 | -0.074 |
| gptoss_20b__errors | 1.666 | -0.072 | 0.122 | 0.072 | -0.056 |
| gptoss_20b__rubric | 1.861 | -0.017 | 0.078 | 0.003 | -0.127 |
| llama31_8b__rubric | 1.006 | 0.647 | 0.164 | -0.433 | -0.192 |
| qwen3_32b__rubric | 1.404 | -0.181 | -0.309 | -0.064 | -0.010 |
| qwen3_32b__rubric_unit | 1.481 | -0.170 | -0.302 | -0.069 | -0.020 |
| qwen3_32b_think__rubric | 1.828 | -0.024 | -0.028 | -0.000 | -0.002 |

### judges: CHANGED rate on uncertainty, C0 vs C2

| judge | C0 | C2 | P0 |
|---|---|---|---|
| gemma3_27b__rubric | 0.76 | 0.39 | 0.04 |
| gptoss_120b__rubric | 0.93 | 0.90 | 0.05 |
| gptoss_20b__errors | 0.99 | 0.92 | 0.29 |
| gptoss_20b__rubric | 0.96 | 0.79 | 0.11 |
| llama31_8b__rubric | 0.25 | 0.40 | 0.07 |
| qwen3_32b__rubric | 0.70 | 0.37 | 0.01 |
| qwen3_32b__rubric_unit | 0.71 | 0.38 | 0.01 |
| qwen3_32b_think__rubric | 0.89 | 0.87 | 0.00 |
