#!/bin/bash

docker run -it -v ${PWD}"/runner":/experiments/runner -v ${PWD}"/out-test":/experiments/simulator/trace/prediction --name dev-env nan42/eval:dev-runner bash

#  python3 Main.py -t 20 -s 100 -c position -w 100
