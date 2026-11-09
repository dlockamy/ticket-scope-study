#!/bin/bash
# usage: new-team-run2.sh <mono|multi> <H0|H1|H2> <rep> <tag>   two developers, one ticket (C3, complete list), split on the board
set -eu
TOPO=$1; ARM=$2; REP=$3; TAG=$4; B=$HOME/study-mfe/s2; CH=${TEAM_CHANGE:-C3}
ID=$TAG-T-$ARM-$TOPO-r$REP; R=$B/runs/$ID; rm -rf $R; mkdir -p $R/work
case $ARM in H0) MSG=false; HO=false;; H1) MSG=true; HO=false;; H2) MSG=false; HO=true;; esac
perl -MTime::HiRes=time -e 'printf "%d\n", time*1000' > $R/start_ms
jq -n --arg r $ID --arg t $TOPO --arg a $ARM --argjson rep $REP --arg tag $TAG --arg ch $CH --argjson msg $MSG --argjson ho $HO --argjson ms $(cat $R/start_ms) \
  '{run:$r,topology:$t,mode:"team",change:$ch,arm:$a,rep:$rep,tag:$tag,model:"claude-sonnet-5-5",devs:["dev-a","dev-b"],msg:$msg,handoff:$ho,start_ms:$ms}' > $R/meta.json
python3 $B/bin/gen.py $TOPO $CH A3 $R > /dev/null
sed -i '' 's/Assignee: you/Assignees: dev-a owns sub-tasks 1 and 2, dev-b owns sub-tasks 3 and 4 (see the board)/' $R/ticket.md
if [ $TOPO = mono ]; then RC=(mono mono mono mono); else RC=(contracts billing shell reports); fi
python3 - $R $CH "${RC[@]}" <<'PY'
import json, sys
R = sys.argv[1]; ch = sys.argv[2]; rc = sys.argv[3:]
if ch == 'C4': titles = ['billingUrl value changes to the versioned address (shared contract; release per the team rules)', 'billing app adopts the new contract release', 'core shell adopts the new contract release', 'reports app adopts the new contract release']
else: titles = ['validateApp requires an owner (shared contract; breaking, release per the team rules)', 'billing app passes its owner and adopts the new contract', 'core shell passes its owner and adopts the new contract', 'reports app passes its owner and adopts the new contract']
owners = ['dev-a', 'dev-a', 'dev-b', 'dev-b']
tasks = [dict(id=i + 1, key=f"{'PLAT-104' if ch == 'C4' else 'PLAT-103'}-{i+1}", ticket=('PLAT-104' if ch == 'C4' else 'PLAT-103'), repo=rc[i], title=titles[i], owner=owners[i], state='todo', depends=[] if i == 0 else [1]) for i in range(4)]
json.dump(tasks, open(f'{R}/tasks.json', 'w'))
PY
for d in dev-a dev-b; do printf '#!/bin/bash\nexport ST_RUN=%s ST_ME=%s\nexec bash %s/bin/st-team2.sh "$@"\n' "$R" "$d" "$B" > $R/st-$d; chmod +x $R/st-$d; done
echo $R
