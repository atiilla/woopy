FROM bitnami/python:3.11

WORKDIR /app
# Install system dependencies: cmake, jdk17, ant, maven, gradle, libcairo2-dev, pkg-config
RUN install_packages cmake libcairo2-dev pkg-config libgirepository1.0-dev python3-dev python3-pip python3-venv

RUN pip3 install --upgrade pip
RUN python3 -m venv venv
RUN . venv/bin/activate

COPY requirements.txt /app/requirements.txt
COPY src /app/src
COPY test /app/test
COPY res /app/res

RUN pip3 install -r /app/requirements.txt

CMD ["python3", "/app/src/web.py"]

