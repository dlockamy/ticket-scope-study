#!/bin/bash
# Stop (do not remove) the study services. State is kept in the containers/volume; /tmp/study is untouched.
docker stop study-jenkins study-registry localstack-mfe
