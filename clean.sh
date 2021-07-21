#!/bin/bash

. config.txt

trace_vol=${TRACE_VOL}
result_vol=${RESULT_VOL}


function delete_vol() {
  docker volume rm $trace_vol
  docker volume rm $result_vol
  echo "all volumes deleted"
}

docker rm $(docker ps -aq)

delete_vol





