#!/bin/bash
# Snapshot the baseline (field must be UP and idle): repos, Jenkins home, registry storage, S3 buckets.
set -eu
S=$HOME/study-mfe/s2/snap; rm -rf $S; mkdir -p $S/s3-mono $S/s3-multi
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1
EP=http://localhost:4566
aws --endpoint-url=$EP s3 sync s3://homelab-mfe-delivery-bucket $S/s3-mono --only-show-errors
aws --endpoint-url=$EP s3 sync s3://homelab-mfe-delivery-bucket-multi $S/s3-multi --only-show-errors
bash $HOME/study-mfe/s2/bin/field-down.sh >/dev/null
rsync -a --delete /tmp/study/ $S/study/
docker run --rm -v study-jenkins-home:/v -v $S:/s alpine tar czf /s/jenkins.tgz -C /v .
docker run --rm --volumes-from study-registry -v $S:/s alpine tar czf /s/registry.tgz -C /verdaccio/storage .
du -sh $S/* | sed "s#$S/##"
