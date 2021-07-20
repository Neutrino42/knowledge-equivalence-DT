#!/bin/bash

. config.txt

tag=${TAG}
docker_image=${IMAGE}
trace_vol=${TRACE_VOL}
result_vol=${RESULT_VOL}

compare_method="interaction"
compare_window=1000


function run() {
  docker volume create ${trace_vol}
  docker volume create ${result_vol}

  echo ${compare_method}

  for threshold in 70
  do
    for seed in 100 200 300 400 500
    do
      for tau in 1 2 3 5
      do
          echo $threshold
          echo $seed
          echo $tau
          docker run -d \
          --mount source=${result_vol},target=/experiments/runner/result \
          --mount source=${trace_vol},target=/experiments/simulator/trace/prediction \
          --name ${compare_method}_t${threshold}_${tau}_s${seed} \
          ${docker_image}:${tag} -t $threshold -s $seed -c $compare_method -w $compare_window -a $tau &
      done
    done
  done
}

run





