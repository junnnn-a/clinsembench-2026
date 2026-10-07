#!/usr/bin/env bash
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/gpu_wait.sh; source scripts/env_llm.sh
for attempt in 1 2 3 4; do
  [ -f data/pairs/full_mimicoi_all.csv ] && break
  gpu_wait 26000 43200
  $PY scripts/15_generate_omission_insertion.py --corpus mimic > logs/15_generate_oi_mimic.log 2>&1
  echo "EXIT=$? (attempt $attempt)" >> logs/15_generate_oi_mimic.log
  sleep 20
done
grep -E "^\[|^  |EXIT" logs/15_generate_oi_mimic.log | grep -v "INFO\|WARNING" | tail -14 | cut -c1-320
[ -f data/pairs/full_mimicoi_all.csv ] && bash scripts/run_set.sh mimicoi
echo "OI_DONE $(date)"
