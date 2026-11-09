#!/bin/bash
# usage: run-round.sh <C> <ARM> <REP> <MODEL> <TAG> [clarify]  -- restore field, run mono+multi developers concurrently, score both
set -u
C=$1; ARM=$2; REP=$3; MODEL=$4; TAG=$5; CL=${6:-}
B=$HOME/study-mfe/s2/bin; export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1
bash $B/field-restore3.sh >/dev/null 2>&1 || { echo "RESTORE FAILED"; exit 1; }
source $B/jk.sh
# The Docker VM clock drifts behind the host (seen: 300 s, which turned every CI wait into ~5 min). Sync it, record skew at both ends.
docker run --rm --privileged alpine date -s "@$(date +%s)" >/dev/null 2>&1
SK0=$(( $(date +%s) - $(docker exec study-jenkins date +%s) ))
jk_settle 120
RM=$($B/new-run3.sh mono $C $ARM $REP $MODEL $TAG $CL); RU=$($B/new-run3.sh multi $C $ARM $REP $MODEL $TAG $CL)
bash $B/run-agent.sh $RM & bash $B/run-agent.sh $RU & wait
jk_settle 180
SK1=$(( $(date +%s) - $(docker exec study-jenkins date +%s) ))
for R in $RM $RU; do mkdir -p $HOME/study-mfe/s2/results/$(basename $R); echo "{\"skew_start_s\":$SK0,\"skew_end_s\":$SK1}" > $HOME/study-mfe/s2/results/$(basename $R)/skew.json; done
for R in $RM $RU; do bash $B/finish3.sh $(basename $R); done
