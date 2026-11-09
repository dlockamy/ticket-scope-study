#!/bin/bash
# usage: run-agent.sh <run-dir>  -- runs one headless developer to completion (or the 25 min cap); never fails the caller
R=$1; MODEL=$(jq -r .model $R/meta.json)
cd $R/work
perl -e 'alarm shift; exec @ARGV' 1500 claude -p --model $MODEL --output-format json --setting-sources project --strict-mcp-config \
  --allowedTools Bash Read Edit Write Glob Grep --disallowedTools WebFetch WebSearch Agent Skill --max-turns 150 \
  "$(cat $R/brief.md)" > $R/agent.json 2> $R/agent.err
echo "exit=$?" >> $R/agent.err
exit 0
