#!/bin/bash

docker build --tag docker.io/yilmazchef/woopy:latest .
docker push docker.io/yilmazchef/woopy:latest
docker pull docker.io/yilmazchef/woopy
docker stop woopy && docker rm woopy
docker run -p 5000:5000 --name=woopy -d docker.io/yilmazchef/woopy:latest

