#!/bin/bash
# Adds an "estate" of 12 unrelated repositories (multi-repo) / packages (monorepo) that do not use the shared contract.
# Run on a RESTORED baseline field (/tmp/study from snap), then re-baseline Jenkins and snapshot to snap3.
set -eu
export GIT_AUTHOR_NAME=study GIT_AUTHOR_EMAIL=study@localhost GIT_COMMITTER_NAME=study GIT_COMMITTER_EMAIL=study@localhost
declare -a SPEC=(
 "apps-analytics-dashboard|analytics|Internal analytics dashboard|data|renders usage charts from the warehouse export"
 "apps-admin-console|admin|Back-office admin console|ops|lists accounts and feature flags"
 "apps-help-center|help|Customer help center|support|serves articles from markdown"
 "apps-marketing-site|marketing|Public marketing site|growth|static landing pages"
 "libs-ui-kit|uikit|Shared UI components|design|buttons, inputs and layout helpers"
 "libs-logger|logger|Structured logging helper|platform|JSON logger with levels"
 "libs-i18n|i18n|Translation helpers|localization|loads message catalogs"
 "svc-notifications|notify|Notification service|messaging|queues email and push messages"
 "svc-auth-proxy|authproxy|Auth proxy|security|validates session cookies"
 "svc-search|search|Search service|discovery|indexes documents"
 "svc-export|export|CSV export service|data|builds CSV exports"
 "tools-release-notes|relnotes|Release notes generator|platform|collects merged PR titles"
)
mk() { # dir name desc team blurb
  mkdir -p "$1/src"; cd "$1"
  printf '{\n  "name": "@acme/%s",\n  "version": "1.0.0",\n  "team": "%s",\n  "description": "%s"\n}\n' "$2" "$4" "$3" > package.json
  printf '# %s\n\n%s. Owned by team %s; it %s.\n' "$2" "$3" "$4" "$5" > README.md
  printf '// %s\nexport function describe() { return "%s"; }\n' "$2" "$3" > src/index.js
  cd - >/dev/null
}
for row in "${SPEC[@]}"; do
  IFS='|' read -r repo key desc team blurb <<<"$row"
  d=/tmp/study/multi/$repo; rm -rf $d; mkdir -p $d; ( mk $d $repo "$desc" "$team" "$blurb"; cd $d; git init -q -b main; git add -A; git commit -qm "initial import" )
  # monorepo: same package under packages/
  mkdir -p /tmp/study/mono/packages; ( mk /tmp/study/mono/packages/$repo $repo "$desc" "$team" "$blurb" )
done
( cd /tmp/study/mono; git add -A; git commit -qm "add unrelated packages under packages/ (not part of the MFE pipelines)" )
echo "noise added: $(ls /tmp/study/multi | wc -l) multi dirs; mono packages: $(ls /tmp/study/mono/packages | wc -l)"
