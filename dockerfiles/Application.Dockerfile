FROM bitnami/python:3.11

WORKDIR /app
# Install system dependencies: cmake, jdk17, ant, maven, gradle, libcairo2-dev, pkg-config
RUN install_packages cmake openjdk-17-jdk ant maven gradle libcairo2-dev pkg-config libgirepository1.0-dev python3-dev python3-pip python3-venv

RUN pip3 install --upgrade pip
RUN python3 -m venv venv
RUN . venv/bin/activate

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# podman run -it --rm --name=vinci application:latest bash