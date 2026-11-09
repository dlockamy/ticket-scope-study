#!/bin/sh
# Publish the built core shell. (Multi-repo copy of the shell case of the monorepo's scripts/publish.sh.)
set -eu
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/.." && pwd)
: "${S3_BUCKET:?S3_BUCKET must be set}"
[ -f "$ROOT/dist/index.html" ] || { echo "missing $ROOT/dist/index.html — run the build first" >&2; exit 1; }
echo "Publishing core shell to s3://$S3_BUCKET/index.html"
aws s3 cp "$ROOT/dist/index.html" "s3://$S3_BUCKET/index.html" --cache-control 'no-cache'
