#!/bin/bash
# Builds the whole study field from scratch: registry, Jenkins, 3 topology-neutral pieces:
#   external/libs-platform-kit        (own repo, CI+CD publish to the private registry; consumed by billing ONLY, in both worlds)
#   multi/{libs-shared-contracts,apps-core-shell,apps-sub-route-billing}   (every repo has CI+CD)
#   mono (clone of homelab-mfe-monorepo; contracts in-repo)                (root CI + CD)
# No remotes anywhere; nothing leaves this machine.
set -eu
export GIT_AUTHOR_NAME=study GIT_AUTHOR_EMAIL=study@localhost GIT_COMMITTER_NAME=study GIT_COMMITTER_EMAIL=study@localhost
H=$HOME/study-mfe/s2/helpers; SRC=$HOME/src/github.com/dlockamy/homelab-mfe-monorepo; STUDY=$HOME/study-mfe
export MFE_REGISTRY=http://127.0.0.1:4873/        # host-side; build containers get host.docker.internal from Jenkins
say() { echo; echo "### $*"; }

say "teardown"
docker rm -f study-jenkins study-registry >/dev/null 2>&1 || true
docker volume rm study-jenkins-home >/dev/null 2>&1 || true
rm -rf /tmp/study && mkdir -p /tmp/study/multi /tmp/study/external

say "private registry"
docker run -d --name study-registry -p 127.0.0.1:4873:4873 -v $STUDY/registry/config.yaml:/verdaccio/conf/config.yaml:ro verdaccio/verdaccio:5 >/dev/null
until curl -s -m 3 http://127.0.0.1:4873/-/ping >/dev/null; do sleep 1; done
TOKEN=$(curl -s -X PUT -H 'content-type: application/json' -d '{"name":"ci","password":"study-ci-pass-1","email":"ci@study.local"}' http://127.0.0.1:4873/-/user/org.couchdb.user:ci | jq -r .token)
echo "$TOKEN" > $STUDY/registry/ci-token; chmod 600 $STUDY/registry/ci-token

say "jenkins"
docker run -d --name study-jenkins --user root -p 127.0.0.1:18080:8080 -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp/study:/tmp/study -v $STUDY/registry/ci-token:/run/study/registry-token:ro -v study-jenkins-home:/var/jenkins_home study-jenkins:local >/dev/null
until docker logs study-jenkins 2>&1 | grep -q "fully up and running"; do sleep 2; done
source $STUDY/bin/jk.sh

mklib() { # dir name version indexfile
  mkdir -p "$1" && cd "$1" && git init -q -b main
  cp "$H/$4" index.js; cp "$H/lib-Jenkinsfile" Jenkinsfile; cp "$H/lib-Jenkinsfile.cd" Jenkinsfile.cd; cp "$H/npmrc" .npmrc; cp "$H/contributing-multi.md" CONTRIBUTING.md
  printf '{"name": "%s", "version": "%s", "type": "module", "main": "index.js"}\n' "$2" "$3" > package.json
  printf 'node_modules\n*.tgz\n' > .gitignore
  git add -A && git commit -qm "$2 v$3" && cd - >/dev/null
}
say "libs (own repos): platform-kit [external], shared-contracts [multi]"
mklib /tmp/study/external/libs-platform-kit @studio/platform-kit 1.0.0 platformkit-index.js
mklib /tmp/study/multi/libs-shared-contracts @mfe/shared-contracts 1.0.0 contracts-index.js
jk_create ext-platformkit-ci /tmp/study/external/libs-platform-kit Jenkinsfile
jk_create ext-platformkit-cd /tmp/study/external/libs-platform-kit Jenkinsfile.cd
jk_create multi-contracts-ci /tmp/study/multi/libs-shared-contracts Jenkinsfile
jk_create multi-contracts-cd /tmp/study/multi/libs-shared-contracts Jenkinsfile.cd
echo "waiting for the libs' CD to publish v1.0.0 ..."
for i in $(seq 1 90); do jk_reg_has @studio/platform-kit 1.0.0 && jk_reg_has @mfe/shared-contracts 1.0.0 && break; sleep 2; done
jk_reg_has @studio/platform-kit 1.0.0 && jk_reg_has @mfe/shared-contracts 1.0.0 && echo "registry has both libs @1.0.0" || { echo "LIB PUBLISH FAILED"; exit 1; }

say "multi-repo apps"
cd /tmp/study/multi
mkdir apps-core-shell && ( cd apps-core-shell && git init -q -b main && mkdir src scripts
  cp "$SRC/apps/core-shell/src/index.html" src/; cp "$H/shell-build.js" build.js; cp "$H/shell-config.js" src/config.js
  cp "$H/mfe-resolve.cjs" "$H/check-contract.cjs" scripts/; cp "$H/npmrc" .npmrc
  cat > package.json <<'PKG'
{
  "name": "@mfe/core-shell",
  "version": "1.0.0",
  "team": "platform",
  "scripts": {"prebuild": "npm install --no-audit --no-fund", "build": "node build.js"},
  "dependencies": {"@mfe/shared-contracts": "^1.0.0"}
}
PKG
  npm install --no-audit --no-fund 2>&1 | tail -2
  cp "$H/shell-Jenkinsfile" Jenkinsfile; cp "$H/contributing-multi.md" CONTRIBUTING.md; cp "$H/shell-publish.sh" scripts/publish.sh; chmod +x scripts/publish.sh
  sed -e 's#__APP__#core-shell#; s#__PUBLISH__#scripts/publish.sh#; s#__TAG__#apps-core-shell#g' "$H/app-Jenkinsfile.cd" > Jenkinsfile.cd
  printf 'node_modules\ndist\n' > .gitignore )
mkdir apps-sub-route-billing && ( cd apps-sub-route-billing && git init -q -b main && mkdir src scripts
  cp "$H/billing-main.js" src/main.js; cp "$H/billing-build.js" build.js
  cp "$H/mfe-resolve.cjs" "$H/check-contract.cjs" scripts/; cp "$SRC/scripts/update-importmap.js" scripts/
  perl -0pe 's#\$ROOT/apps/sub-route-billing/dist#\$ROOT/dist#g; s#  shell\)\n.*?    ;;\n\n##s; s#shell \| billing#billing#' "$SRC/scripts/publish.sh" > scripts/publish.sh; chmod +x scripts/publish.sh
  python3 - <<'PY'
# s2 deviation: the shipped flip_manifest is a read-modify-write on one shared importmap.json; two apps deploying at the same
# moment (multi-repo CD runs in parallel) overwrite each other (seen at baseline). Verify-and-retry in the multi-repo copy only.
p='scripts/publish.sh'; s=open(p).read()
s=s.replace("flip_manifest() {","flip_once() {",1)
s=s.replace("# Point '@mfe/sub-route-billing' at","""flip_manifest() {
  for i in 1 2 3 4 5 6; do
    flip_once "$1"
    sleep 2
    if aws s3api get-object --bucket "$S3_BUCKET" --key importmap.json "$TMP/verify.json" >/dev/null 2>&1 && grep -q "\\"/$1\\"" "$TMP/verify.json"; then return 0; fi
    echo "importmap update was overwritten by a concurrent publish; retrying ($i)" >&2
  done
  echo "importmap update kept being overwritten" >&2; return 1
}

# Point '@mfe/sub-route-billing' at""",1)
open(p,'w').write(s)
PY
  cat > package.json <<'EOF'
{
  "name": "@mfe/sub-route-billing",
  "version": "1.0.0",
  "team": "payments",
  "scripts": {"prebuild": "npm install --no-audit --no-fund", "build": "node build.js"},
  "dependencies": {"@mfe/shared-contracts": "^1.0.0", "@studio/platform-kit": "^1.0.0"}
}
EOF
  cp "$H/npmrc" .npmrc; cp "$H/contributing-multi.md" CONTRIBUTING.md; cp "$H/billing-Jenkinsfile" Jenkinsfile
  sed -e 's#__APP__#sub-route-billing#; s#__PUBLISH__#scripts/publish.sh billing "$BILLING_VERSION"#; s#__TAG__#apps-sub-route-billing#g' "$H/app-Jenkinsfile.cd" > Jenkinsfile.cd
  printf 'node_modules\ndist\n' > .gitignore
  npm install --no-audit --no-fund 2>&1 | tail -2 )


mkdir apps-sub-route-reports && ( cd apps-sub-route-reports && git init -q -b main && mkdir src scripts
  cp "$H/reports-main.js" src/main.js; cp "$H/reports-build.js" build.js
  cp "$H/mfe-resolve.cjs" "$H/check-contract.cjs" scripts/; cp "$SRC/scripts/update-importmap.js" scripts/
  sed -e 's/sub-route-billing/sub-route-reports/g; s/billing/reports/g' ../apps-sub-route-billing/scripts/publish.sh > scripts/publish.sh; chmod +x scripts/publish.sh
  cat > package.json <<'EOF'
{
  "name": "@mfe/sub-route-reports",
  "version": "1.0.0",
  "team": "insights",
  "scripts": {"prebuild": "npm install --no-audit --no-fund", "build": "node build.js"},
  "dependencies": {"@mfe/shared-contracts": "^1.0.0"}
}
EOF
  cp "$H/npmrc" .npmrc; cp "$H/contributing-multi.md" CONTRIBUTING.md; cp "$H/reports-Jenkinsfile" Jenkinsfile
  sed -e 's#__APP__#sub-route-reports#; s#__PUBLISH__#scripts/publish.sh reports "$BILLING_VERSION"#; s#__TAG__#apps-sub-route-reports#g' "$H/app-Jenkinsfile.cd" > Jenkinsfile.cd
  printf 'node_modules\ndist\n' > .gitignore
  npm install --no-audit --no-fund 2>&1 | tail -2
  git add -A; git commit -qm "reports baseline: CI, CD, publish script; deps contracts@^1" )

# Makefiles (ensure/stop-localstack copied verbatim from the monorepo's Makefile)
MK_HEAD='# Local development against LocalStack (a fake AWS). Nothing here touches real AWS.
export MFE_REGISTRY ?= http://127.0.0.1:4873/
LOCALSTACK_URL=http://localhost:4566
S3_BUCKET=homelab-mfe-delivery-bucket-multi
AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION
unexport AWS_PROFILE AWS_SESSION_TOKEN
AWS_LOCAL=aws --endpoint-url=$(LOCALSTACK_URL)
.PHONY: ensure-localstack stop-localstack init clean'
ENSURE=$(sed -n '/^ensure-localstack:/,/^start-localstack:/p' "$SRC/Makefile" | sed '$d'); STOP=$(sed -n '/^stop-localstack:/,/^build-shell:/p' "$SRC/Makefile" | sed '$d')
( cd apps-sub-route-billing; { printf '%s\n\n%s\n%s\n' "$MK_HEAD" "$ENSURE" "$STOP"; cat <<'EOF'
build-billing: ensure-localstack ## Compile Billing and release it as v<timestamp> (immutable artifact + manifest flip)
	@echo "Compiling Billing Sub-route..."
	@npm run build
	@VERSION=v$$(date +%s); \
	S3_BUCKET=$(S3_BUCKET) AWS_ENDPOINT_URL=$(LOCALSTACK_URL) scripts/publish.sh billing $$VERSION && \
	echo "Release live on mock CDN. Active bundle: /artifacts/billing/$$VERSION/main.js"

clean:
	rm -rf node_modules dist
EOF
  } > Makefile; git add -A; git commit -qm "billing baseline: CI, CD, Makefile, publish scripts; deps contracts@^1 + platform-kit@^1" )
( cd apps-core-shell; { printf '%s\n\n%s\n%s\n' "$MK_HEAD" "$ENSURE" "$STOP"; cat <<'EOF'
build-shell: ensure-localstack ## Compile the Core Shell and publish it to mock S3
	@echo "Compiling Core Shell application..."
	@npm run build
	@S3_BUCKET=$(S3_BUCKET) AWS_ENDPOINT_URL=$(LOCALSTACK_URL) scripts/publish.sh

clean:
	rm -rf dist
EOF
  } > Makefile; git add -A; git commit -qm "core-shell baseline: CI, CD, Makefile, publish script" )

say "monorepo"
git clone -q "$SRC" /tmp/study/mono && cd /tmp/study/mono && git remote remove origin && { git checkout -q main 2>/dev/null || git checkout -q -b main; }
cp "$H/mfe-resolve.cjs" "$H/check-contract.cjs" scripts/
cp "$H/contracts-index.js" libs/shared-contracts/index.js
echo '{"name": "@mfe/shared-contracts", "version": "1.0.0", "type": "module", "main": "index.js"}' > libs/shared-contracts/package.json
cp "$H/shell-build.js" apps/core-shell/build.js; cp "$H/shell-config.js" apps/core-shell/src/config.js
cd apps/sub-route-billing
cp "$H/billing-main.js" src/main.js; cp "$H/billing-build.js" build.js; cp "$H/npmrc" .npmrc
cat > package.json <<'EOF'
{
  "name": "@mfe/sub-route-billing",
  "version": "1.0.0",
  "team": "payments",
  "scripts": {"prebuild": "npm install --no-audit --no-fund", "build": "node build.js"},
  "dependencies": {"@studio/platform-kit": "^1.0.0"}
}
EOF
npm install --no-audit --no-fund 2>&1 | tail -2; 
# --- s2: third consumer in the monorepo ---
mkdir -p /tmp/study/mono/apps/sub-route-reports/src && cd /tmp/study/mono/apps/sub-route-reports
cp "$H/reports-main.js" src/main.js; cp "$H/reports-build.js" build.js; cp "$H/npmrc" .npmrc
cat > package.json <<'EOF'
{
  "name": "@mfe/sub-route-reports",
  "version": "1.0.0",
  "team": "insights",
  "scripts": {"build": "node build.js"}
}
EOF
cd /tmp/study/mono
python3 - <<'PY'
import re
p='scripts/publish.sh'; s=open(p).read()
# flip_manifest takes an optional specifier
s=s.replace("flip_manifest() {\n  KEY=$1\n","flip_manifest() {\n  KEY=$1\n  SPEC=${2:-@mfe/sub-route-billing}\n")
s=s.replace("""node "$HERE/update-importmap.js" "$TMP/importmap.json" '@mfe/sub-route-billing' "/$KEY\"""","""node "$HERE/update-importmap.js" "$TMP/importmap.json" "$SPEC" "/$KEY\"""")
case=re.search(r"  billing\)\n.*?    flip_manifest \"\$KEY\"\n    ;;\n", s, re.S).group(0)
rep=case.replace("billing)","reports)").replace("sub-route-billing","sub-route-reports").replace("artifacts/billing","artifacts/reports").replace("publish.sh billing","publish.sh reports").replace('flip_manifest "$KEY"','flip_manifest "$KEY" @mfe/sub-route-reports')
s=s.replace(case, case+"\n"+rep,1)
s=s.replace("usage: publish.sh shell | billing <version> | rollback <version>","usage: publish.sh shell | billing <version> | reports <version> | rollback <version>")
open(p,'w').write(s)
p='Jenkinsfile'; s=open(p).read()
s=s.replace("def apps = ['core-shell', 'sub-route-billing']","def apps = ['core-shell', 'sub-route-billing', 'sub-route-reports']")
s=s.replace("                    test -s apps/sub-route-billing/dist/main.js\n","                    test -s apps/sub-route-billing/dist/main.js\n                    test -s apps/sub-route-reports/dist/main.js\n")
open(p,'w').write(s)
p='Jenkinsfile.cd'; s=open(p).read()
s=s.replace("""                    env.BILLING_CHANGED    = (files == null || files.any { it.startsWith('apps/sub-route-billing/') }) ? 'true' : 'false'\n""","""                    env.BILLING_CHANGED    = (files == null || files.any { it.startsWith('apps/sub-route-billing/') }) ? 'true' : 'false'\n                    env.REPORTS_CHANGED    = (files == null || files.any { it.startsWith('apps/sub-route-reports/') }) ? 'true' : 'false'\n""")
s=re.sub(r"^(\s*)environment name: 'BILLING_CHANGED',\s+value: 'true'\n", lambda m: m.group(0)+m.group(1)+"environment name: 'REPORTS_CHANGED',    value: 'true'\n", s, flags=re.M)
s=s.replace("""                    if (env.BILLING_CHANGED    == 'true') { dir('apps/sub-route-billing') { sh 'npm run build' } }\n""","""                    if (env.BILLING_CHANGED    == 'true') { dir('apps/sub-route-billing') { sh 'npm run build' } }\n                    if (env.REPORTS_CHANGED    == 'true') { dir('apps/sub-route-reports') { sh 'npm run build' } }\n""")
s=s.replace("""                        BILLING_VERSION = "v${env.BUILD_NUMBER}\"""","""                        BILLING_VERSION = "v${env.BUILD_NUMBER}"\n                        REPORTS_VERSION = "v${env.BUILD_NUMBER}\"""")
s=s.replace("""                                if [ "$BILLING_CHANGED"    = true ]; then scripts/publish.sh billing "$BILLING_VERSION"; fi\n""","""                                if [ "$BILLING_CHANGED"    = true ]; then scripts/publish.sh billing "$BILLING_VERSION"; fi\n                                if [ "$REPORTS_CHANGED"    = true ]; then scripts/publish.sh reports "$REPORTS_VERSION"; fi\n""")
s=s.replace("""                                if [ "$BILLING_CHANGED"    = true ]; then push_tag "apps-sub-route-billing-v${BUILD_NUMBER}"; fi\n""","""                                if [ "$BILLING_CHANGED"    = true ]; then push_tag "apps-sub-route-billing-v${BUILD_NUMBER}"; fi\n                                if [ "$REPORTS_CHANGED"    = true ]; then push_tag "apps-sub-route-reports-v${BUILD_NUMBER}"; fi\n""")
s=s.replace('core-shell=${env.CORE_SHELL_CHANGED} billing=${env.BILLING_CHANGED}','core-shell=${env.CORE_SHELL_CHANGED} billing=${env.BILLING_CHANGED} reports=${env.REPORTS_CHANGED}')
open(p,'w').write(s)
PY
grep -c REPORTS Jenkinsfile.cd; grep -c reports Jenkinsfile scripts/publish.sh

cd /tmp/study/mono; cp "$H/contributing-mono.md" CONTRIBUTING.md
jq '. + {team:"platform"}' apps/core-shell/package.json > /tmp/p.json && mv /tmp/p.json apps/core-shell/package.json
jq '. + {team:"payments"}' apps/sub-route-billing/package.json > /tmp/p.json && mv /tmp/p.json apps/sub-route-billing/package.json
perl -pi -e "s/DEPLOY_ENABLED     = 'false'/DEPLOY_ENABLED     = 'true'/" Jenkinsfile.cd   # the switch Jenkinsfile.cd's own header documents
git diff --stat | tail -1
git add -A && git commit -qm "study baseline: billingUrl, platform-kit dependency (registry), inlining build, contract check, DEPLOY_ENABLED=true"

say "localstack + bucket"
docker rm -f localstack-mfe >/dev/null 2>&1 || true
( cd /tmp/study/mono && make ensure-localstack 2>&1 | tail -1 )
( cd /tmp/study/multi/apps-sub-route-billing && make ensure-localstack 2>&1 | tail -1 )

say "remaining jobs"
jk_create mono-ci /tmp/study/mono Jenkinsfile
jk_create mono-cd /tmp/study/mono Jenkinsfile.cd
jk_create multi-shell-ci /tmp/study/multi/apps-core-shell Jenkinsfile
jk_create multi-shell-cd /tmp/study/multi/apps-core-shell Jenkinsfile.cd
jk_create multi-billing-ci /tmp/study/multi/apps-sub-route-billing Jenkinsfile
jk_create multi-billing-cd /tmp/study/multi/apps-sub-route-billing Jenkinsfile.cd
jk_create multi-reports-ci /tmp/study/multi/apps-sub-route-reports Jenkinsfile
jk_create multi-reports-cd /tmp/study/multi/apps-sub-route-reports Jenkinsfile.cd
sleep 15; jk_settle 300
say "baseline"
for j in ext-platformkit-ci ext-platformkit-cd multi-contracts-ci multi-contracts-cd multi-shell-ci multi-shell-cd multi-billing-ci multi-billing-cd multi-reports-ci multi-reports-cd mono-ci mono-cd; do printf "%-20s " $j; jk_last $j | tr '\t' ' '; done
