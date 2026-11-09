#!/bin/bash
set -u
ID=$1; R=$HOME/study-mfe/s2/runs/$ID; O=$HOME/study-mfe/s2/results/$ID; mkdir -p $O
TOPO=$(jq -r .topology $R/meta.json)
CH=$(jq -r .change $R/meta.json); node $HOME/study-mfe/s2/bin/accept2.cjs $TOPO $CH > $O/acceptance.json
python3 $HOME/study-mfe/s2/bin/report-team2.py $R > $O/report.json
cp $R/events.jsonl $R/prs.json $R/meta.json $R/tasks.json $R/ticket.md $R/msgs.jsonl $R/handoffs.jsonl $R/agent-dev-a.json $R/agent-dev-b.json $O/ 2>/dev/null
for k in $(jq -r '[.pr_detail[].repo]|unique[]' $O/report.json); do
  case $k in mono) d=/tmp/study/mono;; platformkit) d=/tmp/study/external/libs-platform-kit;; shell) d=/tmp/study/multi/apps-core-shell;; billing) d=/tmp/study/multi/apps-sub-route-billing;; reports) d=/tmp/study/multi/apps-sub-route-reports;; contracts) d=/tmp/study/multi/libs-shared-contracts;; esac
  BASE=$(git -C $HOME/study-mfe/s2/snap/study/${d#/tmp/study/} rev-parse HEAD); git -C $d log $BASE..main --no-merges -p --format='=== %h %s' -- . ':!package-lock.json' > $O/landed-$k.diff 2>/dev/null
done
jq -s '.[0] + {acceptance_pass: .[1].pass, missed: .[1].missed, consumers: .[1].consumers, semver_class: .[1].info.semver_class, semver_ok: .[1].info.semver_ok, agents_ok: ((.[0].agent_errors|length)==0)}' $O/report.json $O/acceptance.json > $O/summary.json
jq -c '{run,acceptance_pass,missed,prs,makespan_s,merge_conflicts,msgs_total,handoffs_posted,agents_ok}' $O/summary.json
