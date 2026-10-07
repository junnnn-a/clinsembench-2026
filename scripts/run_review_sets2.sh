#!/usr/bin/env bash
# 10/7 review, extra sets — third arrangement (docs/13 §6). Sequential, resumable.
#  iualt : fast scorers on all rows (already running/finished); slow scorers (GREEN, RadCliQ, temporal, CRIMSON) on the 602 new S2 rows only,
#          the other rows are identical to the IU set and are copied by 25_merge_iualt.py
#  rate3 : public suite, no GREEN (chest-X-ray-specific, slowest), CRIMSON + gpt-oss-20b
#  rate1 : RaTE-Eval task 1, test split (441 pairs), all scorers + gpt-oss-20b ; rate2: task 2 test, metrics only
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/gpu_wait.sh
export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 NUMEXPR_NUM_THREADS=8
CPY=/opt/conda/envs/clinsev/bin/python
while pgrep -f "^/opt/conda/envs/clinsev/bin/python scripts/7_score_metrics.py --pairs data/pairs/full_iualt_all.csv" > /dev/null; do sleep 30; done
mkdir -p results/2_full_iualts2/scores
for m in green radcliq temporal; do
  [ -f results/2_full_iualts2/scores/$m.csv ] && continue
  gpu_wait 30000 43200
  HF_HOME=/home/irteam/hf_cache TOKENIZERS_PARALLELISM=false $CPY scripts/7_score_metrics.py --pairs data/pairs/full_iualts2_all.csv --out results/2_full_iualts2/scores --metrics $m --batch_size 16 >> logs/7_score_full_iualts2_$m.log 2>&1
done
( source scripts/env_llm.sh
  for attempt in 1 2 3; do
    [ -f results/2_full_iualts2/scores/crimson.csv ] && break
    gpu_wait 30000 43200
    $PY scripts/10_crimson.py --pairs data/pairs/full_iualts2_all.csv --out results/2_full_iualts2/scores --gpu_mem 0.12 > logs/10_crimson_full_iualts2.log 2>&1
  done )
$CPY scripts/25_merge_iualt.py > logs/25_merge_iualt.log 2>&1
echo "IUALT_DONE $(date)"
SKIP_GREEN=1 ONE_JUDGE=1 bash scripts/run_set.sh rate3 > logs/run_set_rate3.log 2>&1
ONE_JUDGE=1 bash scripts/run_set.sh rate1 > logs/run_set_rate1.log 2>&1
NO_LLM=1 bash scripts/run_set.sh rate2 > logs/run_set_rate2.log 2>&1
echo "REVIEW_SETS_DONE $(date)"
