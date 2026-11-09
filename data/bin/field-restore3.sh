#!/bin/bash
# Restore the snapshot and bring the field up. ~1-2 min.
set -eu
S=$HOME/study-mfe/s2/snap3
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1
EP=http://localhost:4566
bash $HOME/study-mfe/s2/bin/field-down.sh >/dev/null 2>&1 || true
rsync -a --delete $S/study/ /tmp/study/
docker run --rm -v study-jenkins-home:/v -v $S:/s alpine sh -c 'find /v -mindepth 1 -delete && tar xzf /s/jenkins.tgz -C /v'
docker run --rm --volumes-from study-registry -v $S:/s alpine sh -c 'find /verdaccio/storage -mindepth 1 -delete && tar xzf /s/registry.tgz -C /verdaccio/storage'
docker start localstack-mfe >/dev/null
until curl -s -m 3 $EP/_localstack/health | grep -q '"s3": "\(running\|available\)"'; do sleep 2; done
for pair in "homelab-mfe-delivery-bucket:s3-mono" "homelab-mfe-delivery-bucket-multi:s3-multi"; do
  b=${pair%%:*}; d=${pair##*:}
  aws --endpoint-url=$EP s3 mb s3://$b >/dev/null 2>&1 || true
  aws --endpoint-url=$EP s3 rm s3://$b --recursive --only-show-errors
  aws --endpoint-url=$EP s3 sync $S/$d s3://$b --only-show-errors
done
bash $HOME/study-mfe/s2/bin/field-up.sh
