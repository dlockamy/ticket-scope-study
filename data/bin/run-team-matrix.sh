#!/bin/bash
# usage: run-team-matrix.sh <queue.json>   valid = all agents ran without error; invalid rounds set aside and retried in a later pass
S=$HOME/study-mfe/s2; Q=${1:-$S/queue5.json}; fails=0
valid() { [ -s $S/results/$1/summary.json ] && jq -e '.agents_ok == true' $S/results/$1/summary.json >/dev/null 2>&1; }
probe() { cd /tmp/s2-iso-test && claude -p --model claude-sonnet-5-5 --output-format json --setting-sources project --strict-mcp-config --max-turns 2 "Reply with the single word ok." 2>/dev/null | jq -e '.terminal_reason=="completed"' >/dev/null 2>&1; }
n=$(jq length $Q)
for i in $(seq 0 $((n-1))); do
  [ -e $S/STOP ] && { echo "$(date +%T) STOP"; break; }
  r=$(jq -c ".[$i]" $Q); A=$(jq -r .arm <<<"$r"); P=$(jq -r .rep <<<"$r"); T=$(jq -r .tag <<<"$r")
  valid $T-T-$A-multi-r$P && valid $T-T-$A-mono-r$P && continue
  ok=0; for k in $(seq 1 30); do probe && { ok=1; break; }; echo "$(date +%T) login probe failed ($k)"; sleep 120; done
  [ $ok = 1 ] || { echo "$(date +%T) login never recovered"; break; }
  echo "$(date +%T) round $i: $T $A rep$P"
  bash $S/bin/run-team-round.sh $A $P $T >> $S/results/matrix-team.log 2>&1
  if valid $T-T-$A-multi-r$P && valid $T-T-$A-mono-r$P; then fails=0
  else fails=$((fails+1)); echo "$(date +%T) round $i INVALID; set aside ($fails)"; for l in multi mono; do [ -d $S/results/$T-T-$A-$l-r$P ] && mv $S/results/$T-T-$A-$l-r$P $S/results/invalid-auth/$T-T-$A-$l-r$P-$(date +%H%M); done; [ $fails -ge 3 ] && { echo "3 invalid in a row, stop"; break; }; fi
done
echo "$(date +%T) team matrix finished"
