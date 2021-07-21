#!/bin/bash

. config.txt

tag=${TAG}
docker_image=${IMAGE}

docker build --build-arg JAR_VERSION=${JAR_VERSION} --build-arg TRACE_FILE=${TRACE_FILE} -t ${docker_image}:${tag} -f src/Dockerfile ./src


