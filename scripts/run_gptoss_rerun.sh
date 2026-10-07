#!/usr/bin/env bash
# re-run gpt-oss-20b with final-channel parsing and a larger token budget (see docs/8 §failure log)
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/env_llm.sh; source scripts/gpu_wait.sh
run() { # corpus prompt
  local log=logs/9_judge_full_$1_gptoss_20b_$2_rerun.log
  gpu_wait 45000 43200 || return
  echo "=== $1 $2 $(date)"
  $PY scripts/9_llm_judge.py --pairs data/pairs/full_$1_all.csv --out results/2_full_$1/judges --model openai/gpt-oss-20b --tag gptoss_20b \
      --prompt $2 --max_model_len 8192 --gpu_mem 0.3 --reasoning low > $log 2>&1
  echo "EXIT=$?" >> $log
  grep -E "^\[gen|^(PRESERVED|CHANGED|UNPARSED|n=)|EXIT|OutOfMemory|ValueError" $log | tail -5; sleep 15
}
run iu rubric; run mimic rubric; run iu errors; run mimic errors
echo "ALL_DONE $(date)"
