# External validity: do our columns order scorers the way radiologists do? (RaTE-Eval Tasks 1-2)

## Per scorer: Kendall tau with radiologist ratings, and our paired accuracies (mean of IU and MIMIC)

| metric | Task 1 (sentence) | Task 2 (paragraph) | Conf-R | Conf-P | Ctrl-0 | Ctrl-2 | mono tau (fixed surface) |
|---|---|---|---|---|---|---|---|
| bertscore_deberta_mnli | 0.216 | 0.437 | 0.023 | 0.031 | 0.801 | 0.810 | 0.739 |
| bertscore_distilbert | 0.285 | 0.474 | 0.001 | 0.012 | 0.642 | 0.638 | 0.357 |
| bertscore_roberta_large | 0.224 | 0.442 | 0.005 | 0.012 | 0.667 | 0.697 | 0.564 |
| bleu | 0.124 | 0.301 | 0.007 | 0.009 | 0.564 | 0.558 | 0.175 |
| crimson | 0.262 |  | 0.814 | 0.820 | 0.823 | 0.818 | 0.883 |
| f1chexbert | 0.084 | 0.160 | 0.513 | 0.498 | 0.523 | 0.524 | 0.003 |
| gptoss_20b__rubric | 0.377 |  | 0.971 | 0.963 | 0.968 | 0.951 | 0.693 |
| green | 0.375 | 0.395 | 0.716 | 0.675 | 0.841 | 0.757 | 0.772 |
| jaccard | 0.242 | 0.453 | 0.611 | 0.021 | 0.611 | 0.606 | 0.410 |
| radcliq | 0.314 | 0.489 | 0.088 | 0.034 | 0.707 | 0.707 | 0.583 |
| radgraph | 0.356 | 0.375 | 0.304 | 0.052 | 0.571 | 0.580 | 0.163 |
| ratescore | 0.352 | 0.462 | 0.616 | 0.138 | 0.668 | 0.661 | 0.483 |
| rougeL | 0.215 | 0.396 | 0.000 | 0.011 | 0.568 | 0.568 | 0.356 |
| srrbert | 0.092 | 0.209 | 0.606 | 0.483 | 0.611 | 0.612 | 0.358 |
| temporal | 0.026 | 0.134 | 0.530 | 0.384 | 0.530 | 0.528 | 0.111 |
| token_f1 | 0.237 | 0.409 | 0.620 | 0.019 | 0.620 | 0.621 | 0.456 |

## Across scorers: Spearman correlation between human tau and each of our columns

| human set | scorers | our column | n_scorers | spearman | ci_lo | ci_hi | perm_p |
|---|---|---|---|---|---|---|---|
| Task 1 (sentence) | all scorers | Conf-R | 16 | 0.406 | -0.119 | 0.772 | 0.116 |
| Task 1 (sentence) | metrics only (no LLM judges) | Conf-R | 15 | 0.279 | -0.280 | 0.690 | 0.329 |
| Task 1 (sentence) | all scorers | Conf-P | 16 | 0.294 | -0.319 | 0.790 | 0.273 |
| Task 1 (sentence) | metrics only (no LLM judges) | Conf-P | 15 | 0.143 | -0.424 | 0.702 | 0.608 |
| Task 1 (sentence) | all scorers | Ctrl-0 | 16 | 0.718 | 0.237 | 0.935 | 0.003 |
| Task 1 (sentence) | metrics only (no LLM judges) | Ctrl-0 | 15 | 0.657 | 0.081 | 0.924 | 0.012 |
| Task 1 (sentence) | all scorers | Ctrl-1 | 16 | 0.644 | 0.172 | 0.881 | 0.007 |
| Task 1 (sentence) | metrics only (no LLM judges) | Ctrl-1 | 15 | 0.568 | 0.024 | 0.838 | 0.035 |
| Task 1 (sentence) | all scorers | Ctrl-2 | 16 | 0.659 | 0.129 | 0.914 | 0.007 |
| Task 1 (sentence) | metrics only (no LLM judges) | Ctrl-2 | 15 | 0.586 | 0.069 | 0.881 | 0.024 |
| Task 1 (sentence) | all scorers | mono growing-surface step | 16 | 0.009 | -0.693 | 0.591 | 0.978 |
| Task 1 (sentence) | metrics only (no LLM judges) | mono growing-surface step | 15 | 0.184 | -0.565 | 0.669 | 0.513 |
| Task 1 (sentence) | all scorers | mono tau (fixed surface) | 16 | 0.559 | 0.009 | 0.870 | 0.024 |
| Task 1 (sentence) | metrics only (no LLM judges) | mono tau (fixed surface) | 15 | 0.525 | -0.075 | 0.881 | 0.045 |
| Task 2 (paragraph) | all scorers | Conf-R | 14 | -0.160 | -0.590 | 0.362 | 0.578 |
| Task 2 (paragraph) | metrics only (no LLM judges) | Conf-R | 14 | -0.160 | -0.610 | 0.335 | 0.591 |
| Task 2 (paragraph) | all scorers | Conf-P | 14 | -0.371 | -0.728 | 0.295 | 0.199 |
| Task 2 (paragraph) | metrics only (no LLM judges) | Conf-P | 14 | -0.371 | -0.733 | 0.291 | 0.190 |
| Task 2 (paragraph) | all scorers | Ctrl-0 | 14 | 0.662 | 0.145 | 0.928 | 0.013 |
| Task 2 (paragraph) | metrics only (no LLM judges) | Ctrl-0 | 14 | 0.662 | 0.122 | 0.928 | 0.010 |
| Task 2 (paragraph) | all scorers | Ctrl-1 | 14 | 0.626 | 0.136 | 0.888 | 0.021 |
| Task 2 (paragraph) | metrics only (no LLM judges) | Ctrl-1 | 14 | 0.626 | 0.148 | 0.893 | 0.022 |
| Task 2 (paragraph) | all scorers | Ctrl-2 | 14 | 0.666 | 0.170 | 0.914 | 0.012 |
| Task 2 (paragraph) | metrics only (no LLM judges) | Ctrl-2 | 14 | 0.666 | 0.154 | 0.913 | 0.010 |
| Task 2 (paragraph) | all scorers | mono growing-surface step | 14 | 0.641 | 0.087 | 0.879 | 0.019 |
| Task 2 (paragraph) | metrics only (no LLM judges) | mono growing-surface step | 14 | 0.641 | 0.111 | 0.880 | 0.016 |
| Task 2 (paragraph) | all scorers | mono tau (fixed surface) | 14 | 0.618 | 0.027 | 0.888 | 0.020 |
| Task 2 (paragraph) | metrics only (no LLM judges) | mono tau (fixed surface) | 14 | 0.618 | 0.050 | 0.896 | 0.023 |
