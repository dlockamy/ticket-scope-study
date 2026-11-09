#!/bin/bash
# usage: run-team-round.sh <H0|H1|H2> <rep> <tag>
set -u
ARM=$1; REP=$2; TAG=$3; B=$HOME/study-mfe/s2/bin; export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1
bash $B/field-restore.sh >/dev/null 2>&1 || { echo "RESTORE FAILED"; exit 1; }
source $B/jk.sh
docker run --rm --privileged alpine date -s "@$(date +%s)" >/dev/null 2>&1
SK0=$(( $(date +%s) - $(docker exec study-jenkins date +%s) ))
jk_settle 120
RM=$($B/new-team-run2.sh mono $ARM $REP $TAG); RU=$($B/new-team-run2.sh multi $ARM $REP $TAG)
launch() { local R=$1 D=$2; ID=$(basename $R); mkdir -p $R/work/$D; ( cd $R/work/$D; perl -e 'alarm shift; exec @ARGV' 1500 claude -p --model claude-sonnet-5-5 --output-format json --setting-sources project --strict-mcp-config \
  --allowedTools Bash Read Edit Write Glob Grep --disallowedTools WebFetch WebSearch Agent Skill --max-turns 150 "$(bash $B/brief-team2.sh $ID $D)" > $R/agent-$D.json 2> $R/agent-$D.err ); }
for R in $RM $RU; do launch $R dev-a & launch $R dev-b & done; wait
jk_settle 180
SK1=$(( $(date +%s) - $(docker exec study-jenkins date +%s) ))
for R in $RM $RU; do mkdir -p $HOME/study-mfe/s2/results/$(basename $R); echo "{\"skew_start_s\":$SK0,\"skew_end_s\":$SK1}" > $HOME/study-mfe/s2/results/$(basename $R)/skew.json; bash $B/finish-team2.sh $(basename $R); done
