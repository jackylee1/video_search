#!/usr/bin/sh

docker build -t videosearch -f Dockerfile .
docker run -d --name videosearch -p 80:5000/tcp videosearch
