#!/bin/bash
# usage: review-job.sh <case> <arm V0..V4>   -> /tmp/s2-review/out/<case>-<arm>.json (agent JSON); idempotent
C=$1; A=$2; B=/tmp/s2-review; O=$B/out/$C-$A.json
if [ -s $O ] && jq -e '.terminal_reason=="completed"' $O >/dev/null 2>&1; then exit 0; fi
case $A in
  V1|V2) CWD=$B/base; TOOLS=(--tools Read Glob Grep --allowedTools Read Glob Grep); ACCESS="You may look at the repositories as they were before this change: they are in the current directory (one folder per repository, read-only). Use Read, Glob and Grep." ;;
  *)     CWD=$B/empty; TOOLS=(--tools ""); ACCESS="You have only what is written below; you cannot look at any repository." ;;
esac
EXTRA=""
case $A in
  V2) EXTRA="Reviewer checklist: if the change alters something shared (a function, a contract, a configuration), check that every app which uses it was updated." ;;
  V3) EXTRA="For reference, the apps in this organization that use the shared contract (\`@mfe/shared-contracts\`) are: core-shell, sub-route-billing, sub-route-reports." ;;
  V4) EXTRA="Developer's description of the change (as it would appear in the PR description):
$(cat $B/cases/$C/summary.txt)" ;;
esac
PROMPT="You are a code reviewer on the platform team of a small company. A developer has finished a ticket and merged the changes below, across one or more repositories. Review whether the change correctly and completely does what the ticket asks. $ACCESS

$EXTRA

=== TICKET ===
$(cat $B/cases/$C/ticket.md)

=== CHANGES MERGED FOR THIS TICKET (all repositories, lockfiles omitted) ===
$(cat $B/cases/$C/change.diff)

=== END ===
Decide whether to approve the change or request changes. Reply with ONLY a JSON object, no other text, in exactly this form:
{\"verdict\": \"approve\" or \"request_changes\", \"issues\": [{\"where\": \"<repository or app>\", \"problem\": \"<one or two sentences>\"}], \"confidence\": <number 0 to 1>}
Use an empty issues list if you approve."
cd $CWD && perl -e 'alarm shift; exec @ARGV' 600 claude -p --model claude-sonnet-5-5 --output-format json --setting-sources project --strict-mcp-config "${TOOLS[@]}" --max-turns 40 "$PROMPT" > $O.tmp 2>/dev/null
mv $O.tmp $O
