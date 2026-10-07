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
# Gemma-3-27B hangs after its multi-modal warm-up in eager mode (4 times); it is run with torch.compile + CUDA graphs instead (VLLM_EAGER=0).
# 10/7 06:50 — final arrangement (docs/13 §6): ONE sequential queue for everything that starts a vLLM engine. Two engines
# initialising at the same time made the first one hang after its warm-up (three times), so no other LLM job may run alongside.
export GPU_HOLD=300
while pgrep -f "^/home/irteam/junah-data-1/ARR_10/2_ClimSemBench/envs/llm/bin/python scripts/(9_llm_judge|10_crimson)" > /dev/null; do sleep 30; done
judge iu qwen3_32b  Qwen/Qwen3-32B rubric_unit 90000 0.6 --no_think --max_model_len 2048
judge mimic qwen3_32b  Qwen/Qwen3-32B rubric_unit 90000 0.6 --no_think --max_model_len 2048
judge iu llama31_8b meta-llama/Llama-3.1-8B-Instruct rubric_unit 40000 0.25 --max_model_len 2048
judge mimicmono qwen3_32b_think Qwen/Qwen3-32B rubric 90000 0.6 --max_model_len 8192 --max_tokens 3072
judge mimic     qwen3_32b_think Qwen/Qwen3-32B rubric 90000 0.6 --max_model_len 8192 --max_tokens 3072
echo "REVIEW1007_DONE $(date)"
ONE_JUDGE=1 bash scripts/run_set.sh rate1 > logs/run_set_rate1.log 2>&1
NO_LLM=1 bash scripts/run_set.sh rate2 > logs/run_set_rate2.log 2>&1
echo "REVIEW_SETS_DONE $(date)"
# Gemma-3-27B last: it hung after the multi-modal warm-up four times today (eager and compile mode alike); see docs/13 §6
VLLM_EAGER=0 judge iu gemma3_27b google/gemma-3-27b-it rubric_unit 66000 0.45 --max_model_len 2048
VLLM_EAGER=0 judge mimic gemma3_27b google/gemma-3-27b-it rubric_unit 66000 0.45 --max_model_len 2048
VLLM_EAGER=0 judge mimicmono gemma3_27b  google/gemma-3-27b-it errors 66000 0.45 --max_model_len 4096 --max_tokens 500
echo "GEMMA_DONE $(date)"
