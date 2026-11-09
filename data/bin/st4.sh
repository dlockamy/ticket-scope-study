#!/bin/bash
# st — stand-in for "GitHub + ticket tracker" for developer agents. Every action is timestamped into the run's event log.
# usage: st <command>   (run dir comes from $ST_RUN, set by the per-run wrapper)
set -u
RUN=${ST_RUN:?ST_RUN not set}
source $HOME/study-mfe/s2/bin/jk.sh
TOPO=$(jq -r .topology $RUN/meta.json)
ms() { perl -MTime::HiRes=time -e 'printf "%d\n", time*1000'; }
ev() { # name [json-object-string]
  jq -cn --arg e "$1" --argjson t "$(ms)" --argjson d "${2:-{\}}" '{ts:$t,event:$e} + $d' >> $RUN/events.jsonl; }
origin_of() { case $1 in
  mono) echo /tmp/study/mono;; platformkit) echo /tmp/study/external/libs-platform-kit;;
  shell) echo /tmp/study/multi/apps-core-shell;; billing) echo /tmp/study/multi/apps-sub-route-billing;; reports) echo /tmp/study/multi/apps-sub-route-reports;; contracts) echo /tmp/study/multi/libs-shared-contracts;;
  *) return 1;; esac; }
ci_of() { case $1 in mono) echo mono-ci;; platformkit) echo ext-platformkit-ci;; shell) echo multi-shell-ci;; billing) echo multi-billing-ci;; reports) echo multi-reports-ci;; contracts) echo multi-contracts-ci;; esac; }
cd_of() { ci_of "$1" | sed 's/-ci$/-cd/'; }
valid_key() { if [ "$TOPO" = mono ]; then case $1 in mono|platformkit) return 0;; esac; else case $1 in shell|billing|reports|contracts|platformkit) return 0;; esac; fi; return 1; }
need_key() { valid_key "$1" || { echo "unknown repo key '$1' (see: st repos)" >&2; exit 2; }; }
pr_get() { jq -r --argjson n "$1" ".[] | select(.id==\$n) | .$2" $RUN/prs.json; }
pr_set() { jq --argjson n "$1" --arg k "$2" --argjson v "$3" 'map(if .id==$n then .[$k]=$v else . end)' $RUN/prs.json > $RUN/prs.tmp && mv $RUN/prs.tmp $RUN/prs.json; }
infra_fail() { curl -s -m 10 "$1" | grep -qE "Error cloning remote repo|unable to open loose object|not our ref"; }
main_build_for() { # job sha [minnum] -> compact json of the main-branch build that built sha (or null)
  curl -s -g -m 10 "$J/job/$1/job/main/api/json?tree=builds[number,building,result,duration,timestamp,actions[lastBuiltRevision[SHA1]]]" 2>/dev/null \
   | jq -c --arg sha "$2" --argjson min "${3:-0}" '[.builds[]? | select(.number > $min) | select(any(.actions[]?; .lastBuiltRevision.SHA1? == $sha))] | .[0] // null' 2>/dev/null; }
branch_build_for() { # job branch sha [minnum]
  curl -s -g -m 10 "$J/job/$1/job/$2/api/json?tree=builds[number,building,result,duration,timestamp,actions[lastBuiltRevision[SHA1]]]" 2>/dev/null \
   | jq -c --arg sha "$3" --argjson min "${4:-0}" '[.builds[]? | select(.number > $min) | select(any(.actions[]?; .lastBuiltRevision.SHA1? == $sha))] | .[0] // null' 2>/dev/null; }
size_of() { # workdir branch -> json {files,add,del,lock_add,lock_del,commits}
  (cd "$1" && git fetch -q origin main 2>/dev/null; git diff --numstat origin/main..."$2" | awk '
     { if ($3 ~ /package-lock\.json$/) { la+=$1; ld+=$2 } else { a+=$1; d+=$2; f++ } lf++ }
     END { printf "{\"files\":%d,\"add\":%d,\"del\":%d,\"lock_add\":%d,\"lock_del\":%d}", f, a, d, la, ld }' \
   | jq -c --argjson c "$(cd "$1" && git rev-list --count origin/main.."$2")" '. + {commits:$c}'); }

cmd=${1:-help}; shift || true
case $cmd in
  help) cat <<'EOF'
st ticket                          show the ticket assigned to you
st repos                           list repositories you can work in
st clone <key>                     clone a repository into your work area
st task add [--repo <key>] "<title>"   record a sub-task (ticket breakdown)
st task start|done <n>             update a sub-task
st pr open <key> <branch> "<title>"    push your branch and open a PR (starts CI)
st pr wait <n>                     wait for CI on the PR's latest push
st pr push <n>                     push new commits to the PR branch (re-runs CI)
st pr merge <n>                    merge a PR whose latest CI run is green (starts CD)
st deploy wait <n>                 wait for CI/CD on main after merging PR n
st status                          your PRs and tasks
st done "<summary>"                declare the ticket finished
st blocked "<reason>"              give up (nobody is available to answer questions)
Branch names: lowercase letters, digits and hyphens only.
EOF
    if [ "$(jq -r '.epic // false' $RUN/meta.json)" = true ]; then echo 'st ticket <id>                     show a child ticket of the epic'; echo 'st ticket done <id>                mark a child ticket done (when its change is live)'; fi
    if [ "$(jq -r '.catalog // "none"' $RUN/meta.json)" != none ]; then echo 'st deps <package>                  list the repositories that depend on a package (team dependency catalog)'; fi
    if [ "$(jq -r '.audit // false' $RUN/meta.json)" = true ]; then echo 'st audit                           run the compliance check across all app repositories (main branches)'; fi
    if [ "$(jq -r '.clarify // false' $RUN/meta.json)" = true ]; then echo 'st ask "<question>"                ask the ticket requester a clarifying question (max 3)'; fi
  ;;
  ticket)
    if [ "${1:-}" = done ]; then id=${2:?id}; [ -f $RUN/children/$id.md ] || { echo "unknown child ticket $id" >&2; exit 2; }; ev child_done "{\"child\":\"$id\"}"; echo "ticket $id marked done"
    elif [ -n "${1:-}" ]; then [ -f $RUN/children/$1.md ] || { echo "unknown ticket $1" >&2; exit 2; }; ev child_opened "{\"child\":\"$1\"}"; cat $RUN/children/$1.md
    else cat $RUN/ticket.md; fi;;
  audit) [ "$(jq -r '.audit // false' $RUN/meta.json)" = true ] || { echo "unknown command: audit (try: st help)" >&2; exit 2; }
    out=$(python3 $HOME/study-mfe/s2/bin/audit.py $TOPO); echo "$out"; ev audit "$(jq -cn --arg o "$out" '{violations:($o|[match("VIOLATION";"g")]|length)}')";;
  deps) pkg=${1:-}; [ "$(jq -r '.catalog // "none"' $RUN/meta.json)" != none ] || { echo "unknown command: deps (try: st help)" >&2; exit 2; }
    [ -n "$pkg" ] || { echo "usage: st deps <package>" >&2; exit 2; }
    ev deps_query "$(jq -cn --arg p "$pkg" '{pkg:$p}')"
    jq -r --arg p "$pkg" 'if .[$p] then "Consumers of \($p) (dependency catalog, maintained by the teams):\n" + (.[$p] | map("  " + .) | join("\n")) else "No catalog entry for \($p)." end' $RUN/catalog.json;;
  ask) [ "$(jq -r '.clarify // false' $RUN/meta.json)" = true ] || { echo "unknown command: ask (try: st help)" >&2; exit 2; }
    q="$*"; [ -n "$q" ] || { echo 'usage: st ask "<question>"' >&2; exit 2; }
    n=$(grep -c '"event":"ask"' $RUN/events.jsonl 2>/dev/null || true); n=${n:-0}
    if [ "$n" -ge 3 ]; then echo "The requester has no more time for questions. Use your judgement."; ev ask_refused '{}'; exit 0; fi
    a=$(python3 $HOME/study-mfe/s2/bin/responder.py $RUN/key.json "$q"); ev ask "$(jq -cn --arg q "$q" --arg a "$a" '{q:$q,a:$a}')"; echo "$a";;
  repos)
    if [ "$TOPO" = mono ]; then cat <<'EOF'
key          repository               description
mono         homelab-mfe-monorepo     Micro-frontend platform: core shell, billing and reports sub-routes, shared contracts (apps/, libs/)
platformkit  libs-platform-kit        Shared platform utilities library, published to the private registry (@studio/platform-kit)
EOF
    else cat <<'EOF'
key          repository               description
shell        apps-core-shell          Core shell page for the micro-frontend platform
billing      apps-sub-route-billing   Billing sub-route micro-frontend
reports      apps-sub-route-reports   Reports sub-route micro-frontend
contracts    libs-shared-contracts    Shared configuration contract library, published to the private registry (@mfe/shared-contracts)
platformkit  libs-platform-kit        Shared platform utilities library, published to the private registry (@studio/platform-kit)
EOF
    fi;;
  clone) k=${1:?key}; need_key $k; d=$RUN/work/$k
    if [ -d $d ]; then echo "already cloned: $d"; exit 0; fi
    mkdir -p $RUN/work && git clone -q --no-hardlinks "$(origin_of $k)" $d && git -C $d config remote.origin.pushurl "disabled-use-st-pr-open" && git -C $d config user.name "dev-$(basename $RUN)" && git -C $d config user.email "dev@study.local"
    ev clone "{\"repo\":\"$k\"}"; echo "cloned $k -> $d";;
  task)
    sub=${1:?}; shift; [ -f $RUN/tasks.json ] || echo '[]' > $RUN/tasks.json
    case $sub in
      add) repo=""; if [ "${1:-}" = "--repo" ]; then repo=$2; shift 2; fi; title=${1:?title}
        n=$(jq 'length+1' $RUN/tasks.json); jq --argjson n $n --arg t "$title" --arg r "$repo" '. + [{id:$n,title:$t,repo:$r,state:"todo"}]' $RUN/tasks.json > $RUN/t.tmp && mv $RUN/t.tmp $RUN/tasks.json
        ev task_added "$(jq -cn --argjson n $n --arg t "$title" --arg r "$repo" '{task:$n,title:$t,repo:$r}')"; echo "task $n added";;
      start|done) n=${1:?n}; st=$([ $sub = start ] && echo doing || echo done)
        jq --argjson n $n --arg s $st 'map(if .id==$n then .state=$s else . end)' $RUN/tasks.json > $RUN/t.tmp && mv $RUN/t.tmp $RUN/tasks.json; ev task_$sub "{\"task\":$n}"; echo "task $n $st";;
    esac;;
  pr)
    sub=${1:?}; shift; [ -f $RUN/prs.json ] || echo '[]' > $RUN/prs.json
    case $sub in
      open) k=${1:?key}; b=${2:?branch}; title=${3:?title}; need_key $k
        [[ $b =~ ^[a-z0-9][a-z0-9-]*$ ]] || { echo "bad branch name '$b'" >&2; exit 2; }
        w=$RUN/work/$k; [ -d $w ] || { echo "clone $k first" >&2; exit 2; }
        git -C $w rev-parse --verify -q "$b" >/dev/null || { echo "branch '$b' does not exist in $w" >&2; exit 2; }
        git -C $w push -q "$(origin_of $k)" "$b:refs/heads/$b" 2>&1 | tail -2
        head=$(git -C $w rev-parse "$b"); sz=$(size_of $w "$b"); id=$(jq 'length+1' $RUN/prs.json)
        jq --argjson id $id --arg k $k --arg b "$b" --arg t "$title" --arg h "$head" --argjson sz "$sz" --argjson ts $(ms) \
          '. + [{id:$id,repo:$k,branch:$b,title:$t,head:$h,opened_ts:$ts,size:$sz,ci:null,merged_ts:null}]' $RUN/prs.json > $RUN/p.tmp && mv $RUN/p.tmp $RUN/prs.json
        jk_scan "$(ci_of $k)"; ev pr_opened "$(jq -cn --argjson id $id --arg k $k --arg b "$b" --argjson sz "$sz" '{pr:$id,repo:$k,branch:$b,size:$sz}')"
        echo "PR #$id opened on $k ($b): $(echo $sz | jq -r '"\(.files) files +\(.add)/-\(.del) lines (+\(.lock_add)/-\(.lock_del) lockfile), \(.commits) commit(s)"'); CI started";;
      push) n=${1:?}; k=$(pr_get $n repo); b=$(pr_get $n branch); w=$RUN/work/$k
        git -C $w push -q "$(origin_of $k)" "$b:refs/heads/$b" 2>&1 | tail -2; head=$(git -C $w rev-parse "$b"); sz=$(size_of $w "$b")
        pr_set $n head "\"$head\""; pr_set $n size "$sz"; pr_set $n ci null; jk_scan "$(ci_of $k)"
        ev pr_updated "$(jq -cn --argjson id $n --argjson sz "$sz" '{pr:$id,size:$sz}')"; echo "PR #$n updated; CI re-started";;
      wait) n=${1:?}; k=$(pr_get $n repo); b=$(pr_get $n branch); h=$(pr_get $n head); ci=$(ci_of $k); t0=$(ms); minnum=0; retries=0
        until [ $(( $(ms) - t0 )) -gt 600000 ]; do
          bb=$(branch_build_for $ci $b $h $minnum)
          if [ "$bb" != null ] && [ -n "$bb" ] && [ "$(echo "$bb" | jq -r .building)" = false ]; then
            res=$(echo "$bb" | jq -r .result); dur=$(echo "$bb" | jq -r .duration); num=$(echo "$bb" | jq -r .number)
            if [ "$res" != SUCCESS ] && [ $retries -lt 2 ] && infra_fail "$J/job/$ci/job/$b/$num/consoleText"; then retries=$((retries+1)); minnum=$num; ev infra_retry "$(jq -cn --argjson pr $n --arg j $ci '{pr:$pr,job:$j,kind:"ci"}')"; curl -s -o /dev/null -X POST "$J/job/$ci/job/$b/build?delay=0"; sleep 3; continue; fi
            pr_set $n ci "\"$res\""; ev ci_result "$(jq -cn --argjson pr $n --arg r $res --argjson d $dur --arg sha $h --argjson w $(( $(ms) - t0 )) '{pr:$pr,result:$r,build_ms:$d,waited_ms:$w,sha:$sha}')"
            echo "CI for PR #$n: $res (build ran ${dur} ms)"
            if [ "$res" != SUCCESS ]; then echo "--- console tail ---"; curl -s -m 10 "$J/job/$ci/job/$b/$num/consoleText" | grep -v '^\[Pipeline\]' | tail -40 | cut -c1-200; exit 1; fi
            exit 0; fi
          sleep 3; done
        echo "timed out waiting for CI" >&2; exit 3;;
      merge) n=${1:?}; k=$(pr_get $n repo); b=$(pr_get $n branch); h=$(pr_get $n head); title=$(pr_get $n title); o=$(origin_of $k)
        [ "$(pr_get $n ci)" = SUCCESS ] || { echo "CI is not green for the latest push of PR #$n (run: st pr wait $n)" >&2; exit 1; }
        ci=$(ci_of $k); cdj=$(cd_of $k); ci_prev=$(jk_num $ci); cd_prev=$(jk_num $cdj)
        ( cd $o && git checkout -q main && GIT_AUTHOR_NAME=maintainer GIT_AUTHOR_EMAIL=m@study.local GIT_COMMITTER_NAME=maintainer GIT_COMMITTER_EMAIL=m@study.local git merge -q --no-ff -m "Merge PR #$n: $title" "refs/heads/$b" ) 2>&1 | tail -3
        [ "${PIPESTATUS[0]}" = 0 ] || { echo "merge failed (main moved? rebase your branch onto origin/main and 'st pr push $n')" >&2; ( cd $o && git merge --abort 2>/dev/null ); exit 1; }
        msha=$(git -C $o rev-parse main); pr_set $n merge_sha "\"$msha\""; pr_set $n merged_ts $(ms); pr_set $n ci_prev $ci_prev; pr_set $n cd_prev $cd_prev
        jk_scan $ci; jk_scan $cdj; ev pr_merged "$(jq -cn --argjson pr $n --arg sha $msha '{pr:$pr,merge_sha:$sha}')"; echo "PR #$n merged to main ($msha); CI/CD started";;
      list) jq -r '.[] | "#\(.id) \(.repo) \(.branch) ci=\(.ci // "-") merged=\(if .merged_ts then "yes" else "no" end)  \(.title)"' $RUN/prs.json;;
    esac;;
  deploy)
    [ "${1:-}" = wait ] || exit 2; n=${2:?}; k=$(pr_get $n repo); sha=$(pr_get $n merge_sha); ci=$(ci_of $k); cdj=$(cd_of $k); t0=$(ms); cmin=0; imin=0; cret=0; iret=0
    [ -n "$sha" ] && [ "$sha" != null ] || { echo "PR #$n is not merged" >&2; exit 2; }
    until [ $(( $(ms) - t0 )) -gt 600000 ]; do
      cb=$(main_build_for $cdj $sha $cmin); ib=$(main_build_for $ci $sha $imin)
      if [ "$cb" != null ] && [ -n "$cb" ] && [ "$ib" != null ] && [ -n "$ib" ] && [ "$(echo "$cb" | jq -r .building)" = false ] && [ "$(echo "$ib" | jq -r .building)" = false ]; then
        cr=$(echo "$cb" | jq -r .result); ir=$(echo "$ib" | jq -r .result)
        cn=$(echo "$cb" | jq -r .number); in_=$(echo "$ib" | jq -r .number)
        if [ "$cr" != SUCCESS ] && [ $cret -lt 2 ] && infra_fail "$J/job/$cdj/job/main/$cn/consoleText"; then cret=$((cret+1)); cmin=$cn; ev infra_retry "$(jq -cn --arg j $cdj '{job:$j,kind:"cd"}')"; curl -s -o /dev/null -X POST "$J/job/$cdj/job/main/build?delay=0"; sleep 3; continue; fi
        if [ "$ir" != SUCCESS ] && [ $iret -lt 2 ] && infra_fail "$J/job/$ci/job/main/$in_/consoleText"; then iret=$((iret+1)); imin=$in_; ev infra_retry "$(jq -cn --arg j $ci '{job:$j,kind:"ci_main"}')"; curl -s -o /dev/null -X POST "$J/job/$ci/job/main/build?delay=0"; sleep 3; continue; fi
        ev deploy_result "$(jq -cn --argjson pr $n --arg cr $cr --arg ir $ir --argjson cd_ms "$(echo "$cb" | jq .duration)" --argjson ci_ms "$(echo "$ib" | jq .duration)" --argjson w $(( $(ms) - t0 )) '{pr:$pr,cd_result:$cr,ci_main_result:$ir,cd_ms:$cd_ms,ci_main_ms:$ci_ms,waited_ms:$w}')"
        echo "main after PR #$n: CI=$ir CD=$cr (CD ran $(echo "$cb" | jq -r .duration) ms)"
        case $k in contracts|platformkit) echo "registry now has: $(curl -s -m 5 http://127.0.0.1:4873/$( [ $k = contracts ] && echo @mfe%2fshared-contracts || echo @studio%2fplatform-kit) | jq -r '.versions|keys|join(", ")')";; esac
        if [ "$cr" != SUCCESS ] || [ "$ir" != SUCCESS ]; then echo "--- CD console tail ---"; curl -s -m 10 "$J/job/$cdj/job/main/$(echo "$cb" | jq -r .number)/consoleText" | grep -v '^\[Pipeline\]' | tail -40 | cut -c1-200; exit 1; fi
        exit 0; fi
      sleep 3; done
    echo "timed out waiting for main builds" >&2; exit 3;;
  status) jq -r '.[] | "PR #\(.id) \(.repo) \(.branch): ci=\(.ci // "-") merged=\(if .merged_ts then "yes" else "no" end)"' $RUN/prs.json 2>/dev/null; jq -r '.[] | "task \(.id) [\(.state)] \(.repo) \(.title)"' $RUN/tasks.json 2>/dev/null;;
  done) if [ -d $RUN/children ]; then open=""; for f in $RUN/children/*.md; do id=$(basename $f .md); grep '"event":"child_done"' $RUN/events.jsonl 2>/dev/null | grep -q "\"child\":\"$id\"" || open="$open $id"; done
      if [ -n "$open" ]; then echo "The epic cannot be closed: child tickets still open:$open" >&2; ev done_refused "$(jq -cn --arg o "$open" '{open:$o}')"; exit 1; fi; fi
    ev done "$(jq -cn --arg s "${1:-}" '{summary:$s}')"; echo "ticket marked done";;
  blocked) ev blocked "$(jq -cn --arg s "${1:-}" '{reason:$s}')"; echo "ticket marked blocked";;
  *) echo "unknown command: $cmd (try: st help)" >&2; exit 2;;
esac
