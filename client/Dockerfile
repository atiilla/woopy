FROM bitnami/python:3.11

WORKDIR /app
# Install system dependencies: cmake, jdk17, ant, maven, gradle, libcairo2-dev, pkg-config
RUN install_packages cmake libcairo2-dev pkg-config libgirepository1.0-dev python3-dev python3-pip python3-venv

RUN pip3 install --upgrade pip
RUN python3 -m venv venv
RUN . venv/bin/activate

COPY requirements.txt requirements.txt
COPY __init__.py __init__.py
COPY __main__.py __main__.py
COPY web.py web.py
COPY .env .env

RUN pip3 install -r requirements.txt

ENV FLASK_APP=web.py

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000

# podman run --rm -it -p 5000:5000 --name=woopy-web woopy-web:latest
