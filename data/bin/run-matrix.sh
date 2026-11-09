#!/bin/bash
# Runs the queue round by round. A round is VALID only if both agents ran without an API/auth error.
# Pre-flight login probe with retry; invalid rounds are set aside and retried later in the same pass; stops after 3 consecutive invalid rounds.
S=$HOME/study-mfe/s2; fails=0
valid() { # run-name
  [ -s $S/results/$1/summary.json ] && jq -e '(.agent_error != true) and ((.agent_tokens // 0) > 0)' $S/results/$1/summary.json >/dev/null 2>&1; }
probe() { cd /tmp/s2-iso-test && claude -p --model claude-sonnet-5-5 --output-format json --setting-sources project --strict-mcp-config --max-turns 2 "Reply with the single word ok." 2>/dev/null | jq -e '.terminal_reason=="completed"' >/dev/null 2>&1; }
Q=${1:-$S/queue.json}; n=$(jq length $Q)
for i in $(seq 0 $((n-1))); do
  [ -e $S/STOP ] && { echo "$(date +%T) STOP file present"; break; }
  r=$(jq -c ".[$i]" $Q); C=$(jq -r .change <<<"$r"); A=$(jq -r .arm <<<"$r"); P=$(jq -r .rep <<<"$r"); M=$(jq -r .model <<<"$r"); T=$(jq -r .tag <<<"$r")
  valid $T-$C-$A-multi-r$P && valid $T-$C-$A-mono-r$P && continue
  ok=0; for k in $(seq 1 30); do probe && { ok=1; break; }; echo "$(date +%T) login probe failed ($k); waiting 120 s"; sleep 120; done
  [ $ok = 1 ] || { echo "$(date +%T) login never recovered, stopping"; break; }
  echo "$(date +%T) round $i: $T $C $A rep$P $M"
  bash $S/bin/run-round.sh $C $A $P $M $T >> $S/results/matrix.log 2>&1
  if valid $T-$C-$A-multi-r$P && valid $T-$C-$A-mono-r$P; then fails=0
  else fails=$((fails+1)); echo "$(date +%T) round $i INVALID (agent error); set aside (fail $fails)"; for l in multi mono; do [ -d $S/results/$T-$C-$A-$l-r$P ] && mv $S/results/$T-$C-$A-$l-r$P $S/results/invalid-auth/$T-$C-$A-$l-r$P-$(date +%H%M); done; [ $fails -ge 3 ] && { echo "3 consecutive invalid rounds, stopping"; break; }; fi
done
echo "$(date +%T) matrix finished"
