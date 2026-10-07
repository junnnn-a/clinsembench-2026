#!/usr/bin/env bash
# queue 2: after the IU rubric queue, run rubric on the MIMIC pilot (4 models) and the GREEN-style
# "errors" prompt on the IU pilot (2 models).
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/env_llm.sh
until grep -q "ALL_DONE" logs/run_judges_pilot_iu.log 2>/dev/null; do sleep 30; done
run() { # corpus tag model prompt extra...
  local corpus=$1 tag=$2 model=$3 prompt=$4; shift 4
  local log=logs/9_judge_pilot_${corpus}_${tag}_${prompt}.log
  echo "=== $corpus $tag $prompt $(date)"
  $PY scripts/9_llm_judge.py --pairs data/pairs/pilot_${corpus}_all.csv --out results/1_pilot_${corpus}/judges --model $model --tag $tag --prompt $prompt --max_model_len 2048 "$@" > $log 2>&1
  echo "EXIT=$?" >> $log
  grep -E "^\[gen|^(PRESERVED|CHANGED|UNPARSED|n=)|EXIT|OutOfMemory|ValueError" $log | tail -4
}
run mimic qwen3_32b Qwen/Qwen3-32B rubric --no_think --gpu_mem 0.6
run mimic llama31_8b meta-llama/Llama-3.1-8B-Instruct rubric --gpu_mem 0.3
run mimic gemma3_27b google/gemma-3-27b-it rubric --gpu_mem 0.55
run mimic gptoss_20b openai/gpt-oss-20b rubric --gpu_mem 0.4 --reasoning low
run iu qwen3_32b Qwen/Qwen3-32B errors --no_think --gpu_mem 0.6 --max_tokens 400
run iu gptoss_20b openai/gpt-oss-20b errors --gpu_mem 0.4 --reasoning low --max_tokens 400
echo "ALL_DONE $(date)"
