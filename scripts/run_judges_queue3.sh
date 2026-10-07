#!/usr/bin/env bash
# queue 3 (GPU-contention aware): every job waits until enough GPU memory is free. Requirements are
# weights + KV headroom; gpu_mem is the matching fraction of 139.8 GiB.
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/env_llm.sh; source scripts/gpu_wait.sh
run() { # corpus tag model prompt need_MiB gpu_mem extra...
  local corpus=$1 tag=$2 model=$3 prompt=$4 need=$5 mem=$6; shift 6
  local log=logs/9_judge_pilot_${corpus}_${tag}_${prompt}.log
  [ -f results/1_pilot_${corpus}/judges/${tag}__${prompt}.csv ] && { echo "skip $corpus $tag $prompt"; return; }
  gpu_wait $need 14400 || return
  echo "=== $corpus $tag $prompt $(date)"
  $PY scripts/9_llm_judge.py --pairs data/pairs/pilot_${corpus}_all.csv --out results/1_pilot_${corpus}/judges --model $model --tag $tag --prompt $prompt --max_model_len 2048 --gpu_mem $mem "$@" > $log 2>&1
  echo "EXIT=$?" >> $log
  grep -E "^\[gen|^(PRESERVED|CHANGED|UNPARSED|n=)|EXIT|OutOfMemory|ValueError" $log | tail -4
  sleep 15
}
crimson() { # corpus need mem
  [ -f results/1_pilot_$1/scores_all/crimson.csv ] && [ $(wc -l < results/1_pilot_$1/scores_all/crimson.csv) -gt 1900 ] && { echo "skip crimson $1"; return; }
  gpu_wait $2 14400 || return
  echo "=== crimson $1 $(date)"
  $PY scripts/10_crimson.py --pairs data/pairs/pilot_$1_all.csv --out results/1_pilot_$1/scores_all --gpu_mem $3 > logs/10_crimson_pilot_$1.log 2>&1
  echo "EXIT=$?" >> logs/10_crimson_pilot_$1.log
  grep -E "^\[crimson|EXIT|Error" logs/10_crimson_pilot_$1.log | grep -v INFO | tail -3
  sleep 15
}
run iu    gptoss_20b openai/gpt-oss-20b rubric 27000 0.18 --reasoning low
run mimic llama31_8b meta-llama/Llama-3.1-8B-Instruct rubric 23000 0.15
run mimic gptoss_20b openai/gpt-oss-20b rubric 27000 0.18 --reasoning low
until grep -q "DL_DONE" logs/downloads_round2.log 2>/dev/null; do sleep 30; done
crimson iu 19000 0.12
crimson mimic 19000 0.12
run iu    qwen3_32b_fp8 Qwen/Qwen3-32B-FP8 rubric 45000 0.30 --no_think
run mimic qwen3_32b_fp8 Qwen/Qwen3-32B-FP8 rubric 45000 0.30 --no_think
run iu    qwen3_32b_fp8 Qwen/Qwen3-32B-FP8 errors 45000 0.30 --no_think --max_tokens 400
run iu    gptoss_20b openai/gpt-oss-20b errors 27000 0.18 --reasoning low --max_tokens 400
run iu    gemma3_27b google/gemma-3-27b-it rubric 66000 0.45
run mimic gemma3_27b google/gemma-3-27b-it rubric 66000 0.45
echo "ALL_DONE $(date)"
