#!/usr/bin/env bash
# sequential judge queue on the IU pilot (rubric prompt). Waits for the MIMIC paraphrase job to release the GPU.
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/env_llm.sh
until grep -q "EXIT" logs/5_paraphrase_pilot_mimic.log 2>/dev/null; do sleep 20; done
PAIRS=data/pairs/pilot_iu_all.csv; OUT=results/1_pilot_iu/judges
run() { # tag model extra...
  local tag=$1 model=$2; shift 2
  echo "=== $tag $(date)"
  $PY scripts/9_llm_judge.py --pairs $PAIRS --out $OUT --model $model --tag $tag --prompt rubric --max_model_len 2048 "$@" > logs/9_judge_pilot_iu_${tag}_rubric.log 2>&1
  echo "EXIT=$?" >> logs/9_judge_pilot_iu_${tag}_rubric.log
  grep -E "^\[gen|^(PRESERVED|CHANGED|UNPARSED)|EXIT|OutOfMemory|ValueError" logs/9_judge_pilot_iu_${tag}_rubric.log | tail -5
}
run qwen3_32b Qwen/Qwen3-32B --no_think --gpu_mem 0.6
run llama31_8b meta-llama/Llama-3.1-8B-Instruct --gpu_mem 0.3
run gemma3_27b google/gemma-3-27b-it --gpu_mem 0.55
run gptoss_20b openai/gpt-oss-20b --gpu_mem 0.4 --reasoning low
echo "ALL_DONE $(date)"
