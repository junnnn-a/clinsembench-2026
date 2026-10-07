# LLM judges — rate of CHANGED verdicts per cell

P cells and identity should be 0 (false alarms); C cells should be 1 (detections).

| judge | identity | P0 | P1 | P2 | C0 | C1 | C2 |
|---|---|---|---|---|---|---|---|
| gemma3_27b__errors | 0.000 | 0.896 | 0.961 | 0.987 | 0.999 | 1.000 | 1.000 |
| gemma3_27b__rubric | 0.000 | 0.215 | 0.240 | 0.087 | 0.930 | 0.900 | 0.837 |
| gptoss_120b__errors | 0.000 | 0.048 | 0.064 | 0.081 | 0.987 | 0.976 | 0.979 |
| gptoss_120b__rubric | 0.000 | 0.057 | 0.071 | 0.073 | 0.970 | 0.960 | 0.970 |
| gptoss_20b__errors | 0.000 | 0.115 | 0.099 | 0.161 | 0.981 | 0.985 | 0.974 |
| gptoss_20b__rubric | 0.000 | 0.030 | 0.026 | 0.065 | 0.958 | 0.960 | 0.949 |
| llama31_8b__rubric | 0.004 | 0.169 | 0.575 | 0.251 | 0.693 | 0.876 | 0.713 |
| llama31_8b__rubric_unit | 0.000 | 0.098 | 0.421 | 0.126 | 0.592 | 0.806 | 0.580 |
| qwen3_32b__errors | 0.000 | 0.204 | 0.231 | 0.244 | 0.963 | 0.938 | 0.947 |
| qwen3_32b__rubric | 0.000 | 0.108 | 0.063 | 0.022 | 0.930 | 0.855 | 0.833 |
| qwen3_32b__rubric_unit | 0.000 | 0.087 | 0.047 | 0.016 | 0.918 | 0.836 | 0.827 |
| qwen3_32b_think__rubric | 0.000 | 0.027 | 0.020 | 0.030 | 0.958 | 0.955 | 0.952 |

## P0 by edit type (false-alarm rate)

| judge | anatomy | laterality | measurement | negation | severity | temporal | uncertainty |
|---|---|---|---|---|---|---|---|
| gemma3_27b__errors | 0.76 | 0.91 | 1.00 | 0.78 | 0.98 | 1.00 | 0.84 |
| gemma3_27b__rubric | 0.15 | 0.01 | 0.87 | 0.02 | 0.34 | 0.21 | 0.04 |
| gptoss_120b__errors | 0.01 | 0.00 | 0.03 | 0.03 | 0.20 | 0.00 | 0.06 |
| gptoss_120b__rubric | 0.00 | 0.00 | 0.41 | 0.03 | 0.06 | 0.00 | 0.01 |
| gptoss_20b__errors | 0.11 | 0.00 | 0.01 | 0.03 | 0.47 | 0.00 | 0.18 |
| gptoss_20b__rubric | 0.01 | 0.00 | 0.01 | 0.03 | 0.12 | 0.00 | 0.05 |
| llama31_8b__rubric | 0.15 | 0.06 | 0.84 | 0.10 | 0.14 | 0.04 | 0.03 |
| llama31_8b__rubric_unit | 0.09 | 0.01 | 0.54 | 0.05 | 0.07 | 0.02 | 0.02 |
| qwen3_32b__errors | 0.16 | 0.02 | 0.37 | 0.09 | 0.39 | 0.31 | 0.10 |
| qwen3_32b__rubric | 0.13 | 0.01 | 0.27 | 0.06 | 0.20 | 0.10 | 0.01 |
| qwen3_32b__rubric_unit | 0.14 | 0.01 | 0.14 | 0.06 | 0.15 | 0.08 | 0.01 |
| qwen3_32b_think__rubric | 0.01 | 0.00 | 0.13 | 0.03 | 0.04 | 0.00 | 0.00 |

## P1 by edit type (false-alarm rate)

| judge | anatomy | laterality | measurement | negation | severity | temporal | uncertainty |
|---|---|---|---|---|---|---|---|
| gemma3_27b__errors | 0.95 | 0.94 | 1.00 | 0.96 | 0.96 | 1.00 | 0.91 |
| gemma3_27b__rubric | 0.21 | 0.13 | 0.85 | 0.09 | 0.27 | 0.15 | 0.13 |
| gptoss_120b__errors | 0.05 | 0.03 | 0.06 | 0.03 | 0.20 | 0.01 | 0.07 |
| gptoss_120b__rubric | 0.01 | 0.01 | 0.31 | 0.03 | 0.17 | 0.01 | 0.04 |
| gptoss_20b__errors | 0.07 | 0.02 | 0.03 | 0.03 | 0.44 | 0.00 | 0.09 |
| gptoss_20b__rubric | 0.01 | 0.00 | 0.02 | 0.02 | 0.10 | 0.01 | 0.03 |
| llama31_8b__rubric | 0.61 | 0.66 | 0.96 | 0.45 | 0.66 | 0.38 | 0.34 |
| llama31_8b__rubric_unit | 0.48 | 0.49 | 0.85 | 0.29 | 0.47 | 0.22 | 0.19 |
| qwen3_32b__errors | 0.19 | 0.12 | 0.29 | 0.13 | 0.39 | 0.33 | 0.16 |
| qwen3_32b__rubric | 0.05 | 0.03 | 0.24 | 0.03 | 0.09 | 0.02 | 0.02 |
| qwen3_32b__rubric_unit | 0.05 | 0.03 | 0.13 | 0.03 | 0.07 | 0.01 | 0.03 |
| qwen3_32b_think__rubric | 0.01 | 0.02 | 0.06 | 0.02 | 0.02 | 0.00 | 0.02 |

## P2 by edit type (false-alarm rate)

| judge | anatomy | laterality | measurement | negation | severity | temporal | uncertainty |
|---|---|---|---|---|---|---|---|
| gemma3_27b__errors | 0.96 | 0.99 | 1.00 | 0.99 | 0.99 | 0.99 | 0.99 |
| gemma3_27b__rubric | 0.04 | 0.00 | 0.64 | 0.01 | 0.05 | 0.02 | 0.00 |
| gptoss_120b__errors | 0.07 | 0.05 | 0.07 | 0.06 | 0.18 | 0.06 | 0.07 |
| gptoss_120b__rubric | 0.05 | 0.04 | 0.24 | 0.05 | 0.07 | 0.04 | 0.07 |
| gptoss_20b__errors | 0.15 | 0.08 | 0.06 | 0.10 | 0.45 | 0.12 | 0.14 |
| gptoss_20b__rubric | 0.03 | 0.05 | 0.05 | 0.06 | 0.15 | 0.07 | 0.04 |
| llama31_8b__rubric | 0.19 | 0.20 | 0.98 | 0.13 | 0.26 | 0.09 | 0.09 |
| llama31_8b__rubric_unit | 0.08 | 0.08 | 0.64 | 0.05 | 0.12 | 0.02 | 0.04 |
| qwen3_32b__errors | 0.25 | 0.18 | 0.35 | 0.13 | 0.31 | 0.27 | 0.22 |
| qwen3_32b__rubric | 0.01 | 0.01 | 0.15 | 0.01 | 0.01 | 0.01 | 0.01 |
| qwen3_32b__rubric_unit | 0.01 | 0.01 | 0.09 | 0.01 | 0.01 | 0.01 | 0.01 |
| qwen3_32b_think__rubric | 0.03 | 0.04 | 0.06 | 0.02 | 0.01 | 0.03 | 0.02 |

## C0 by edit type (detection rate)

| judge | anatomy | laterality | measurement | negation | severity | temporal | uncertainty |
|---|---|---|---|---|---|---|---|
| gemma3_27b__errors | 1.00 | 0.99 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| gemma3_27b__rubric | 0.96 | 0.84 | 1.00 | 0.99 | 0.99 | 1.00 | 0.68 |
| gptoss_120b__errors | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 1.00 | 0.90 |
| gptoss_120b__rubric | 1.00 | 1.00 | 1.00 | 1.00 | 0.97 | 1.00 | 0.76 |
| gptoss_20b__errors | 0.97 | 0.99 | 1.00 | 0.99 | 0.99 | 1.00 | 0.90 |
| gptoss_20b__rubric | 0.94 | 0.97 | 1.00 | 1.00 | 0.94 | 1.00 | 0.83 |
| llama31_8b__rubric | 0.52 | 0.58 | 0.97 | 0.98 | 0.77 | 0.77 | 0.28 |
| llama31_8b__rubric_unit | 0.37 | 0.49 | 0.80 | 0.97 | 0.69 | 0.65 | 0.18 |
| qwen3_32b__errors | 1.00 | 0.97 | 0.93 | 1.00 | 0.98 | 1.00 | 0.81 |
| qwen3_32b__rubric | 0.99 | 0.93 | 0.88 | 1.00 | 0.99 | 1.00 | 0.60 |
| qwen3_32b__rubric_unit | 0.99 | 0.92 | 0.80 | 1.00 | 0.99 | 1.00 | 0.57 |
| qwen3_32b_think__rubric | 1.00 | 1.00 | 1.00 | 1.00 | 0.94 | 1.00 | 0.69 |

## C2 by edit type (detection rate)

| judge | anatomy | laterality | measurement | negation | severity | temporal | uncertainty |
|---|---|---|---|---|---|---|---|
| gemma3_27b__errors | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| gemma3_27b__rubric | 0.85 | 0.73 | 0.97 | 0.97 | 0.91 | 0.98 | 0.34 |
| gptoss_120b__errors | 1.00 | 1.00 | 1.00 | 1.00 | 0.97 | 1.00 | 0.84 |
| gptoss_120b__rubric | 1.00 | 1.00 | 1.00 | 1.00 | 0.97 | 1.00 | 0.76 |
| gptoss_20b__errors | 0.98 | 0.97 | 1.00 | 1.00 | 0.98 | 0.99 | 0.87 |
| gptoss_20b__rubric | 0.97 | 0.94 | 1.00 | 1.00 | 0.93 | 1.00 | 0.78 |
| llama31_8b__rubric | 0.55 | 0.58 | 0.97 | 0.96 | 0.81 | 0.77 | 0.37 |
| llama31_8b__rubric_unit | 0.38 | 0.44 | 0.86 | 0.92 | 0.69 | 0.60 | 0.21 |
| qwen3_32b__errors | 0.99 | 0.97 | 0.87 | 1.00 | 0.93 | 0.99 | 0.79 |
| qwen3_32b__rubric | 0.92 | 0.84 | 0.84 | 0.98 | 0.88 | 0.91 | 0.29 |
| qwen3_32b__rubric_unit | 0.92 | 0.83 | 0.78 | 0.98 | 0.88 | 0.91 | 0.31 |
| qwen3_32b_think__rubric | 1.00 | 0.99 | 1.00 | 1.00 | 0.93 | 0.99 | 0.68 |
