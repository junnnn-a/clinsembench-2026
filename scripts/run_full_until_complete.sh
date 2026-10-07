#!/usr/bin/env bash
# supervisor: after run_full.sh and the mop-up finish, re-run run_full.sh (every step is resumable / skips
# finished outputs) until all expected outputs exist. Needed because jobs on the shared GPU fail with OOM.
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
complete() {
  for c in iu mimic; do
    for m in lexical bertscore f1chexbert srrbert radgraph ratescore temporal radcliq green; do
      [ -f results/2_full_$c/scores/$m.csv ] || { echo "missing $c $m"; return 1; }
    done
    n=$(($(wc -l < data/pairs/full_${c}_all.csv) - 1))
    k=$( [ -f results/2_full_$c/scores/crimson.csv ] && python3 -c "import csv,sys; csv.field_size_limit(10**9); print(sum(1 for _ in csv.reader(open('results/2_full_$c/scores/crimson.csv')))-1)" || echo 0 )
    [ "$k" -ge "$n" ] || { echo "missing $c crimson ($k/$n)"; return 1; }
    for j in gptoss_20b llama31_8b gemma3_27b qwen3_32b; do
      [ -f results/2_full_$c/judges/${j}__rubric.csv ] || { echo "missing $c judge $j"; return 1; }
    done
  done
  for j in gptoss_20b gemma3_27b; do [ -f results/2_full_iu/judges/${j}__errors.csv ] || { echo "missing iu errors $j"; return 1; }; done
  return 0
}
until grep -q "ALL_DONE\|FATAL" logs/run_full.log; do sleep 120; done
until grep -q "MOPUP_DONE" logs/run_full_mopup.log; do sleep 120; done
for round in 1 2 3 4; do
  if complete; then echo "COMPLETE $(date)"; exit 0; fi
  echo "=== supervisor round $round $(date)"
  bash scripts/run_full.sh > logs/run_full_round$round.log 2>&1
done
complete && echo "COMPLETE $(date)" || echo "INCOMPLETE after 4 rounds $(date)"
