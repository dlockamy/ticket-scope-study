#!/bin/bash
# st (team edition) — like st-core.sh, plus identities, a shared board, a message channel and locking.
# env: ST_RUN (shared run dir), ST_ME (this developer's id)
set -u
RUN=${ST_RUN:?ST_RUN not set}; ME=${ST_ME:?ST_ME not set}
source $HOME/study-mfe/s2/bin/jk.sh
TOPO=$(jq -r .topology $RUN/meta.json); MODE=$(jq -r .mode $RUN/meta.json)
ms() { perl -MTime::HiRes=time -e 'printf "%d\n", time*1000'; }
ev() { jq -cn --arg e "$1" --arg w "$ME" --argjson t "$(ms)" --argjson d "${2:-{\}}" '{ts:$t,who:$w,event:$e} + $d' >> $RUN/events.jsonl; }
lock() { local n=0; while ! mkdir "$RUN/.lock-$1" 2>/dev/null; do sleep 0.2; n=$((n+1)); [ $n -gt 300 ] && rm -rf "$RUN/.lock-$1"; done; }
unlock() { rmdir "$RUN/.lock-$1" 2>/dev/null; }
origin_of() { case $1 in
  mono) echo /tmp/study/mono;; platformkit) echo /tmp/study/external/libs-platform-kit;;
  shell) echo /tmp/study/multi/apps-core-shell;; billing) echo /tmp/study/multi/apps-sub-route-billing;; reports) echo /tmp/study/multi/apps-sub-route-reports;; contracts) echo /tmp/study/multi/libs-shared-contracts;;
  *) return 1;; esac; }
ci_of() { case $1 in mono) echo mono-ci;; platformkit) echo ext-platformkit-ci;; shell) echo multi-shell-ci;; billing) echo multi-billing-ci;; reports) echo multi-reports-ci;; contracts) echo multi-contracts-ci;; esac; }
cd_of() { ci_of "$1" | sed 's/-ci$/-cd/'; }
valid_key() { if [ "$TOPO" = mono ]; then case $1 in mono|platformkit) return 0;; esac; else case $1 in shell|billing|reports|contracts|platformkit) return 0;; esac; fi; return 1; }
need_key() { valid_key "$1" || { echo "unknown repo key '$1' (see: st repos)" >&2; exit 2; }; }
pr_get() { jq -r --argjson n "$1" ".[] | select(.id==\$n) | .$2" $RUN/prs.json; }
pr_set() { lock prs; jq --argjson n "$1" --arg k "$2" --argjson v "$3" 'map(if .id==$n then .[$k]=$v else . end)' $RUN/prs.json > $RUN/prs.$ME.tmp && mv $RUN/prs.$ME.tmp $RUN/prs.json; unlock prs; }
infra_fail() { curl -s -m 10 "$1" | grep -qE "Error cloning remote repo|unable to open loose object|not our ref"; }
main_build_for() { # job sha [min]: a finished main build whose revision is sha, or (ORIGIN_FOR_WAIT set) a descendant of sha: later merges supersede earlier ones
  local j=$1 sha=$2 min=${3:-0} list exact row n s
  list=$(curl -s -g -m 10 "$J/job/$j/job/main/api/json?tree=builds[number,building,result,duration,timestamp,actions[lastBuiltRevision[SHA1]]]" 2>/dev/null)
  exact=$(echo "$list" | jq -c --arg sha "$sha" --argjson min "$min" '[.builds[]? | select(.number > $min) | select(any(.actions[]?; .lastBuiltRevision.SHA1? == $sha))] | .[0] // null' 2>/dev/null)
  if [ -n "$exact" ] && [ "$exact" != null ]; then echo "$exact"; return; fi
  if [ -n "${ORIGIN_FOR_WAIT:-}" ]; then
    for row in $(echo "$list" | jq -r --argjson min "$min" '.builds[]? | select(.number > $min and .building == false) | "\(.number):\([.actions[]? | .lastBuiltRevision.SHA1? | select(. != null)][0] // "")"' 2>/dev/null); do
      n=${row%%:*}; s=${row#*:}
      if [ -n "$s" ] && git -C "$ORIGIN_FOR_WAIT" merge-base --is-ancestor "$sha" "$s" 2>/dev/null; then echo "$list" | jq -c --argjson n "$n" '[.builds[]? | select(.number == $n)][0]'; return; fi
    done
  fi
  echo null; }
branch_build_for() { curl -s -g -m 10 "$J/job/$1/job/$2/api/json?tree=builds[number,building,result,duration,timestamp,actions[lastBuiltRevision[SHA1]]]" 2>/dev/null | jq -c --arg sha "$3" --argjson min "${4:-0}" '[.builds[]? | select(.number > $min) | select(any(.actions[]?; .lastBuiltRevision.SHA1? == $sha))] | .[0] // null' 2>/dev/null; }
size_of() { (cd "$1" && git fetch -q origin main 2>/dev/null; git diff --numstat origin/main..."$2" | awk '{ if ($3 ~ /package-lock\.json$/) { la+=$1; ld+=$2 } else { a+=$1; d+=$2; f++ } } END { printf "{\"files\":%d,\"add\":%d,\"del\":%d,\"lock_add\":%d,\"lock_del\":%d}", f, a, d, la, ld }' | jq -c --argjson c "$(cd "$1" && git rev-list --count origin/main.."$2")" '. + {commits:$c}'); }
teammates() { jq -r --arg me "$ME" '.devs[] | select(. != $me)' $RUN/meta.json; }
WORK=$RUN/work/$ME
cmd=${1:-help}; shift || true
case $cmd in
  help) { cat <<'EOF'
st ticket [id]                     show the ticket (in backlog mode: st ticket <id>)
st board                           shared task board: every task, its owner, state and dependencies
st team                            who is on your team
st msg send <dev|all> "<text>"     message a teammate
st msg inbox                       read new messages
st msg wait [seconds]              block until a new message arrives (default 300)
st task claim <n> | start <n> | done <n>    update a task on the board
st next                            (backlog mode) take the next unclaimed ticket
st ticket done <id>                (backlog mode) mark a ticket finished and live
st repos                           list repositories
st clone <key>                     clone a repository into your work area
st pr open <key> <branch> "<title>"   push your branch and open a PR (starts CI)
st pr wait <n>                     wait for CI on the PR's latest push
st pr push <n>                     push new commits to the PR branch (re-runs CI)
st pr merge <n>                    merge a PR whose latest CI run is green (starts CD)
st pr list                         all PRs (yours and your teammates')
st deploy wait <n>                 wait for CI/CD on main after merging PR n
st done "<summary>"                you have finished everything you are responsible for
st blocked "<reason>"              give up
Branch names: lowercase letters, digits and hyphens only.
EOF
    if [ "$(jq -r '.handoff // false' $RUN/meta.json)" = true ]; then echo 'st handoff post <version> <class> "<what changed>" "<who must act>"   publish a handoff note when you release something others depend on'; echo 'st handoff show                    read the handoff notes'; fi
    } | { if [ "$(jq -r '.msg // false' $RUN/meta.json)" = true ]; then cat; else grep -v '^st msg'; fi; }
  ;;
  team) echo "you are $ME; teammates: $(teammates | tr '\n' ' ')";;
  ticket)
    if [ "${1:-}" = done ]; then id=${2:?id}; lock backlog; jq --arg id "$id" --arg me "$ME" 'map(if .id==$id and .owner==$me then .state="done" else . end)' $RUN/backlog.json > $RUN/b.$ME.tmp && mv $RUN/b.$ME.tmp $RUN/backlog.json; unlock backlog; ev ticket_done "{\"ticket\":\"$id\"}"; echo "ticket $id marked done"
    elif [ -n "${1:-}" ]; then cat $RUN/tickets/$1.md
    else cat $RUN/ticket.md; fi;;
  board) [ -f $RUN/tasks.json ] && jq -r '.[] | "\(.id)\t\(.key // .ticket)\t[\(.repo)]\towner=\(.owner // "-")\t\(.state)\tdepends=\((.depends // [])|map(tostring)|join(","))\t\(.title)"' $RUN/tasks.json | cut -c1-220 || echo "(no tasks)"; [ -f $RUN/backlog.json ] && jq -r '.[] | "\(.id)\towner=\(.owner // "-")\t\(.state)\t\(.title)"' $RUN/backlog.json;;
  task) sub=${1:?}; n=${2:?n}
    case $sub in claim) st=doing;; start) st=doing;; done) st=done;; *) exit 2;; esac
    lock tasks; jq --argjson n $n --arg s $st --arg me "$ME" 'map(if .id==$n then (.state=$s | .owner=(.owner // $me)) else . end)' $RUN/tasks.json > $RUN/t.$ME.tmp && mv $RUN/t.$ME.tmp $RUN/tasks.json; unlock tasks
    ev task_$sub "{\"task\":$n}"; echo "task $n -> $st";;
  next) lock backlog; id=$(jq -r '[.[]|select(.owner==null)][0].id // empty' $RUN/backlog.json)
    if [ -z "$id" ]; then unlock backlog; echo "no more tickets in the backlog"; exit 0; fi
    jq --arg id "$id" --arg me "$ME" 'map(if .id==$id then (.owner=$me | .state="doing") else . end)' $RUN/backlog.json > $RUN/b.$ME.tmp && mv $RUN/b.$ME.tmp $RUN/backlog.json; unlock backlog
    ev ticket_claimed "{\"ticket\":\"$id\"}"; echo "you now own $id:"; echo; cat $RUN/tickets/$id.md;;
  msg) [ "$(jq -r '.msg // false' $RUN/meta.json)" = true ] || { echo "unknown command: msg (try: st help)" >&2; exit 2; }
    sub=${1:?}; shift
    case $sub in
      send) to=${1:?}; text=${2:?}; id=$(ms); jq -cn --argjson id $id --arg f "$ME" --arg t "$to" --arg x "$text" '{id:$id,ts:$id,from:$f,to:$t,text:$x}' >> $RUN/msgs.jsonl; ev msg_sent "$(jq -cn --arg t "$to" --argjson n ${#text} '{to:$t,chars:$n}')"; echo "sent";;
      inbox|wait) t0=$(ms); lim=$(( ${1:-300} * 1000 )); cur=$RUN/cursor.$ME; [ -f $cur ] || echo 0 > $cur
        while :; do
          total=$([ -f $RUN/msgs.jsonl ] && wc -l < $RUN/msgs.jsonl | tr -d ' ' || echo 0); seen=$(cat $cur)
          new=$([ "$total" -gt "$seen" ] && tail -n +$((seen+1)) $RUN/msgs.jsonl | jq -c --arg me "$ME" 'select(.from != $me and (.to==$me or .to=="all"))' || true)
          if [ "$total" -gt "$seen" ]; then echo $total > $cur; fi
          if [ -n "$new" ]; then echo "$new" | jq -r '"[from \(.from)] \(.text)"'; echo "$new" | while read -r m; do ev msg_read "$(echo "$m" | jq -c --argjson now "$(ms)" '{from:.from,latency_ms:($now-.ts)}')"; done
            [ "$sub" = wait ] && ev msg_wait "{\"waited_ms\":$(( $(ms) - t0 ))}"; exit 0; fi
          [ "$sub" = inbox ] && { echo "(no new messages)"; exit 0; }
          [ $(( $(ms) - t0 )) -gt $lim ] && { ev msg_wait "{\"waited_ms\":$(( $(ms) - t0 )),\"timeout\":true}"; echo "(no message within the wait)"; exit 0; }
          sleep 2; done;;
    esac;;
  handoff) [ "$(jq -r '.handoff // false' $RUN/meta.json)" = true ] || { echo "unknown command: handoff (try: st help)" >&2; exit 2; }
    sub=${1:-show}; shift || true
    case $sub in
      post) ver=${1:?version}; cls=${2:?release class}; what=${3:?what changed}; who=${4:?who must act}; id=$(ms)
        jq -cn --argjson id $id --arg f "$ME" --arg v "$ver" --arg c "$cls" --arg w "$what" --arg a "$who" '{id:$id,ts:$id,from:$f,version:$v,class:$c,what:$w,who:$a}' >> $RUN/handoffs.jsonl
        ev handoff_posted "$(jq -cn --arg v "$ver" --arg c "$cls" '{version:$v,class:$c}')"; echo "handoff posted";;
      show) if [ -s $RUN/handoffs.jsonl ]; then jq -r '"[handoff from \(.from)] released: \(.version) (\(.class)); changed: \(.what); who must act: \(.who)"' $RUN/handoffs.jsonl; ev handoff_read '{}'; else echo "(no handoff notes yet)"; ev handoff_read '{"empty":true}'; fi;;
      *) echo "usage: st handoff post|show" >&2; exit 2;;
    esac;;
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
  clone) k=${1:?key}; need_key $k; d=$WORK/$k
    if [ -d $d ]; then echo "already cloned: $d"; exit 0; fi
    mkdir -p $WORK && git clone -q --no-hardlinks "$(origin_of $k)" $d && git -C $d config remote.origin.pushurl "disabled-use-st-pr-open" && git -C $d config user.name "$ME" && git -C $d config user.email "$ME@study.local"
    ev clone "{\"repo\":\"$k\"}"; echo "cloned $k -> $d";;
  pr)
    sub=${1:?}; shift; [ -f $RUN/prs.json ] || echo '[]' > $RUN/prs.json
    case $sub in
      open) k=${1:?key}; b=${2:?branch}; title=${3:?title}; need_key $k
        [[ $b =~ ^[a-z0-9][a-z0-9-]*$ ]] || { echo "bad branch name '$b'" >&2; exit 2; }
        w=$WORK/$k; [ -d $w ] || { echo "clone $k first" >&2; exit 2; }
        git -C $w rev-parse --verify -q "$b" >/dev/null || { echo "branch '$b' does not exist in $w" >&2; exit 2; }
        git -C $w push -q "$(origin_of $k)" "$b:refs/heads/$b" 2>&1 | tail -2
        head=$(git -C $w rev-parse "$b"); sz=$(size_of $w "$b")
        lock prs; id=$(jq 'length+1' $RUN/prs.json)
        jq --argjson id $id --arg k $k --arg b "$b" --arg t "$title" --arg h "$head" --arg a "$ME" --argjson sz "$sz" --argjson ts $(ms) '. + [{id:$id,author:$a,repo:$k,branch:$b,title:$t,head:$h,opened_ts:$ts,size:$sz,ci:null,merged_ts:null}]' $RUN/prs.json > $RUN/prs.$ME.tmp && mv $RUN/prs.$ME.tmp $RUN/prs.json; unlock prs
        jk_scan "$(ci_of $k)"; ev pr_opened "$(jq -cn --argjson id $id --arg k $k --arg b "$b" --argjson sz "$sz" '{pr:$id,repo:$k,branch:$b,size:$sz}')"
        echo "PR #$id opened on $k ($b): $(echo $sz | jq -r '"\(.files) files +\(.add)/-\(.del) lines (+\(.lock_add)/-\(.lock_del) lockfile), \(.commits) commit(s)"'); CI started";;
      push) n=${1:?}; k=$(pr_get $n repo); b=$(pr_get $n branch); w=$WORK/$k
        git -C $w push -q "$(origin_of $k)" "$b:refs/heads/$b" 2>&1 | tail -2; head=$(git -C $w rev-parse "$b"); sz=$(size_of $w "$b")
        pr_set $n head "\"$head\""; pr_set $n size "$sz"; pr_set $n ci null; jk_scan "$(ci_of $k)"
        ev pr_updated "$(jq -cn --argjson id $n --argjson sz "$sz" '{pr:$id,size:$sz}')"; echo "PR #$n updated; CI re-started";;
      wait) n=${1:?}; k=$(pr_get $n repo); b=$(pr_get $n branch); h=$(pr_get $n head); ci=$(ci_of $k); t0=$(ms); minnum=0; retries=0
        until [ $(( $(ms) - t0 )) -gt 600000 ]; do
          bb=$(branch_build_for $ci $b $h $minnum)
          if [ "$bb" != null ] && [ -n "$bb" ] && [ "$(echo "$bb" | jq -r .building)" = false ]; then
            res=$(echo "$bb" | jq -r .result); dur=$(echo "$bb" | jq -r .duration); num=$(echo "$bb" | jq -r .number)
            if [ "$res" != SUCCESS ] && [ $retries -lt 2 ] && infra_fail "$J/job/$ci/job/$b/$num/consoleText"; then retries=$((retries+1)); minnum=$num; ev infra_retry "{\"pr\":$n,\"kind\":\"ci\"}"; curl -s -o /dev/null -X POST "$J/job/$ci/job/$b/build?delay=0"; sleep 3; continue; fi
            pr_set $n ci "\"$res\""; ev ci_result "$(jq -cn --argjson pr $n --arg r $res --argjson d $dur --arg sha $h --argjson w $(( $(ms) - t0 )) '{pr:$pr,result:$r,build_ms:$d,waited_ms:$w,sha:$sha}')"
            echo "CI for PR #$n: $res (build ran ${dur} ms)"
            if [ "$res" != SUCCESS ]; then echo "--- console tail ---"; curl -s -m 10 "$J/job/$ci/job/$b/$num/consoleText" | grep -v '^\[Pipeline\]' | tail -40 | cut -c1-200; exit 1; fi
            exit 0; fi
          sleep 3; done
        echo "timed out waiting for CI" >&2; exit 3;;
      merge) n=${1:?}; k=$(pr_get $n repo); b=$(pr_get $n branch); title=$(pr_get $n title); o=$(origin_of $k)
        [ "$(pr_get $n ci)" = SUCCESS ] || { echo "CI is not green for the latest push of PR #$n (run: st pr wait $n)" >&2; exit 1; }
        ci=$(ci_of $k); cdj=$(cd_of $k)
        lock merge-$k
        ci_prev=$(jk_num $ci); cd_prev=$(jk_num $cdj)
        ( cd $o && git checkout -q main && GIT_AUTHOR_NAME=maintainer GIT_AUTHOR_EMAIL=m@study.local GIT_COMMITTER_NAME=maintainer GIT_COMMITTER_EMAIL=m@study.local git merge -q --no-ff -m "Merge PR #$n: $title" "refs/heads/$b" ) 2>&1 | tail -3
        rc=${PIPESTATUS[0]}
        if [ "$rc" != 0 ]; then ( cd $o && git merge --abort 2>/dev/null ); unlock merge-$k; ev merge_failed "{\"pr\":$n}"; echo "merge failed: conflicts with main. Rebase or merge origin/main into your branch, fix, then 'st pr push $n' and wait for CI again." >&2; exit 1; fi
        msha=$(git -C $o rev-parse main); unlock merge-$k
        pr_set $n merge_sha "\"$msha\""; pr_set $n merged_ts $(ms); pr_set $n ci_prev $ci_prev; pr_set $n cd_prev $cd_prev
        jk_scan $ci; jk_scan $cdj; ev pr_merged "$(jq -cn --argjson pr $n --arg sha $msha '{pr:$pr,merge_sha:$sha}')"; echo "PR #$n merged to main ($msha); CI/CD started";;
      list) jq -r '.[] | "#\(.id) \(.author) \(.repo) \(.branch) ci=\(.ci // "-") merged=\(if .merged_ts then "yes" else "no" end)  \(.title)"' $RUN/prs.json;;
    esac;;
  deploy)
    [ "${1:-}" = wait ] || exit 2; n=${2:?}; k=$(pr_get $n repo); sha=$(pr_get $n merge_sha); ci=$(ci_of $k); cdj=$(cd_of $k); t0=$(ms); cmin=0; imin=0; cret=0; iret=0
    [ -n "$sha" ] && [ "$sha" != null ] || { echo "PR #$n is not merged" >&2; exit 2; }
    ORIGIN_FOR_WAIT=$(origin_of $k)
    until [ $(( $(ms) - t0 )) -gt 600000 ]; do
      cb=$(main_build_for $cdj $sha $cmin); ib=$(main_build_for $ci $sha $imin)
      if [ "$cb" != null ] && [ -n "$cb" ] && [ "$ib" != null ] && [ -n "$ib" ] && [ "$(echo "$cb" | jq -r .building)" = false ] && [ "$(echo "$ib" | jq -r .building)" = false ]; then
        cr=$(echo "$cb" | jq -r .result); ir=$(echo "$ib" | jq -r .result); cn=$(echo "$cb" | jq -r .number); in_=$(echo "$ib" | jq -r .number)
        if [ "$cr" != SUCCESS ] && [ $cret -lt 2 ] && infra_fail "$J/job/$cdj/job/main/$cn/consoleText"; then cret=$((cret+1)); cmin=$cn; ev infra_retry "{\"kind\":\"cd\"}"; curl -s -o /dev/null -X POST "$J/job/$cdj/job/main/build?delay=0"; sleep 3; continue; fi
        if [ "$ir" != SUCCESS ] && [ $iret -lt 2 ] && infra_fail "$J/job/$ci/job/main/$in_/consoleText"; then iret=$((iret+1)); imin=$in_; ev infra_retry "{\"kind\":\"ci_main\"}"; curl -s -o /dev/null -X POST "$J/job/$ci/job/main/build?delay=0"; sleep 3; continue; fi
        ev deploy_result "$(jq -cn --argjson pr $n --arg cr $cr --arg ir $ir --argjson cd_ms "$(echo "$cb" | jq .duration)" --argjson ci_ms "$(echo "$ib" | jq .duration)" --argjson w $(( $(ms) - t0 )) '{pr:$pr,cd_result:$cr,ci_main_result:$ir,cd_ms:$cd_ms,ci_main_ms:$ci_ms,waited_ms:$w}')"
        echo "main after PR #$n: CI=$ir CD=$cr (CD ran $(echo "$cb" | jq -r .duration) ms)"
        case $k in contracts|platformkit) echo "registry now has: $(curl -s -m 5 http://127.0.0.1:4873/$( [ $k = contracts ] && echo @mfe%2fshared-contracts || echo @studio%2fplatform-kit) | jq -r '.versions|keys|join(", ")')";; esac
        if [ "$cr" != SUCCESS ] || [ "$ir" != SUCCESS ]; then echo "--- CD console tail ---"; curl -s -m 10 "$J/job/$cdj/job/main/$cn/consoleText" | grep -v '^\[Pipeline\]' | tail -40 | cut -c1-200; exit 1; fi
        exit 0; fi
      sleep 3; done
    echo "timed out waiting for main builds" >&2; exit 3;;
  done) ev done "$(jq -cn --arg s "${1:-}" '{summary:$s}')"; echo "marked done";;
  blocked) ev blocked "$(jq -cn --arg s "${1:-}" '{reason:$s}')"; echo "marked blocked";;
  *) echo "unknown command: $cmd (try: st help)" >&2; exit 2;;
esac
