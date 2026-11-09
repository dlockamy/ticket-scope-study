#!/bin/bash
S=$HOME/study-mfe/s2
bash $S/bin/run-matrix4.sh $S/queue7.json > $S/results/matrix-driver-phase8.log 2>&1
bash $S/bin/run-matrix4.sh $S/queue8.json > $S/results/matrix-driver-phase9.log 2>&1
