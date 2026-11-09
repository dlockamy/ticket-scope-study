#!/bin/bash
# Restart the study services in dependency order and wait until Jenkins answers.
docker start localstack-mfe study-registry study-jenkins >/dev/null
until curl -s -m 3 http://127.0.0.1:4873/-/ping >/dev/null; do sleep 1; done
until curl -s -m 3 -o /dev/null -w '%{http_code}' http://127.0.0.1:18080/login | grep -q 200; do sleep 2; done
echo "field up: Jenkins http://127.0.0.1:18080  registry http://127.0.0.1:4873  localstack :4566"
