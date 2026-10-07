#!/usr/bin/env bash
# run_set.sh <tag>  — generic, resumable scoring pipeline for data/pairs/full_<tag>_all.csv -> results/2_full_<tag>/
#   floor -> metrics (each waits for GPU memory, <=3 in parallel) -> CRIMSON -> judges (rubric). All steps skip finished outputs.
TAG=$1
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/gpu_wait.sh
# 10/7: every scorer used to start ~190 threads and starved on the shared machine (RadGraph 9 s/pair) -> cap CPU threads
export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 NUMEXPR_NUM_THREADS=8
CPY=/opt/conda/envs/clinsev/bin/python
PAIRS=data/pairs/full_${TAG}_all.csv
OUT=results/2_full_${TAG}
[ -f $PAIRS ] || { echo "no $PAIRS"; exit 1; }
mkdir -p $OUT
$CPY scripts/6_shortcut_floor.py --pairs_csv $PAIRS --out_csv $OUT/shortcut_floor_all.csv > logs/6_shortcut_floor_full_$TAG.log 2>&1 &
score() { # group need
  for m in ${1//,/ }; do [ -f $OUT/scores/$m.csv ] || break; done
  [ -f $OUT/scores/${1##*,}.csv ] && [ -f $OUT/scores/${1%%,*}.csv ] && return
  gpu_wait $2 43200
  HF_HOME=/home/irteam/hf_cache TOKENIZERS_PARALLELISM=false $CPY scripts/7_score_metrics.py --pairs $PAIRS --out $OUT/scores --metrics $1 --batch_size 16 >> logs/7_score_full_${TAG}_${1//,/_}.log 2>&1
  grep -E "^\[done\]|FAILED" logs/7_score_full_${TAG}_${1//,/_}.log | tail -2 | cut -c1-140
}
for round in 1 2 3; do
  score lexical,bertscore,f1chexbert,srrbert 16000 &
  score radgraph 12000 & score ratescore 12000 &
  wait
  score temporal 12000 & score radcliq 12000 & { [ -n "$SKIP_GREEN" ] || score green 30000; } &
  wait
  ok=1; for m in lexical bertscore f1chexbert srrbert radgraph ratescore temporal radcliq $([ -n "$SKIP_GREEN" ] || echo green); do [ -f $OUT/scores/$m.csv ] || ok=0; done
  [ $ok -eq 1 ] && break
done
[ -n "$NO_LLM" ] && { wait; echo "ALL_DONE $TAG (metrics only) $(date)"; exit 0; }   # NO_LLM=1: skip CRIMSON and judges
( source scripts/env_llm.sh
  n=$(($(wc -l < $PAIRS) - 1))
  for attempt in 1 2 3; do
    gpu_wait 19000 43200
    $PY scripts/10_crimson.py --pairs $PAIRS --out $OUT/scores --gpu_mem 0.12 > logs/10_crimson_full_$TAG.log 2>&1
    grep -E "^\[crimson" logs/10_crimson_full_$TAG.log | tail -1 | cut -c1-140
    grep -q "todo=0\|parse failures" logs/10_crimson_full_$TAG.log && break
    sleep 30
  done
  run() { # tag model prompt need mem extra...
    local tag=$1 model=$2 prompt=$3 need=$4 mem=$5; shift 5
    local log=logs/9_judge_full_${TAG}_${tag}_${prompt}.log
    for attempt in 1 2 3; do
      [ -f $OUT/judges/${tag}__${prompt}.csv ] && return
      gpu_wait $need 43200 || return
      echo "=== $TAG $tag $prompt $(date)"
      $PY scripts/9_llm_judge.py --pairs $PAIRS --out $OUT/judges --model $model --tag $tag --prompt $prompt --gpu_mem $mem "$@" > $log 2>&1
      echo "EXIT=$?" >> $log
      grep -E "^\[gen|EXIT|OutOfMemory|ValueError" $log | tail -3 | cut -c1-140; sleep 15
    done
  }
  [ -n "$NO_JUDGES" ] && exit 0                       # NO_JUDGES=1: metrics + CRIMSON only
  run gptoss_20b openai/gpt-oss-20b rubric 45000 0.3 --reasoning low --max_model_len 8192
  [ -n "$ONE_JUDGE" ] && exit 0                       # ONE_JUDGE=1: only gpt-oss-20b
  run llama31_8b meta-llama/Llama-3.1-8B-Instruct rubric 23000 0.15 --max_model_len 2048
  run gemma3_27b google/gemma-3-27b-it rubric 66000 0.45 --max_model_len 2048
  run qwen3_32b Qwen/Qwen3-32B rubric 90000 0.6 --no_think --max_model_len 2048
)
wait
echo "ALL_DONE $TAG $(date)"
