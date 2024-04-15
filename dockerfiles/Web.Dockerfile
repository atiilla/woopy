FROM bitnami/python:3.11

WORKDIR /app
# Install system dependencies: cmake, jdk17, ant, maven, gradle, libcairo2-dev, pkg-config
RUN install_packages cmake libcairo2-dev pkg-config libgirepository1.0-dev python3-dev python3-pip python3-venv

RUN pip3 install --upgrade pip
RUN python3 -m venv venv
RUN . venv/bin/activate

COPY ../web/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ../web/__init__.py app/__init__.py
COPY ../web/__main__.py app/__main__.py
COPY ../web/web.py app/web.py
COPY ../web/.env app/.env

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000
