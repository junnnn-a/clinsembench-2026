# LLM judges — rate of CHANGED verdicts per cell

P cells and identity should be 0 (false alarms); C cells should be 1 (detections).

| judge | identity | P0 | P1 | P2 | C0 | C1 | C2 |
|---|---|---|---|---|---|---|---|
| gemma3_27b__rubric | 0.000 | 0.293 | 0.311 | 0.096 | 0.941 | 0.880 | 0.808 |
| gptoss_120b__rubric | 0.001 | 0.070 | 0.077 | 0.104 | 0.987 | 0.977 | 0.978 |
| gptoss_20b__errors | 0.000 | 0.151 | 0.113 | 0.200 | 0.990 | 0.971 | 0.977 |
| gptoss_20b__rubric | 0.000 | 0.048 | 0.038 | 0.087 | 0.975 | 0.968 | 0.950 |
| llama31_8b__rubric | 0.006 | 0.150 | 0.594 | 0.250 | 0.610 | 0.849 | 0.661 |
| qwen3_32b__rubric | 0.000 | 0.257 | 0.173 | 0.108 | 0.939 | 0.835 | 0.823 |
| qwen3_32b__rubric_unit | 0.000 | 0.205 | 0.122 | 0.053 | 0.930 | 0.825 | 0.805 |
| qwen3_32b_think__rubric | 0.000 | 0.064 | 0.056 | 0.057 | 0.979 | 0.968 | 0.968 |

## P0 by edit type (false-alarm rate)

| judge | anatomy | laterality | measurement | negation | severity | temporal | uncertainty |
|---|---|---|---|---|---|---|---|
| gemma3_27b__rubric | 0.22 | 0.03 | 0.85 | 0.03 | 0.54 | 0.35 | 0.04 |
| gptoss_120b__rubric | 0.01 | 0.00 | 0.29 | 0.03 | 0.08 | 0.03 | 0.05 |
| gptoss_20b__errors | 0.10 | 0.00 | 0.05 | 0.03 | 0.51 | 0.09 | 0.29 |
| gptoss_20b__rubric | 0.00 | 0.01 | 0.04 | 0.02 | 0.12 | 0.03 | 0.11 |
| llama31_8b__rubric | 0.13 | 0.05 | 0.48 | 0.03 | 0.13 | 0.17 | 0.07 |
| qwen3_32b__rubric | 0.21 | 0.01 | 0.96 | 0.05 | 0.32 | 0.25 | 0.01 |
| qwen3_32b__rubric_unit | 0.15 | 0.01 | 0.70 | 0.05 | 0.29 | 0.21 | 0.01 |
| qwen3_32b_think__rubric | 0.01 | 0.00 | 0.33 | 0.01 | 0.07 | 0.03 | 0.00 |

## P1 by edit type (false-alarm rate)

| judge | anatomy | laterality | measurement | negation | severity | temporal | uncertainty |
|---|---|---|---|---|---|---|---|
| gemma3_27b__rubric | 0.18 | 0.14 | 0.83 | 0.09 | 0.43 | 0.31 | 0.19 |
| gptoss_120b__rubric | 0.02 | 0.00 | 0.37 | 0.02 | 0.09 | 0.01 | 0.03 |
| gptoss_20b__errors | 0.07 | 0.01 | 0.06 | 0.01 | 0.55 | 0.01 | 0.09 |
| gptoss_20b__rubric | 0.00 | 0.00 | 0.07 | 0.02 | 0.11 | 0.01 | 0.06 |
| llama31_8b__rubric | 0.55 | 0.55 | 0.85 | 0.41 | 0.67 | 0.58 | 0.55 |
| qwen3_32b__rubric | 0.05 | 0.01 | 0.87 | 0.03 | 0.13 | 0.11 | 0.01 |
| qwen3_32b__rubric_unit | 0.05 | 0.01 | 0.54 | 0.03 | 0.10 | 0.11 | 0.01 |
| qwen3_32b_think__rubric | 0.01 | 0.01 | 0.31 | 0.01 | 0.03 | 0.01 | 0.00 |

## P2 by edit type (false-alarm rate)

| judge | anatomy | laterality | measurement | negation | severity | temporal | uncertainty |
|---|---|---|---|---|---|---|---|
| gemma3_27b__rubric | 0.06 | 0.01 | 0.41 | 0.03 | 0.10 | 0.05 | 0.01 |
| gptoss_120b__rubric | 0.06 | 0.05 | 0.25 | 0.08 | 0.11 | 0.09 | 0.09 |
| gptoss_20b__errors | 0.18 | 0.09 | 0.16 | 0.18 | 0.53 | 0.11 | 0.15 |
| gptoss_20b__rubric | 0.07 | 0.05 | 0.14 | 0.07 | 0.14 | 0.07 | 0.07 |
| llama31_8b__rubric | 0.17 | 0.15 | 0.69 | 0.14 | 0.23 | 0.23 | 0.15 |
| qwen3_32b__rubric | 0.02 | 0.01 | 0.62 | 0.03 | 0.03 | 0.03 | 0.00 |
| qwen3_32b__rubric_unit | 0.02 | 0.01 | 0.27 | 0.03 | 0.03 | 0.02 | 0.01 |
| qwen3_32b_think__rubric | 0.07 | 0.03 | 0.12 | 0.05 | 0.05 | 0.04 | 0.03 |

## C0 by edit type (detection rate)

| judge | anatomy | laterality | measurement | negation | severity | temporal | uncertainty |
|---|---|---|---|---|---|---|---|
| gemma3_27b__rubric | 0.98 | 0.88 | 0.99 | 1.00 | 0.98 | 0.99 | 0.76 |
| gptoss_120b__rubric | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 1.00 | 0.93 |
| gptoss_20b__errors | 0.98 | 0.99 | 0.99 | 0.99 | 1.00 | 1.00 | 0.99 |
| gptoss_20b__rubric | 0.94 | 0.99 | 1.00 | 1.00 | 0.95 | 0.99 | 0.96 |
| llama31_8b__rubric | 0.45 | 0.55 | 0.65 | 0.94 | 0.56 | 0.87 | 0.25 |
| qwen3_32b__rubric | 1.00 | 0.91 | 0.99 | 1.00 | 0.98 | 0.99 | 0.70 |
| qwen3_32b__rubric_unit | 1.00 | 0.89 | 0.95 | 1.00 | 0.98 | 0.99 | 0.71 |
| qwen3_32b_think__rubric | 1.00 | 1.00 | 1.00 | 1.00 | 0.96 | 1.00 | 0.89 |

## C2 by edit type (detection rate)

| judge | anatomy | laterality | measurement | negation | severity | temporal | uncertainty |
|---|---|---|---|---|---|---|---|
| gemma3_27b__rubric | 0.87 | 0.71 | 0.98 | 0.99 | 0.81 | 0.91 | 0.39 |
| gptoss_120b__rubric | 1.00 | 0.99 | 1.00 | 1.00 | 0.97 | 0.99 | 0.90 |
| gptoss_20b__errors | 0.97 | 0.97 | 0.99 | 0.99 | 1.00 | 1.00 | 0.92 |
| gptoss_20b__rubric | 0.97 | 0.99 | 1.00 | 1.00 | 0.92 | 0.99 | 0.79 |
| llama31_8b__rubric | 0.46 | 0.55 | 0.78 | 0.95 | 0.62 | 0.87 | 0.40 |
| qwen3_32b__rubric | 0.87 | 0.84 | 0.97 | 0.99 | 0.79 | 0.91 | 0.37 |
| qwen3_32b__rubric_unit | 0.87 | 0.82 | 0.89 | 0.99 | 0.77 | 0.91 | 0.38 |
| qwen3_32b_think__rubric | 1.00 | 1.00 | 1.00 | 1.00 | 0.91 | 0.99 | 0.87 |
