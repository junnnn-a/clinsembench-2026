#!/usr/bin/env bash
# mop-up for the full metric scoring: after the parallel wave exits, re-run every metric group that is still
# missing (OOM under GPU sharing), one at a time, waiting for free GPU memory. Repeats up to 5 rounds.
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/gpu_wait.sh
CPY=/opt/conda/envs/clinsev/bin/python
while [ "$(ps -eo args | grep -c '[7]_score_metrics.py --pairs data/pairs/full')" -gt 0 ]; do sleep 60; done
need() { case $1 in green) echo 30000;; bertscore) echo 16000;; *) echo 12000;; esac; }
for round in 1 2 3 4 5; do
  missing=0
  for c in iu mimic; do
    for m in lexical bertscore f1chexbert srrbert radgraph ratescore temporal radcliq green; do
      [ -f results/2_full_$c/scores/$m.csv ] && continue
      missing=1
      gpu_wait $(need $m) 21600 || continue
      echo "=== round $round $c $m $(date)"
      HF_HOME=/home/irteam/hf_cache TOKENIZERS_PARALLELISM=false $CPY scripts/7_score_metrics.py --pairs data/pairs/full_${c}_all.csv \
         --out results/2_full_$c/scores --metrics $m --batch_size 16 >> logs/7_score_full_${c}_mopup.log 2>&1
      grep -E "^\[done\]|FAILED" logs/7_score_full_${c}_mopup.log | tail -1 | cut -c1-160
    done
  done
  [ $missing -eq 0 ] && break
done
echo "MOPUP_DONE $(date)"; ls results/2_full_iu/scores results/2_full_mimic/scores
