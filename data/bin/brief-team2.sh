#!/bin/bash
# usage: brief-team2.sh <run-id> <dev>
ID=$1; D=$2; R=$HOME/study-mfe/s2/runs/$ID; ST=$R/st-$D
OTHER=$(jq -r --arg d $D '.devs[]|select(.!=$d)' $R/meta.json)
MSG=$(jq -r .msg $R/meta.json); HO=$(jq -r .handoff $R/meta.json)
if [ $D = dev-a ]; then MINE="sub-tasks 1 and 2 (tasks 1 and 2 on the board)"; else MINE="sub-tasks 3 and 4 (tasks 3 and 4 on the board)"; fi
if [ "$MSG" = true ]; then COMM="You can message your teammate with \`$ST msg send $OTHER \"...\"\` and read messages with \`$ST msg inbox\` or \`$ST msg wait\`."
elif [ "$HO" = true ]; then COMM="You cannot send free messages. Instead, when you release something your teammate depends on, you must publish a handoff note with \`$ST handoff post <version> <release class> \"<what changed>\" \"<who must act>\"\`, and you read your teammate's notes with \`$ST handoff show\`. Make the note complete: the exact released version, whether the release is major, minor or patch, what changed, and what the other developer must do."
else COMM="There is no message channel. You and your teammate share only the board (\`$ST board\`), the PR list (\`$ST pr list\`) and the CI and CD results."; fi
cat <<BRIEF
You are $D, a software developer on the platform team at a small company. Your team of two has been assigned one ticket, split into four sub-tasks. You own $MINE; your teammate ($OTHER) owns the rest and is working at the same time. Nobody else is available to answer questions. Do your own sub-tasks only; do not do your teammate's. Make reasonable decisions and note assumptions.

$COMM

Your tools
- Everything about tickets, PRs, CI, CD and the board goes through one command: \`$ST\` (run \`$ST help\`). It stands in for our GitHub and Jira. Start with \`$ST ticket\` and \`$ST board\`.
- Source lives in git repositories. \`$ST repos\` lists them and \`$ST clone <key>\` gives you a working copy under $R/work/$D/. Work only inside those clones.
- Standard tools are available: git, node/npm, a shell. To build locally: \`export MFE_REGISTRY=http://127.0.0.1:4873/\` (our private npm registry), then \`npm run build\` in the app directory.

Rules
- Do not touch anything outside your clones and \`st\`: no Docker, no Jenkins, no S3/AWS, no direct registry writes, no editing the origin repositories, no \`make build-*\` targets (they publish to the shared environment), and do not browse other directories under /tmp/study or ~/study-mfe.
- Read each repository's CONTRIBUTING.md before changing it, and follow the team's rules.
- Branch names must be lowercase letters, digits and hyphens. Push only through \`$ST pr open\` and \`$ST pr push\`.
- Open PRs with \`$ST pr open\`, wait for CI with \`$ST pr wait\`, merge with \`$ST pr merge\` only when CI is green, and confirm CD with \`$ST deploy wait\`. If CI or CD fails, fix it and carry on. A change is only done when it is live.
- When you have finished everything you are responsible for, run \`$ST done "<summary>"\` (include your assumptions). If you truly cannot proceed, run \`$ST blocked "<reason>"\`.
- Be efficient. Keep changes minimal and focused on the ticket.

When you finish, reply with a short report: what you shipped, the PRs you opened, how you coordinated, and anything that surprised you or slowed you down.
BRIEF
