#!/bin/bash
# Helpers for the throwaway Jenkins at 127.0.0.1:18080 (container: study-jenkins). Source this file.
J=http://127.0.0.1:18080
RES=$HOME/study-mfe/results

jk_create() { # name remote scriptPath
  local name=$1 remote=$2 script=$3
  curl -s -o /dev/null -w "create $name -> %{http_code}\n" -H 'Content-Type: application/xml' --data-binary @- "$J/createItem?name=$name" <<EOF
<org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject plugin="workflow-multibranch">
  <actions/><description>$remote [$script]</description><properties/>
  <folderViews class="jenkins.branch.MultiBranchProjectViewHolder"><owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/></folderViews>
  <healthMetrics/>
  <icon class="jenkins.branch.MetadataActionFolderIcon"><owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/></icon>
  <orphanedItemStrategy class="com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy"><pruneDeadBranches>true</pruneDeadBranches><daysToKeep>-1</daysToKeep><numToKeep>-1</numToKeep></orphanedItemStrategy>
  <triggers/><disabled>false</disabled>
  <sources class="jenkins.branch.MultiBranchProject\$BranchSourceList"><data>
    <jenkins.branch.BranchSource>
      <source class="jenkins.plugins.git.GitSCMSource"><id>$name-src</id><remote>$remote</remote><credentialsId></credentialsId>
        <traits><jenkins.plugins.git.traits.BranchDiscoveryTrait/></traits></source>
      <strategy class="jenkins.branch.DefaultBranchPropertyStrategy"><properties class="empty-list"/></strategy>
    </jenkins.branch.BranchSource></data>
    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/></sources>
  <factory class="org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory"><owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/><scriptPath>$script</scriptPath></factory>
</org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject>
EOF
}

jk_last() { curl -s "$J/job/$1/job/main/lastBuild/api/json?tree=number,building,result" 2>/dev/null | jq -r '[.number // 0, .building // false, .result // "none"] | @tsv' 2>/dev/null || echo "0	false	none"; }
jk_num()  { jk_last "$1" | cut -f1; }

# jk_scan job : trigger branch indexing
jk_scan() { curl -s -o /dev/null -X POST "$J/job/$1/build?delay=0"; }

# jk_wait job prev_number [timeout_s] : wait until a build > prev_number has finished; echo its number
jk_wait() {
  local job=$1 prev=$2 to=${3:-300} t=0 n b r
  while [ $t -lt $to ]; do
    IFS=$'\t' read -r n b r < <(jk_last "$job")
    if [ "${n:-0}" -gt "$prev" ] && [ "$b" = false ]; then echo "$n"; return 0; fi
    sleep 2; t=$((t+2))
  done
  echo "TIMEOUT"; return 1
}

jk_cpu_us() { docker exec study-jenkins sh -c "awk '/usage_usec/{print \$2}' /sys/fs/cgroup/cpu.stat"; }

# jk_metrics job number : one JSON line of Jenkins-side facts
jk_metrics() {
  curl -s "$J/job/$1/job/main/$2/wfapi/describe" | jq -c --arg job "$1" '{job:$job, build:(.id|tonumber), status:.status, duration_ms:.durationMillis, queue_ms:.queueDurationMillis, stages_ms:([.stages[]|{(.name):.durationMillis}]|add)}'
}

# jk_build job : trigger the main-branch job directly (re-run without SCM change)
jk_build() { curl -s -o /dev/null -X POST "$J/job/$1/job/main/build?delay=0"; }

# jk_settle : wait until the queue is empty and nothing is running (3 consecutive idle polls)
jk_settle() {
  local idle=0 t=0
  while [ $idle -lt 3 ] && [ $t -lt ${1:-300} ]; do
    local q=$(curl -s -m 5 $J/queue/api/json | jq '.items|length')
    local busy=$(curl -s -m 5 -g "$J/computer/api/json?tree=computer[executors[currentExecutable[url]],oneOffExecutors[currentExecutable[url]]]" | jq '[.computer[]|(.executors[],.oneOffExecutors[])|.currentExecutable.url // empty]|length')
    if [ "$q" = 0 ] && [ "$busy" = 0 ]; then idle=$((idle+1)); else idle=0; fi
    sleep 2; t=$((t+2))
  done
}
# jk_reg_has pkg version : is it in the private registry?
jk_reg_has() { curl -s -m 5 "http://127.0.0.1:4873/$(echo "$1" | sed 's#/#%2f#')" | jq -e --arg v "$2" '.versions[$v]' >/dev/null 2>&1; }
