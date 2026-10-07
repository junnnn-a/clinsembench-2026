#!/usr/bin/env bash
# queue 4: pilot fill-ins once the GPU is free (MIMIC GREEN/bertscore re-score, Qwen3-32B bf16 rubric, errors prompt).
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/gpu_wait.sh
( bash scripts/run_scores_pilot_mimic.sh > logs/run_scores_pilot_mimic_r2.log 2>&1 ) &
source scripts/env_llm.sh
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
run iu    qwen3_32b Qwen/Qwen3-32B rubric 90000 0.6 --no_think
run mimic qwen3_32b Qwen/Qwen3-32B rubric 90000 0.6 --no_think
run iu    qwen3_32b Qwen/Qwen3-32B errors 90000 0.6 --no_think --max_tokens 400
run iu    gptoss_20b openai/gpt-oss-20b errors 30000 0.2 --reasoning low --max_tokens 400
run iu    gemma3_27b google/gemma-3-27b-it errors 66000 0.45 --max_tokens 400
wait
echo "ALL_DONE $(date)"
