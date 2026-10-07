# Factorial analysis — data/pairs/full_mimicoi_all.csv

## Paired accuracy by condition

| metric | confound_reevalmed | confound_v1 | controlled_S0 | controlled_S1 | controlled_S2 |
|---|---|---|---|---|---|
| bertscore_deberta_mnli | 0.023 | 0.047 | 0.410 | 0.423 | 0.387 |
| bertscore_distilbert | 0.003 | 0.080 | 0.617 | 0.720 | 0.663 |
| bertscore_roberta_large | 0.007 | 0.080 | 0.553 | 0.723 | 0.643 |
| bleu | 0.003 | 0.183 | 0.578 | 0.587 | 0.638 |
| crimson | 0.925 | 0.943 | 0.937 | 0.948 | 0.937 |
| f1chexbert | 0.780 | 0.787 | 0.797 | 0.787 | 0.788 |
| gemma3_27b__rubric | 0.832 | 0.855 | 0.880 | 0.747 | 0.847 |
| gptoss_120b__rubric | 0.940 | 0.942 | 0.918 | 0.947 | 0.943 |
| gptoss_20b__rubric | 0.962 | 0.958 | 0.947 | 0.955 | 0.955 |
| green | 0.780 | 0.927 | 0.938 | 0.918 | 0.847 |
| jaccard | 0.030 | 0.832 | 0.832 | 0.832 | 0.833 |
| llama31_8b__rubric | 0.640 | 0.565 | 0.690 | 0.732 | 0.695 |
| qwen3_32b__rubric | 0.980 | 0.977 | 0.862 | 0.710 | 0.842 |
| radcliq | 0.080 | 0.543 | 0.950 | 0.967 | 0.970 |
| radgraph | 0.080 | 0.580 | 0.680 | 0.768 | 0.763 |
| ratescore | 0.217 | 0.915 | 0.925 | 0.925 | 0.935 |
| rougeL | 0.003 | 0.013 | 0.625 | 0.518 | 0.637 |
| srrbert | 0.715 | 0.927 | 0.932 | 0.928 | 0.928 |
| temporal | 0.357 | 0.572 | 0.572 | 0.572 | 0.588 |
| token_f1 | 0.013 | 0.625 | 0.625 | 0.625 | 0.652 |

## AUROC by condition

| metric | confound_reevalmed | confound_v1 | controlled_S0 | controlled_S1 | controlled_S2 |
|---|---|---|---|---|---|
| bertscore_deberta_mnli | 0.014 | 0.070 | 0.464 | 0.445 | 0.438 |
| bertscore_distilbert | 0.005 | 0.100 | 0.540 | 0.621 | 0.553 |
| bertscore_roberta_large | 0.008 | 0.074 | 0.508 | 0.655 | 0.556 |
| bleu | 0.000 | 0.324 | 0.568 | 0.570 | 0.555 |
| crimson | 0.930 | 0.942 | 0.943 | 0.949 | 0.933 |
| f1chexbert | 0.780 | 0.786 | 0.796 | 0.785 | 0.783 |
| gemma3_27b__rubric | 0.807 | 0.839 | 0.873 | 0.727 | 0.781 |
| gptoss_120b__rubric | 0.936 | 0.941 | 0.912 | 0.947 | 0.941 |
| gptoss_20b__rubric | 0.961 | 0.964 | 0.951 | 0.958 | 0.953 |
| green | 0.773 | 0.933 | 0.948 | 0.922 | 0.818 |
| jaccard | 0.031 | 0.797 | 0.797 | 0.797 | 0.644 |
| llama31_8b__rubric | 0.646 | 0.573 | 0.690 | 0.736 | 0.696 |
| qwen3_32b__rubric | 0.978 | 0.975 | 0.857 | 0.705 | 0.827 |
| radcliq | 0.060 | 0.564 | 0.918 | 0.884 | 0.783 |
| radgraph | 0.068 | 0.569 | 0.677 | 0.680 | 0.602 |
| ratescore | 0.249 | 0.905 | 0.915 | 0.908 | 0.725 |
| rougeL | 0.001 | 0.014 | 0.646 | 0.521 | 0.582 |
| srrbert | 0.738 | 0.931 | 0.933 | 0.929 | 0.814 |
| temporal | 0.358 | 0.572 | 0.572 | 0.572 | 0.556 |
| token_f1 | 0.012 | 0.646 | 0.646 | 0.646 | 0.593 |

## Decomposition (z-scored penalties)

| metric | sd_D | meaning_effect_S0 | surface_S1 | surface_S2 | meaning_effect_S2 | interaction_S2 | meaning_effect_S1 |
|---|---|---|---|---|---|---|---|
| bertscore_distilbert | 0.061 | 0.076 | 0.842 | 2.093 | 0.128 | 0.052 | 0.188 |
| bertscore_roberta_large | 0.105 | 0.043 | 1.007 | 2.043 | 0.119 | 0.076 | 0.283 |
| bertscore_deberta_mnli | 0.049 | -0.227 | 1.024 | 1.769 | -0.184 | 0.043 | -0.138 |
| crimson | 0.327 | 1.276 | -0.001 | 0.037 | 1.248 | -0.029 | 1.307 |
| f1chexbert | 0.108 | 1.181 | 0.037 | 0.061 | 1.174 | -0.006 | 1.144 |
| green | 0.113 | 1.445 | 0.046 | 0.530 | 1.272 | -0.174 | 1.383 |
| bleu | 0.245 | 0.062 | 0.213 | 2.097 | 0.075 | 0.012 | 0.069 |
| rougeL | 0.181 | 0.105 | 1.899 | 1.814 | 0.123 | 0.019 | 0.060 |
| token_f1 | 0.107 | 0.177 | 0.000 | 1.854 | 0.208 | 0.031 | 0.177 |
| jaccard | 0.156 | 0.428 | 0.000 | 1.890 | 0.300 | -0.127 | 0.428 |
| radcliq | 0.434 | 0.620 | 0.487 | 1.874 | 0.697 | 0.077 | 0.671 |
| radgraph | 0.157 | 0.182 | 0.173 | 1.526 | 0.307 | 0.125 | 0.311 |
| ratescore | 0.087 | 0.684 | 0.015 | 1.331 | 0.794 | 0.110 | 0.682 |
| srrbert | 0.157 | 1.288 | 0.009 | 0.579 | 1.215 | -0.073 | 1.281 |
| temporal | 0.294 | 0.261 | 0.000 | 0.828 | 0.291 | 0.030 | 0.261 |
| gemma3_27b__rubric | 0.456 | 1.541 | 0.300 | 0.113 | 0.740 | -0.800 | 0.843 |
| gptoss_120b__rubric | 0.443 | 1.636 | -0.146 | -0.065 | 1.713 | 0.076 | 1.795 |
| gptoss_20b__rubric | 0.450 | 1.798 | -0.054 | 0.029 | 1.735 | -0.063 | 1.831 |
| llama31_8b__rubric | 0.380 | 0.874 | 0.502 | 0.209 | 0.825 | -0.049 | 0.931 |
| qwen3_32b__rubric | 0.450 | 1.306 | -0.606 | -0.587 | 1.095 | -0.210 | 0.806 |

## Per-type paired accuracy — controlled_S0

| metric | insertion | omission |
|---|---|---|
| bertscore_deberta_mnli | 0.040 | 0.780 |
| bertscore_distilbert | 0.793 | 0.440 |
| bertscore_roberta_large | 0.647 | 0.460 |
| bleu | 0.477 | 0.680 |
| crimson | 0.900 | 0.973 |
| f1chexbert | 0.757 | 0.837 |
| gemma3_27b__rubric | 0.977 | 0.783 |
| gptoss_120b__rubric | 0.987 | 0.850 |
| gptoss_20b__rubric | 0.973 | 0.920 |
| green | 0.900 | 0.977 |
| jaccard | 0.993 | 0.670 |
| llama31_8b__rubric | 0.630 | 0.750 |
| qwen3_32b__rubric | 0.830 | 0.893 |
| radcliq | 0.960 | 0.940 |
| radgraph | 0.847 | 0.513 |
| ratescore | 0.920 | 0.930 |
| rougeL | 0.503 | 0.747 |
| srrbert | 0.957 | 0.907 |
| temporal | 0.513 | 0.630 |
| token_f1 | 0.503 | 0.747 |

## Per-type paired accuracy — controlled_S1

| metric | insertion | omission |
|---|---|---|
| bertscore_deberta_mnli | 0.087 | 0.760 |
| bertscore_distilbert | 0.807 | 0.633 |
| bertscore_roberta_large | 0.620 | 0.827 |
| bleu | 0.453 | 0.720 |
| crimson | 0.920 | 0.977 |
| f1chexbert | 0.743 | 0.830 |
| gemma3_27b__rubric | 0.863 | 0.630 |
| gptoss_120b__rubric | 0.990 | 0.903 |
| gptoss_20b__rubric | 0.960 | 0.950 |
| green | 0.947 | 0.890 |
| jaccard | 0.993 | 0.670 |
| llama31_8b__rubric | 0.727 | 0.737 |
| qwen3_32b__rubric | 0.850 | 0.570 |
| radcliq | 0.947 | 0.987 |
| radgraph | 0.887 | 0.650 |
| ratescore | 0.920 | 0.930 |
| rougeL | 0.547 | 0.490 |
| srrbert | 0.953 | 0.903 |
| temporal | 0.513 | 0.630 |
| token_f1 | 0.503 | 0.747 |

## Per-type paired accuracy — controlled_S2

| metric | insertion | omission |
|---|---|---|
| bertscore_deberta_mnli | 0.040 | 0.733 |
| bertscore_distilbert | 0.713 | 0.613 |
| bertscore_roberta_large | 0.680 | 0.607 |
| bleu | 0.517 | 0.760 |
| crimson | 0.910 | 0.963 |
| f1chexbert | 0.737 | 0.840 |
| gemma3_27b__rubric | 0.910 | 0.783 |
| gptoss_120b__rubric | 0.973 | 0.913 |
| gptoss_20b__rubric | 0.947 | 0.963 |
| green | 0.887 | 0.807 |
| jaccard | 0.980 | 0.687 |
| llama31_8b__rubric | 0.737 | 0.653 |
| qwen3_32b__rubric | 0.947 | 0.737 |
| radcliq | 0.960 | 0.980 |
| radgraph | 0.860 | 0.667 |
| ratescore | 0.953 | 0.917 |
| rougeL | 0.543 | 0.730 |
| srrbert | 0.963 | 0.893 |
| temporal | 0.533 | 0.643 |
| token_f1 | 0.527 | 0.777 |

## Per-type paired accuracy — confound_v1

| metric | insertion | omission |
|---|---|---|
| bertscore_deberta_mnli | 0.000 | 0.093 |
| bertscore_distilbert | 0.053 | 0.107 |
| bertscore_roberta_large | 0.020 | 0.140 |
| bleu | 0.013 | 0.353 |
| crimson | 0.917 | 0.970 |
| f1chexbert | 0.743 | 0.830 |
| gemma3_27b__rubric | 0.977 | 0.733 |
| gptoss_120b__rubric | 0.993 | 0.890 |
| gptoss_20b__rubric | 0.967 | 0.950 |
| green | 0.950 | 0.903 |
| jaccard | 0.993 | 0.670 |
| llama31_8b__rubric | 0.500 | 0.630 |
| qwen3_32b__rubric | 0.977 | 0.977 |
| radcliq | 0.380 | 0.707 |
| radgraph | 0.630 | 0.530 |
| ratescore | 0.907 | 0.923 |
| rougeL | 0.013 | 0.013 |
| srrbert | 0.950 | 0.903 |
| temporal | 0.513 | 0.630 |
| token_f1 | 0.503 | 0.747 |

## Per-type paired accuracy — confound_reevalmed

| metric | insertion | omission |
|---|---|---|
| bertscore_deberta_mnli | 0.000 | 0.047 |
| bertscore_distilbert | 0.007 | 0.000 |
| bertscore_roberta_large | 0.000 | 0.013 |
| bleu | 0.000 | 0.007 |
| crimson | 0.887 | 0.963 |
| f1chexbert | 0.720 | 0.840 |
| gemma3_27b__rubric | 0.983 | 0.680 |
| gptoss_120b__rubric | 0.973 | 0.907 |
| gptoss_20b__rubric | 0.960 | 0.963 |
| green | 0.810 | 0.750 |
| jaccard | 0.040 | 0.020 |
| llama31_8b__rubric | 0.560 | 0.720 |
| qwen3_32b__rubric | 0.987 | 0.973 |
| radcliq | 0.007 | 0.153 |
| radgraph | 0.047 | 0.113 |
| ratescore | 0.173 | 0.260 |
| rougeL | 0.000 | 0.007 |
| srrbert | 0.717 | 0.713 |
| temporal | 0.297 | 0.417 |
| token_f1 | 0.007 | 0.020 |
