#!/bin/bash

tag="v3-arm"
docker_image="nan42/eval"
result_dir="out/result-"${tag}
trace_dir="out/trace-"${tag}
compare_method="position"
compare_window=100

trace_vol="trace"
result_vol="result"

function run() {
  docker volume create ${trace_vol}
  docker volume create ${result_vol}

  echo ${compare_method}

  for threshold in 24
  do
    for seed in 300
    do
      echo $threshold
      echo $seed
      docker run -d \
      --mount source=${result_vol},target=/experiments/runner/result \
      --mount source=${trace_vol},target=/experiments/simulator/trace/prediction \
      --name ${compare_method}_t${threshold}_s${seed} \
      ${docker_image}:${tag} -t $threshold -s $seed -c $compare_method -w $compare_window
    done
  done
}

# copy output to local host
function collect() {
  CID=$(docker run -d -v "${trace_vol}":/trace -v "${result_vol}":/result busybox true)
  mkdir ${result_dir}
  mkdir ${trace_dir}
  docker cp $CID:/trace ./${trace_dir}
  docker cp $CID:/result ./${result_dir}
  echo "copy done"
  docker rm $CID
}

function delete_vol() {
  docker volume rm $trace_vol
  docker volume rm $result_vol
  echo "all volumes deleted"
}

collect





