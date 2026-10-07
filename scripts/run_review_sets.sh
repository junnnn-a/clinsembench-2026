#!/usr/bin/env bash
# 10/7 review: score the extra sets one after another. Resumable.
# The container has an 8-core CPU quota shared with another project, so the sets are scored sequentially and in order of
# importance, and judges are limited: iualt (S2 robustness; metrics + CRIMSON) -> rate3 (public suite; + gpt-oss-20b)
# -> rate1 / rate2 (external validity; rate1 + gpt-oss-20b, rate2 metrics only)
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
NO_JUDGES=1 bash scripts/run_set.sh iualt > logs/run_set_iualt.log 2>&1
ONE_JUDGE=1 bash scripts/run_set.sh rate3 > logs/run_set_rate3.log 2>&1
ONE_JUDGE=1 bash scripts/run_set.sh rate1 > logs/run_set_rate1.log 2>&1
NO_LLM=1 bash scripts/run_set.sh rate2 > logs/run_set_rate2.log 2>&1
echo "REVIEW_SETS_DONE $(date)"
