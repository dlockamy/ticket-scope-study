#!/bin/bash
# Keeps the Docker VM clock equal to the host clock; logs the skew found before each correction (evidence of drift).
docker rm -f clocksync >/dev/null 2>&1; docker run -d --name clocksync --privileged alpine sleep infinity >/dev/null
LOG=$HOME/study-mfe/s2/results/clock.log
while true; do
  h=$(date +%s); v=$(docker exec clocksync date +%s 2>/dev/null) || { sleep 2; continue; }
  s=$((h - v)); [ "$s" -gt 2 -o "$s" -lt -2 ] && echo "$(date +%H:%M:%S) skew_found=${s}s" >> $LOG
  [ "$s" -ne 0 ] && docker exec clocksync date -s "@$(date +%s)" >/dev/null 2>&1
  sleep 4
done
