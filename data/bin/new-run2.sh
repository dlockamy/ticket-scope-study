#!/bin/bash
# usage: new-run2.sh <mono|multi> <C1|C2|C3> <A1..A7> <rep> <model> <tag> [clarify]   -> creates the run dir, prints its path
set -eu
TOPO=$1; CH=$2; ARM=$3; REP=$4; MODEL=$5; TAG=$6; CLAR=${7:-}
ID=$TAG-$CH-$ARM-$TOPO-r$REP; R=$HOME/study-mfe/s2/runs/$ID
rm -rf $R; mkdir -p $R/work
FIELDS=$(python3 $HOME/study-mfe/s2/bin/gen.py $TOPO $CH $ARM $R $CLAR)
CLAR=$(jq -r 'if .clarify then "clarify" else "" end' <<<"$FIELDS")
perl -MTime::HiRes=time -e 'printf "%d\n", time*1000' > $R/start_ms
jq -n --arg r $ID --arg t $TOPO --arg c $CH --arg a $ARM --argjson rep $REP --arg m $MODEL --arg tag $TAG --argjson ms $(cat $R/start_ms) --argjson f "$FIELDS" \
  '{run:$r,topology:$t,change:$c,arm:$a,rep:$rep,model:$m,tag:$tag,start_ms:$ms} + $f' > $R/meta.json
printf '#!/bin/bash\nexport ST_RUN=%s\nexec bash %s/study-mfe/s2/bin/st2.sh "$@"\n' "$R" "$HOME" > $R/st; chmod +x $R/st
if [ "$CLAR" = clarify ]; then WHO="If something is unclear you may ask the person who wrote the ticket with \`st ask\`, but they are busy: make reasonable decisions, note your assumptions, and finish the job."; else WHO="Nobody is available to answer questions: make reasonable decisions, note your assumptions, and finish the job."; fi
cat > $R/brief.md <<BRIEF
You are a software developer on the platform team at a small company. A ticket has been assigned to you. $WHO

Your tools
- Everything about the ticket, PRs, CI and CD goes through one command: \`$R/st\` (run \`$R/st help\`). It stands in for our GitHub and Jira. Start with \`$R/st ticket\`.
- Source lives in git repositories. \`$R/st repos\` lists them and \`$R/st clone <key>\` gives you a working copy under $R/work/. Work only inside those clones.
- Standard tools are available: git, node/npm, a shell. To build locally: \`export MFE_REGISTRY=http://127.0.0.1:4873/\` (our private npm registry), then \`npm run build\` in the app directory.
$(cat $R/extra.txt)

Rules
- Do not touch anything outside your clones and \`st\`: no Docker, no Jenkins, no S3/AWS, no direct registry writes, no editing the origin repositories, no \`make build-*\` targets (they publish to the shared environment), and do not browse other directories under /tmp/study or ~/study-mfe.
- Read each repository's CONTRIBUTING.md before changing it, and follow the team's rules.
- Branch names must be lowercase letters, digits and hyphens. Push only through \`st pr open\` and \`st pr push\`.
- Open PRs with \`st pr open\`, wait for CI with \`st pr wait\`, merge with \`st pr merge\` only when CI is green, and confirm CD with \`st deploy wait\`. If CI or CD fails, fix it and carry on. The ticket is only done when the change is live.
- When finished, run \`st done "<summary>"\` (include your assumptions). If you truly cannot proceed, run \`st blocked "<reason>"\`.
- Be efficient. Keep changes minimal and focused on the ticket.

When you finish, reply with a short report: what shipped, the PRs you opened, and anything that surprised you or slowed you down.
BRIEF
echo $R
