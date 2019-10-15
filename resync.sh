#!/usr/bin/sh

docker build -t videosearch -f Dockerfile.extend .
docker stop videosearch && docker rm videosearch
docker run -d --name videosearch -p 80:5000/tcp videosearch
