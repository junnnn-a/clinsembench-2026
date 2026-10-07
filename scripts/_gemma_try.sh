#!/usr/bin/env bash
# 10/7: Gemma-3-27B runs. Gemma hangs after its multi-modal warm-up when KV_GB (fixed KV cache) / thread caps are set, so both are unset here.
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/env_llm.sh; source scripts/gpu_wait.sh
unset KV_GB OMP_NUM_THREADS MKL_NUM_THREADS
export VLLM_EAGER=0
run() { # set prompt extra...
  local set=$1 prompt=$2; shift 2
  for attempt in 1 2 3; do
    [ -f results/2_full_${set}/judges/gemma3_27b__${prompt}.csv ] && return
    gpu_wait 90000 86400
    echo "=== $set gemma3_27b $prompt $(date)"
    $PY scripts/9_llm_judge.py --pairs data/pairs/full_${set}_all.csv --out results/2_full_${set}/judges --model google/gemma-3-27b-it --tag gemma3_27b --prompt $prompt --gpu_mem 0.6 "$@" > logs/9_judge_full_${set}_gemma3_27b_${prompt}.log 2>&1
    echo "EXIT=$?" >> logs/9_judge_full_${set}_gemma3_27b_${prompt}.log; sleep 15
  done
}
run mimicmono errors --max_model_len 4096 --max_tokens 500
run iu rubric_unit --max_model_len 2048
run mimic rubric_unit --max_model_len 2048
echo "GEMMA_DONE $(date)"
