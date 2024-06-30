#!/bin/bash

docker build --tag docker.io/yilmazchef/woopy:latest .
docker push docker.io/yilmazchef/woopy:latest
docker pull docker.io/yilmazchef/woopy
docker stop woopy && docker rm woopy
docker run -p 5000:5000 -e FLASK_APP=app.py -e FLASK_ENV=development -e FLASK_DEBUG=1 -e FLASK_HOST=0.0.0.0 -e FLASK_PORT=5000 --name woopy -d docker.io/yilmazchef/woopy:latest
