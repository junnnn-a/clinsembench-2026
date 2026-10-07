#!/usr/bin/env bash
# extra open-weight judges on the full sets: gpt-oss-120b (strongest open reasoning model we can run),
# Qwen3-32B with thinking enabled, Qwen3-32B errors prompt.
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/env_llm.sh; source scripts/gpu_wait.sh
until grep -q "ALL_DONE" logs/run_gptoss_rerun.log; do sleep 60; done
run() { # corpus tag model prompt need mem extra...
  local corpus=$1 tag=$2 model=$3 prompt=$4 need=$5 mem=$6; shift 6
  local log=logs/9_judge_full_${corpus}_${tag}_${prompt}.log
  for attempt in 1 2 3; do
    [ -f results/2_full_${corpus}/judges/${tag}__${prompt}.csv ] && return
    gpu_wait $need 86400 || return
    echo "=== $corpus $tag $prompt $(date)"
    $PY scripts/9_llm_judge.py --pairs data/pairs/full_${corpus}_all.csv --out results/2_full_${corpus}/judges --model $model --tag $tag --prompt $prompt --gpu_mem $mem "$@" > $log 2>&1
    echo "EXIT=$?" >> $log
    grep -E "^\[gen|EXIT|OutOfMemory|ValueError" $log | tail -3 | cut -c1-140; sleep 15
  done
}
run iu    gptoss_120b openai/gpt-oss-120b rubric 88000 0.6 --reasoning low --max_model_len 8192
run mimic gptoss_120b openai/gpt-oss-120b rubric 88000 0.6 --reasoning low --max_model_len 8192
run iu    qwen3_32b_think Qwen/Qwen3-32B rubric 90000 0.6 --max_model_len 8192 --max_tokens 3072
run iu    qwen3_32b Qwen/Qwen3-32B errors 90000 0.6 --no_think --max_model_len 4096 --max_tokens 500
run iu    gptoss_120b openai/gpt-oss-120b errors 88000 0.6 --reasoning low --max_model_len 8192
echo "ALL_DONE $(date)"
