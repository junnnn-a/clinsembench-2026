#!/usr/bin/env bash
# resumable metric scoring queue for the pilots (clinsev env). Skips metrics already written.
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
export HF_HOME=/home/irteam/hf_cache TOKENIZERS_PARALLELISM=false
M=lexical,bertscore,f1chexbert,radgraph,ratescore,temporal,radcliq,srrbert,radeval_bertscore,green
for job in "pilot_iu_S0S1 scores_S0S1 1_pilot_iu" "pilot_iu_S2 scores_S2 1_pilot_iu"; do
  set -- $job
  echo "=== $1 $(date)"
  /opt/conda/envs/clinsev/bin/python scripts/7_score_metrics.py --pairs data/pairs/$1.csv --out results/$3/$2 --metrics $M --batch_size 16 >> logs/7_score_$1.log 2>&1
  echo "EXIT=$?" >> logs/7_score_$1.log
done
echo "ALL_DONE $(date)"
