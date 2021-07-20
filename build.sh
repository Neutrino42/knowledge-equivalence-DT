#!/bin/bash

. config.txt

tag=${TAG}
docker_image=${IMAGE}

docker build -t ${docker_image}:${tag} -f src/Dockerfile ./src


