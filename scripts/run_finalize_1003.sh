#!/usr/bin/env bash
# 10/3 finalisation: missing gpt-oss-120b IU rubric (+ OI / mono with gpt-oss-120b), then refresh every analysis and the figures.
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
source scripts/env_llm.sh; source scripts/gpu_wait.sh
CPY=/opt/conda/envs/clinsev/bin/python
run() { # tagset
  local t=$1
  for attempt in 1 2 3 4; do
    [ -f results/2_full_$t/judges/gptoss_120b__rubric.csv ] && return
    gpu_wait 88000 86400 || return
    echo "=== $t gptoss_120b rubric $(date)"
    $PY scripts/9_llm_judge.py --pairs data/pairs/full_${t}_all.csv --out results/2_full_$t/judges --model openai/gpt-oss-120b --tag gptoss_120b --prompt rubric --gpu_mem 0.6 --reasoning low --max_model_len 8192 > logs/9_judge_full_${t}_gptoss_120b_rubric.log 2>&1
    echo "EXIT=$?" >> logs/9_judge_full_${t}_gptoss_120b_rubric.log
    grep -E "^\[gen|EXIT|ValueError" logs/9_judge_full_${t}_gptoss_120b_rubric.log | tail -2 | cut -c1-140; sleep 20
  done
}
run iu; run mimicoi; run mimicmono
for c in iu mimic mimicoi; do
  $CPY scripts/8_analyze_factorial.py --pairs data/pairs/full_${c}_all.csv --scores results/2_full_$c/scores results/2_full_$c/judges --out results/2_full_$c/analysis --n_boot 1000 > logs/8_analyze_full_$c.log 2>&1
  $CPY scripts/11_judge_cells.py --pairs data/pairs/full_${c}_all.csv --judges results/2_full_$c/judges --out results/2_full_$c/analysis --n_boot 1000 > logs/11_judge_cells_full_$c.log 2>&1
done
$CPY scripts/18_analyze_monotonicity.py --tag mimicmono > logs/18_analyze_monotonicity.log 2>&1
for c in iu mimic; do envs/llm/bin/python scripts/14_extended_analysis.py --corpus $c --n_boot 500 > logs/14_extended_analysis_$c.log 2>&1; done
$CPY scripts/17_make_figures.py > logs/17_make_figures.log 2>&1
echo "FINALIZE_DONE $(date)"
