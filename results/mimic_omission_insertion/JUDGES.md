# LLM judges — rate of CHANGED verdicts per cell

P cells and identity should be 0 (false alarms); C cells should be 1 (detections).

| judge | identity | P0 | P1 | P2 | C0 | C1 | C2 |
|---|---|---|---|---|---|---|---|
| gemma3_27b__rubric | 0.000 | 0.063 | 0.213 | 0.110 | 0.777 | 0.600 | 0.463 |
| gptoss_120b__rubric | 0.000 | 0.170 | 0.103 | 0.143 | 0.983 | 0.990 | 0.990 |
| gptoss_20b__rubric | 0.000 | 0.083 | 0.057 | 0.100 | 0.980 | 0.970 | 0.963 |
| llama31_8b__rubric | 0.000 | 0.003 | 0.373 | 0.110 | 0.387 | 0.783 | 0.500 |
| qwen3_32b__rubric | 0.000 | 0.367 | 0.070 | 0.077 | 0.977 | 0.477 | 0.630 |

## P0 by edit type (false-alarm rate)

| judge | insertion | omission |
|---|---|---|
| gemma3_27b__rubric | 0.11 | 0.02 |
| gptoss_120b__rubric | 0.02 | 0.32 |
| gptoss_20b__rubric | 0.03 | 0.14 |
| llama31_8b__rubric | 0.01 | 0.00 |
| qwen3_32b__rubric | 0.55 | 0.18 |

## P1 by edit type (false-alarm rate)

| judge | insertion | omission |
|---|---|---|
| gemma3_27b__rubric | 0.31 | 0.11 |
| gptoss_120b__rubric | 0.01 | 0.19 |
| gptoss_20b__rubric | 0.03 | 0.08 |
| llama31_8b__rubric | 0.37 | 0.37 |
| qwen3_32b__rubric | 0.14 | 0.00 |

## P2 by edit type (false-alarm rate)

| judge | insertion | omission |
|---|---|---|
| gemma3_27b__rubric | 0.19 | 0.03 |
| gptoss_120b__rubric | 0.06 | 0.23 |
| gptoss_20b__rubric | 0.09 | 0.11 |
| llama31_8b__rubric | 0.16 | 0.06 |
| qwen3_32b__rubric | 0.13 | 0.03 |

## C0 by edit type (detection rate)

| judge | insertion | omission |
|---|---|---|
| gemma3_27b__rubric | 0.98 | 0.57 |
| gptoss_120b__rubric | 0.99 | 0.98 |
| gptoss_20b__rubric | 0.97 | 0.99 |
| llama31_8b__rubric | 0.27 | 0.51 |
| qwen3_32b__rubric | 1.00 | 0.95 |

## C2 by edit type (detection rate)

| judge | insertion | omission |
|---|---|---|
| gemma3_27b__rubric | 0.78 | 0.15 |
| gptoss_120b__rubric | 0.99 | 0.99 |
| gptoss_20b__rubric | 0.95 | 0.98 |
| llama31_8b__rubric | 0.63 | 0.37 |
| qwen3_32b__rubric | 0.97 | 0.29 |
