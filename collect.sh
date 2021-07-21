#!/bin/bash

. config.txt

tag=${TAG}
trace_vol=${TRACE_VOL}
result_vol=${RESULT_VOL}

result_dir="out/result-"${tag}
trace_dir="out/trace-"${tag}

# copy output to local host
function collect() {
  CID=$(docker run -d -v "${trace_vol}":/trace -v "${result_vol}":/result busybox true)
  mkdir -p ${result_dir}
  mkdir -p ${trace_dir}
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





