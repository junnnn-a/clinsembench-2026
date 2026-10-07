#!/usr/bin/env bash
# waits for the gpt-oss rerun, then refreshes every full-set analysis and the figures (CPU only).
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
CPY=/opt/conda/envs/clinsev/bin/python
until grep -q "ALL_DONE" logs/run_gptoss_rerun.log; do sleep 60; done
for c in iu mimic; do
  $CPY scripts/8_analyze_factorial.py --pairs data/pairs/full_${c}_all.csv --scores results/2_full_$c/scores results/2_full_$c/judges --out results/2_full_$c/analysis --n_boot 1000 > logs/8_analyze_full_$c.log 2>&1
  $CPY scripts/11_judge_cells.py --pairs data/pairs/full_${c}_all.csv --judges results/2_full_$c/judges --out results/2_full_$c/analysis --n_boot 1000 > logs/11_judge_cells_full_$c.log 2>&1
  envs/llm/bin/python scripts/14_extended_analysis.py --corpus $c --n_boot 500 > logs/14_extended_analysis_$c.log 2>&1
done
$CPY scripts/17_make_figures.py > logs/17_make_figures.log 2>&1
echo "REANALYZE_DONE $(date)"
