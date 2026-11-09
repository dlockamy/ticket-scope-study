#!/bin/bash
# usage: finish2.sh <run-id>   (field must still be in the state the agents left it)
set -u
ID=$1; R=$HOME/study-mfe/s2/runs/$ID; O=$HOME/study-mfe/s2/results/$ID; mkdir -p $O
TOPO=$(jq -r .topology $R/meta.json); CH=$(jq -r .change $R/meta.json)
node $HOME/study-mfe/s2/bin/accept2.cjs $TOPO $CH > $O/acceptance.json
python3 $HOME/study-mfe/s2/bin/report2.py $R > $O/report.json
cp $R/events.jsonl $R/prs.json $R/tasks.json $R/ticket.md $R/meta.json $R/agent.json $R/agent.err $O/ 2>/dev/null
for k in $(jq -r '.repos_changed[]' $O/report.json); do
  case $k in mono) d=/tmp/study/mono;; platformkit) d=/tmp/study/external/libs-platform-kit;; shell) d=/tmp/study/multi/apps-core-shell;; billing) d=/tmp/study/multi/apps-sub-route-billing;; reports) d=/tmp/study/multi/apps-sub-route-reports;; contracts) d=/tmp/study/multi/libs-shared-contracts;; esac
  BASE=$(git -C $HOME/study-mfe/s2/snap3/study/${d#/tmp/study/} rev-parse HEAD); git -C $d log $BASE..main --no-merges -p --format='=== %h %s' -- . ':!package-lock.json' > $O/landed-$k.diff 2>/dev/null
done
jq -s '.[0] + {acceptance_pass: .[1].pass, missed: .[1].missed, broken_live: .[1].broken_live, consumers: .[1].consumers, semver_ok: .[1].info.semver_ok, semver_class: .[1].info.semver_class, platformkit_changed: .[1].info.platformkit_changed, failed_checks: [.[1].checks[]? | select(.ok|not) | .name]}' $O/report.json $O/acceptance.json > $O/summary.json
jq -c '{run,finished,acceptance_pass,missed,prs,turnaround_s,rework_events,agent_tokens}' $O/summary.json
