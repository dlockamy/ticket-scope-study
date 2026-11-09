#!/bin/bash
# Runs all case x arm review jobs, 6 at a time, up to 3 passes (retry anything that did not complete). Needs the login to be valid.
B=/tmp/s2-review; S=$HOME/study-mfe/s2
for pass in 1 2 3; do
  python3 - <<'PY' > $B/jobs.txt
import itertools, random, os, json
cases = sorted(os.listdir('/tmp/s2-review/cases')); arms = ['V0','V1','V2','V3','V4']
jobs = [(c, a) for c in cases for a in arms
        if not (os.path.exists(f'/tmp/s2-review/out/{c}-{a}.json') and json.load(open(f'/tmp/s2-review/out/{c}-{a}.json')).get('terminal_reason') == 'completed')]
random.Random(7 + len(jobs)).shuffle(jobs)
for c, a in jobs: print(c, a)
PY
  n=$(wc -l < $B/jobs.txt); echo "$(date +%T) pass $pass: $n jobs"; [ "$n" = 0 ] && break
  cat $B/jobs.txt | xargs -P 6 -L 1 bash $S/bin/review-job.sh
done
echo "$(date +%T) reviews finished"
