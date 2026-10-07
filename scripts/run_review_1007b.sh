#!/usr/bin/env bash
# experiments added in response to the 10/7 external review (docs/13). GPU-contention aware, resumable.
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/env_llm.sh; source scripts/gpu_wait.sh
judge() { # set tag model prompt need mem extra...
  local set=$1 tag=$2 model=$3 prompt=$4 need=$5 mem=$6; shift 6
  local log=logs/9_judge_full_${set}_${tag}_${prompt}.log
  for attempt in 1 2 3 4; do
    [ -f results/2_full_${set}/judges/${tag}__${prompt}.csv ] && return
    gpu_wait $need 86400 || return
    echo "=== $set $tag $prompt $(date)"
    $PY scripts/9_llm_judge.py --pairs data/pairs/full_${set}_all.csv --out results/2_full_${set}/judges --model $model --tag $tag --prompt $prompt --gpu_mem $mem "$@" > $log 2>&1
    echo "EXIT=$?" >> $log
    grep -E "^\[gen|EXIT|OutOfMemory|ValueError" $log | tail -2 | cut -c1-140; sleep 15
  done
}
# 10/7 03:30 — second version of the queue. The container turned out to have an 8-core CPU quota shared with another project,
# so the remaining judge runs are reordered by importance (docs/13 §6) and gpt-oss-20b rubric_unit is dropped (its unit false alarms were already 1-4%).
judge mimicmono gptoss_20b  openai/gpt-oss-20b errors 45000 0.3 --reasoning low --max_model_len 8192
judge mimicmono gptoss_120b openai/gpt-oss-120b errors 88000 0.6 --reasoning low --max_model_len 8192
judge mimicmono qwen3_32b   Qwen/Qwen3-32B errors 90000 0.6 --no_think --max_model_len 4096 --max_tokens 500
judge iu gemma3_27b google/gemma-3-27b-it rubric_unit 66000 0.45 --max_model_len 2048
judge iu qwen3_32b  Qwen/Qwen3-32B rubric_unit 90000 0.6 --no_think --max_model_len 2048
judge mimic qwen3_32b  Qwen/Qwen3-32B rubric_unit 90000 0.6 --no_think --max_model_len 2048
judge mimic gemma3_27b google/gemma-3-27b-it rubric_unit 66000 0.45 --max_model_len 2048
judge mimicmono gemma3_27b  google/gemma-3-27b-it errors 66000 0.45 --max_model_len 4096 --max_tokens 500
judge iu llama31_8b meta-llama/Llama-3.1-8B-Instruct rubric_unit 40000 0.25 --max_model_len 2048
judge mimicmono qwen3_32b_think Qwen/Qwen3-32B rubric 90000 0.6 --max_model_len 8192 --max_tokens 3072
judge mimic     qwen3_32b_think Qwen/Qwen3-32B rubric 90000 0.6 --max_model_len 8192 --max_tokens 3072
echo "REVIEW1007_DONE $(date)"
