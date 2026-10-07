#!/usr/bin/env bash
# FULL set pipeline (IU + MIMIC): S2 paraphrase -> shortcut floor -> metric scoring (parallel per metric)
# -> CRIMSON -> LLM judges. GPU-contention aware (gpu_wait). Resumable: every step skips finished outputs.
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/gpu_wait.sh
CPY=/opt/conda/envs/clinsev/bin/python
mkdir -p results/2_full_iu results/2_full_mimic

# ---- 1. S2 paraphrase (retry up to 6 times: other jobs on the shared GPU can grab memory during start-up)
( source scripts/env_llm.sh
  for c in iu mimic; do
    for attempt in 1 2 3 4 5 6; do
      [ -f data/pairs/full_${c}_all.csv ] && break
      gpu_wait 30000 14400
      $PY scripts/5_paraphrase_context.py --corpus $c --tag full --gpu_mem 0.15 > logs/5_paraphrase_full_$c.log 2>&1
      echo "EXIT=$? (attempt $attempt)" >> logs/5_paraphrase_full_$c.log
      grep -E "^\[|^  |EXIT" logs/5_paraphrase_full_$c.log | grep -v "INFO\|WARNING" | tail -5
      sleep 30
    done
  done )
for c in iu mimic; do [ -f data/pairs/full_${c}_all.csv ] || { echo "FATAL: no S2 for $c"; exit 1; }; done

# ---- 2. shortcut floor (CPU)
for c in iu mimic; do
  $CPY scripts/6_shortcut_floor.py --pairs_csv data/pairs/full_${c}_all.csv --out_csv results/2_full_$c/shortcut_floor_all.csv > logs/6_shortcut_floor_full_$c.log 2>&1 &
done

# ---- 3. metric scoring, one process per metric group (clinsev env)
score() { # corpus group
  HF_HOME=/home/irteam/hf_cache TOKENIZERS_PARALLELISM=false $CPY scripts/7_score_metrics.py --pairs data/pairs/full_$1_all.csv \
     --out results/2_full_$1/scores --metrics $2 --batch_size 16 >> logs/7_score_full_$1_${2//,/_}.log 2>&1
  echo "EXIT=$?" >> logs/7_score_full_$1_${2//,/_}.log
}
for c in iu mimic; do
  for g in lexical,bertscore,f1chexbert,srrbert radgraph ratescore temporal radcliq green; do
    score $c $g &
    sleep 20
  done
done

# ---- 4. CRIMSON + judges (llm env), sequential with gpu_wait
( source scripts/env_llm.sh
  for c in iu mimic; do
    gpu_wait 19000 28800
    $PY scripts/10_crimson.py --pairs data/pairs/full_${c}_all.csv --out results/2_full_$c/scores --gpu_mem 0.12 > logs/10_crimson_full_$c.log 2>&1
    echo "EXIT=$?" >> logs/10_crimson_full_$c.log
    grep -E "^\[crimson|EXIT" logs/10_crimson_full_$c.log | tail -3; sleep 15
  done
  run() { # corpus tag model prompt need_MiB gpu_mem extra...
    local corpus=$1 tag=$2 model=$3 prompt=$4 need=$5 mem=$6; shift 6
    local log=logs/9_judge_full_${corpus}_${tag}_${prompt}.log
    [ -f results/2_full_${corpus}/judges/${tag}__${prompt}.csv ] && { echo "skip $corpus $tag $prompt"; return; }
    gpu_wait $need 43200 || return
    echo "=== $corpus $tag $prompt $(date)"
    $PY scripts/9_llm_judge.py --pairs data/pairs/full_${corpus}_all.csv --out results/2_full_${corpus}/judges --model $model --tag $tag --prompt $prompt --max_model_len 2048 --gpu_mem $mem "$@" > $log 2>&1
    echo "EXIT=$?" >> $log
    grep -E "^\[gen|^(PRESERVED|CHANGED|UNPARSED|n=)|EXIT|OutOfMemory|ValueError" $log | tail -4
    sleep 15
  }
  for c in iu mimic; do
    run $c gptoss_20b openai/gpt-oss-20b rubric 30000 0.2 --reasoning low
    run $c llama31_8b meta-llama/Llama-3.1-8B-Instruct rubric 23000 0.15
  done
  for c in iu mimic; do
    run $c gemma3_27b google/gemma-3-27b-it rubric 66000 0.45
    run $c qwen3_32b Qwen/Qwen3-32B rubric 90000 0.6 --no_think
  done
  run iu gptoss_20b openai/gpt-oss-20b errors 30000 0.2 --reasoning low --max_tokens 400
  run iu gemma3_27b google/gemma-3-27b-it errors 66000 0.45 --max_tokens 400
)
wait
echo "ALL_DONE $(date)"
