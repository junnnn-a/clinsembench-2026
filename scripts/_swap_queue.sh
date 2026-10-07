#!/usr/bin/env bash
# one-off helper (10/7): when the running gpt-oss-20b errors run on mimicmono has written its output, replace queue v1 by v2
cd /home/irteam/junah-data-1/ARR_10/2_ClimSemBench
while [ ! -f results/2_full_mimicmono/judges/gptoss_20b__errors.csv ]; do sleep 20; done
sleep 5
kill 2667122 2>/dev/null
sleep 2
ps -eo pid,args | grep "9_llm_judge.py --pairs data/pairs/full_mimicmono_all.csv" | grep -v grep | awk '{print $1}' | xargs -r kill
sleep 20
nohup bash scripts/run_review_1007b.sh >> logs/run_review_1007.log 2>&1 &
echo "swapped $(date)"
