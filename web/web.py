import logging
import os
import secrets
import tempfile
from datetime import datetime

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = Api(app)

CORS(app)


def generate_password() -> str:
    """
    Generate a random password
    """
    # Generate a random token
    token = secrets.token_urlsafe(16)
    return token


class Database:
    """
    Database class: This class is used to create a database for the website
    """

    def __init__(self, database_name, database_user, database_host, database_port: int = 3306,
                 database_character_set: str = 'utf-8', database_table_prefix: str = "wpapp_"):
        self.database_name = database_name
        self.database_user = database_user
        self.database_password = generate_password()
        self.database_root_password = generate_password()
        self.database_host = database_host
        self.database_port = database_port
        self.database_character_set = database_character_set
        self.database_table_prefix = database_table_prefix

    # String representation of the class is docker-compose.yml data
    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the database
        """
        return f"""
    database:
        image: mariadb:11.1
        container_name: database
        volumes:
            - database-data:/var/lib/mysql
        environment:
            MARIADB_DATABASE: {self.database_name}
            MARIADB_USER: {self.database_user}
            MARIADB_PASSWORD: {self.database_password}
            MARIADB_ROOT_PASSWORD: {self.database_root_password}
            MARIADB_HOST: {self.database_host}
            MARIADB_PORT_NUMBER: {self.database_port}
            MARIADB_CHARACTER_SET: {self.database_character_set}
        networks:
            - website-network
        restart: unless-stopped
        healthcheck:
            test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
            interval: 10s
            timeout: 5s
            retries: 5
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"
        """

    def to_kubernetes(self):
        """
        This function returns the kubernetes data for the database
        """
        return f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: database
          labels:
            app: database
        spec:
            ports:
            - port: 3306
                targetPort: 3306
            selector:
                app: database
            type: ClusterIP
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
            name: database
            labels:
                app: database
        spec:
            selector:
                matchLabels:
                    app: database
            template:
                metadata:
                    labels:
                        app: database
                spec:
                    containers:
                    - name: database
                        image: mariadb:11.1
                        ports:
                        - containerPort: 3306
                        env:
                        - name: MARIADB_DATABASE
                            value: {self.database_name}
                        - name: MARIADB_USER
                            value: {self.database_user}
                        - name: MARIADB_PASSWORD
                            value: {self.database_password}
                        - name: MARIADB_ROOT_PASSWORD
                            value: {self.database_root_password}
                        - name: MARIADB_HOST
                            value: {self.database_host}
                        - name: MARIADB_PORT_NUMBER
                            value: {self.database_port}
                        - name: MARIADB_CHARACTER_SET
                            value: {self.database_character_set}
        """

    def to_vagrant_vm(self):
        """
        This function returns the vagrant data for the database
        """
        return f"""
        config.vm.define "database" do |database|
            database.vm.box = "ubuntu/focal64"
            database.vm.hostname = "database"
            database.vm.network "private_network", ip: "
            database.vm.provider "virtualbox" do |vb|
                vb.memory = "1024"
                vb.cpus = "1"
            end
            database.vm.provision "shell", inline: <<-SHELL
                sudo apt-get update
                sudo apt-get install -y mariadb-server
                sudo sed -i 's/bind-address/#bind-address/g' /etc/mysql/mariadb.conf.d/50-server.cnf
                sudo systemctl restart mariadb
                sudo mysql -e "CREATE DATABASE {self.database_name};"
                sudo mysql -e "CREATE USER '{self.database_user}'@'%' IDENTIFIED BY '{self.database_password}';"
                sudo mysql -e "GRANT ALL PRIVILEGES ON {self.database_name}.* TO '{self.database_user}'@'%';"
                sudo mysql -e "FLUSH PRIVILEGES;"
            SHELL
        end
        """


class Cache:
    """
    Cache class: This class is used to create a cache for the website
    """

    def __init__(self, cache_host, cache_port, cache_username: str = "root"):
        self.cache_host = cache_host
        self.cache_port = cache_port
        self.cache_username = cache_username
        self.cache_password = generate_password()

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the cache
        """
        return f"""
    cache:
        image: redis:latest
        container_name: cache
        environment:
            REDIS_HOST: {self.cache_host}
            REDIS_PORT_NUMBER: {self.cache_port}
            REDIS_USERNAME: {self.cache_username}
            REDIS_PASSWORD: {self.cache_password}
            REDIS_DATABASE_NUMBER: "0"
            REDIS_DISABLE_COMMANDS: "FLUSHDB,FLUSHALL"
            REDIS_APPENDONLY: "yes"
            REDIS_MAXMEMORY: "256mb"
            REDIS_MAXMEMORY_POLICY: "allkeys-lru"
        volumes:
            - cache-data:/data
        networks:
            - website-network
        depends_on:
            - website
        labels:
            - "traefik.enable=false"
        restart: unless-stopped
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"
        """

    def to_kubernetes(self):
        """
        This function returns the kubernetes data for the cache
        """
        return f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: cache
          labels:
            app: cache
        spec:
            ports:
            - port: 6379
                targetPort: 6379
            selector:
                app: cache
            type: ClusterIP
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
            name: cache
            labels:
                app: cache
        spec:
            selector:
                matchLabels:
                    app: cache
            template:
                metadata:
                    labels:
                        app: cache
                spec:
                    containers:
                    - name: cache
                        image: redis:latest
                        ports:
                        - containerPort: 6379
                        env:
                        - name: REDIS_HOST
                            value: {self.cache_host}
                        - name: REDIS_PORT_NUMBER
                            value: {self.cache_port}
                        - name: REDIS_USERNAME
                            value: {self.cache_username}
                        - name: REDIS_PASSWORD
                            value: {self.cache_password}
                        - name: REDIS_DATABASE_NUMBER
                            value: "0"
                        - name: REDIS_DISABLE_COMMANDS
                            value: "FLUSHDB,FLUSHALL"
                        - name: REDIS_APPENDONLY
                            value: "yes"
                        - name: REDIS_MAXMEMORY
                            value: "256mb"
                        - name: REDIS_MAXMEMORY_POLICY
                            value: "allkeys-lru"
        """

    def to_vagrant_vm(self):
        """
        This function returns the vagrant data for the cache
        """
        return """
        config.vm.define "cache" do |cache|
            cache.vm.box = "ubuntu/focal64"
            cache.vm.hostname = "cache"
            cache.vm.network "private_network", ip: "
            cache.vm.provider "virtualbox" do |vb|
                vb.memory = "1024"
                vb.cpus = "1"
            end
            cache.vm.provision "shell", inline: <<-SHELL
                sudo apt-get update
                sudo apt-get install -y redis-server
                sudo sed -i 's/bind
            SHELL
        end
        """


class Mail:
    """
    Mail class: This class is used to create a mail server for the website
    """

    def __init__(self, mail_hostname: str, mail_username: str, mail_port: int = 587, mail_encryption: str = "tls",
                 mail_protocol: str = "smtp"):
        self.mail_hostname = mail_hostname
        self.mail_username = mail_username
        self.mail_password = generate_password()
        self.mail_port = mail_port
        self.mail_encryption = mail_encryption
        self.mail_protocol = mail_protocol

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the mail server
        """
        return f"""
    mail:
        image: mailhog/mailhog
        container_name: mail
        environment:
            - MH_UI_BIND_ADDR={self.mail_hostname}:8025
            - MH_SMTP_BIND_ADDR={self.mail_hostname}:1025
            - MH_API_BIND_ADDR={self.mail_hostname}:8025
            - MH_UI_WEB_PATH=/
        ports:
            - "8025:8025"
            - "1025:1025"
        networks:
            - proxy-network
        depends_on:
            - website
        labels:
            - "traefik.enable=false"
        restart: unless-stopped
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"
        """

    def to_kubernetes(self):
        """
        This function returns the kubernetes data for the mail server
        """
        return """
        apiVersion: v1
        kind: Service
        metadata:
          name: mail
          labels:
            app: mail
        spec:
            ports:
            - port: 8025
                targetPort: 8025
            - port: 1025
                targetPort: 1025
            selector:
                app: mail
            type: ClusterIP
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
            name: mail
            labels:
                app: mail
        spec:
            selector:
                matchLabels:
                    app: mail
            template:
                metadata:
                    labels:
                        app: mail
                spec:
                    containers:
                    - name: mail
                        image: mailhog/mailhog
                        ports:
                        - containerPort: 8025
                        - containerPort: 1025
        """

    def to_vagrant_vm(self):
        """
        This function returns the vagrant data for the mail server
        """
        return """
        config.vm.define "mail" do |mail|
            mail.vm.box = "ubuntu/focal64"
            mail.vm.hostname = "mail"
            mail.vm.network "private_network", ip: "
            mail.vm.provider "virtualbox" do |vb|
                vb.memory = "1024"
                vb.cpus = "1"
            end
            mail.vm.provision "shell", inline: <<-SHELL
                sudo apt-get update
                sudo apt-get install -y apache2-utils
                sudo apt-get install -y apt-transport-https
                sudo apt-get install -y ca-certificates
                sudo apt-get install -y curl
                sudo apt-get install -y gnupg
                sudo apt-get install -y lsb-release
                sudo apt-get install -y wget
                sudo apt-get install -y redis-server
                sudo apt-get install -y mariadb-client
                sudo apt-get install -y unzip
                sudo apt-get install -y docker.io
                sudo apt-get install -y docker-compose
                sudo apt-get install -y apache2
                sudo apt-get install -y php
                sudo apt-get install -y php-mysql
                sudo apt-get install -y php-curl
                sudo apt-get install -y php-gd
                sudo apt-get install -y php-intl
                sudo apt-get install -y php-mbstring
                sudo apt-get install -y php-soap
                sudo apt-get install -y php-xml
                sudo apt-get install -y php-xmlrpc
                sudo apt-get install -y php-zip
                sudo systemctl enable docker
                sudo systemctl start docker
                sudo systemctl enable apache2
                sudo systemctl start apache2
                sudo wget
            SHELL
        end
        """


class Website:
    """
    Website class: This class is used to create a website for the user
    """

    def __init__(self, title: str, description: str, host: str, user: str, email: str, database: Database, mail: Mail, cache: Cache):
        self.database_host = f"{database.database_host}"
        self.database_port = f"{database.database_port}"
        self.database_name = f"{database.database_name}"
        self.database_user = f"{database.database_user}"
        self.database_password = f"{database.database_password}"
        self.database_table_prefix = f"{database.database_table_prefix}"
        self.website_hostname = f"{host}"
        self.website_title = f"{title}"
        self.website_description = f"{description}"
        self.website_admin_username = f"{user}"
        # generate a hashed password with SHA-256 and base64 encoding
        self.website_admin_password = generate_password()
        self.website_admin_email = f"{email}"
        self.mail_smtp_host = f"{mail.mail_hostname}"
        self.mail_smtp_port = f"{mail.mail_port}"
        self.mail_smtp_user = f"{mail.mail_username}"
        self.mail_smtp_password = f"{mail.mail_password}"
        self.mail_smtp_protocol = f"{mail.mail_encryption}"
        self.cache_host = f"{cache.cache_host}"
        self.cache_port = f"{cache.cache_port}"
        self.cache_password = f"{cache.cache_password}"

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the website
        """
        return f"""
    website:
        image: bitnami/wordpress:latest
        container_name: website
        volumes:
            - website-data:/bitnami/wordpress
        environment:
            WORDPRESS_DATABASE_HOST: {self.database_host}
            WORDPRESS_DATABASE_PORT_NUMBER: {self.database_port}
            WORDPRESS_DATABASE_NAME: {self.database_name}
            WORDPRESS_DATABASE_USER: {self.database_user}
            WORDPRESS_DATABASE_PASSWORD: {self.database_password}
            WORDPRESS_TABLE_PREFIX: {self.database_table_prefix}
            WORDPRESS_BLOG_NAME: {self.website_title}
            WORDPRESS_USERNAME: {self.website_admin_username}
            WORDPRESS_PASSWORD: {self.website_admin_password}
            WORDPRESS_EMAIL: {self.website_admin_email}
            WORDPRESS_SMTP_HOST: {self.mail_smtp_host}
            WORDPRESS_SMTP_PORT: {self.mail_smtp_port}
            WORDPRESS_SMTP_USER: {self.mail_smtp_user}
            WORDPRESS_SMTP_PASSWORD: {self.mail_smtp_password}
            WORDPRESS_SMTP_PROTOCOL: {self.mail_smtp_protocol}
            WORDPRESS_CACHE_ENABLED: "true"
            WORDPRESS_CACHE_DURATION: "1440"
            WORDPRESS_CACHE_TYPE: "redis"
            WORDPRESS_REDIS_HOST: {self.cache_host}
            WORDPRESS_REDIS_PORT: {self.cache_port}
            WORDPRESS_REDIS_DATABASE: "0"
            WORDPRESS_REDIS_PASSWORD: {self.cache_password}
        networks:
            - website-network
            - proxy-network
        depends_on:
            - database
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.wordpress.rule=Host(`{self.website_hostname}`)"
            - "traefik.http.routers.wordpress.service=wordpress"
            - "traefik.http.routers.wordpress.entrypoints=websecure"
            - "traefik.http.services.wordpress.loadbalancer.server.port=8080"
            - "traefik.http.routers.wordpress.tls=true"
            - "traefik.http.routers.wordpress.tls.certresolver=letsencrypt"
            - "traefik.http.services.wordpress.loadbalancer.passhostheader=true"
            - "traefik.http.routers.wordpress.middlewares=compresstraefik"
            - "traefik.http.middlewares.compresstraefik.compress=true"
            - "traefik.docker.network=proxy-network"
        restart: unless-stopped
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"
        """

    def to_kubernetes(self):
        """
        This function returns the kubernetes data for the website
        """
        return f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: website
          labels:
            app: website
        spec:
            ports:
            - port: 8080
                targetPort: 8080
            selector:
                app: website
            type: ClusterIP
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
            name: website
            labels:
                app: website
        spec:
            selector:
                matchLabels:
                    app: website
            template:
                metadata:
                    labels:
                        app: website
                spec:
                    containers:
                    - name: website
                        image: bitnami/wordpress:latest
                        ports:
                        - containerPort: 8080
                        env:
                        - name: WORDPRESS_DATABASE_HOST
                            value: {self.database_host}
                        - name: WORDPRESS_DATABASE_PORT_NUMBER
                            value: {self.database_port}
                        - name: WORDPRESS_DATABASE_NAME
                            value: {self.database_name}
                        - name: WORDPRESS_DATABASE_USER
                            value: {self.database_user}
                        - name: WORDPRESS_DATABASE_PASSWORD
                            value: {self.database_password}
                        - name: WORDPRESS_TABLE_PREFIX
                            value: {self.database_table_prefix}
                        - name: WORDPRESS_BLOG_NAME
                            value: {self.website_title}
                        - name: WORDPRESS_USERNAME
                            value: {self.website_admin_username}
                        - name: WORDPRESS_PASSWORD
                            value: {self.website_admin_password}
                        - name: WORDPRESS_EMAIL
                            value: {self.website_admin_email}
                        - name: WORDPRESS_SMTP_HOST
                            value: {self.mail_smtp_host}
                        - name: WORDPRESS_SMTP_PORT
                            value: {self.mail_smtp_port}
                        - name: WORDPRESS_SMTP_USER
                            value: {self.mail_smtp_user}
                        - name: WORDPRESS_SMTP_PASSWORD
                            value: {self.mail_smtp_password}
                        - name: WORDPRESS_SMTP_PROTOCOL
                            value: {self.mail_smtp_protocol}
                        - name: WORDPRESS_CACHE_ENABLED
                            value: "true"
                        - name: WORDPRESS_CACHE_DURATION
                            value: "1440"
                        - name: WORDPRESS_CACHE_TYPE
                            value: "redis"
                        - name: WORDPRESS_REDIS_HOST
                            value: {self.cache_host}
                        - name: WORDPRESS_REDIS_PORT
                            value: {self.cache_port}
                        - name: WORDPRESS_REDIS_DATABASE
                            value: "0"
                        - name: WORDPRESS_REDIS_PASSWORD
                            value: {self.cache_password}
        """

    def to_vagrant_vm(self):
        """
        This function returns the vagrant data for the website
        """
        return """
        config.vm.define "website" do |website|
            website.vm.box = "ubuntu/focal64"
            website.vm.hostname = "website"
            website.vm.network "private_network", ip: "
            website.vm.provider "virtualbox" do |vb|
                vb.memory = "1024"
                vb.cpus = "1"
            end
            website.vm.provision "shell", inline: <<-SHELL
                sudo apt-get update
                sudo apt-get install -y apache2
                sudo apt-get install -y php
                sudo apt-get install -y php-mysql
                sudo apt-get install -y php-curl
                sudo apt-get install -y php-gd
                sudo apt-get install -y php-intl
                sudo apt-get install -y php-mbstring
                sudo apt-get install -y php-soap
                sudo apt-get install -y php-xml
                sudo apt-get install -y php-xmlrpc
                sudo apt-get install -y php-zip
                sudo apt-get install -y mariadb-client
                sudo apt-get install -y unzip
                sudo apt-get install -y wget
                sudo wget https://wordpress.org/latest.zip
                sudo unzip latest.zip -d /var/www/html/
                sudo chown -R www-data:www-data /var/www/html/wordpress
                sudo chmod -R 755 /var/www/html/wordpress
                sudo sed -i 's/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/g' /etc/php/7.4/apache2/php.ini
                sudo systemctl restart apache2
            SHELL
        end
        """


class Admin:
    """
    Admin class: This class is used to create an admin panel for the website
    """

    def __init__(self, database: Database, website: Website):
        self.database_host = f"{database.database_host}"
        self.database_port = f"{database.database_port}"
        self.database_user = f"{database.database_user}"
        self.database_password = f"{database.database_password}"
        self.website_hostname = f"{website.website_hostname}"
        self.website_admin_username = f"{website.website_admin_username}"
        self.website_admin_password = f"{website.website_admin_password}"

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the admin panel
        """
        return f"""
    admin:
        image: phpmyadmin:latest
        container_name: admin
        environment:
            PMA_HOST: {self.database_host}
            PMA_PORT: {self.database_port}
            PMA_USER: {self.database_user}
            PMA_PASSWORD: {self.database_password}
            PMA_ARBITRARY: 1
        networks:
            - website-network
            - proxy-network
        depends_on:
            - database
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.phpmyadmin.rule=Host(`phpmyadmin.{self.website_hostname}`)"
            - "traefik.http.routers.phpmyadmin.service=phpmyadmin"
            - "traefik.http.routers.phpmyadmin.entrypoints=websecure"
            - "traefik.http.services.phpmyadmin.loadbalancer.server.port=80"
            - "traefik.http.routers.dashboard.middlewares=authtraefik"
            - "traefik.http.middlewares.authtraefik.basicauth.users={self.website_admin_username}:{self.website_admin_password}"
            - "traefik.http.routers.phpmyadmin.tls=true"
            - "traefik.http.routers.phpmyadmin.tls.certresolver=letsencrypt"
            - "traefik.http.services.phpmyadmin.loadbalancer.passhostheader=true"
            - "traefik.docker.network=proxy-network"
        restart: unless-stopped
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"
        """

    def to_kubernetes(self):
        """
        This function returns the kubernetes data for the admin panel
        """
        return f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: admin
          labels:
            app: admin
        spec:
            ports:
            - port: 80
                targetPort: 80
            selector:
                app: admin
            type: ClusterIP
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
            name: admin
            labels:
                app: admin
        spec:
            selector:
                matchLabels:
                    app: admin
            template:
                metadata:
                    labels:
                        app: admin
                spec:
                    containers:
                    - name: admin
                        image: phpmyadmin:latest
                        ports:
                        - containerPort: 80
                        env:
                        - name: PMA_HOST
                            value: {self.database_host}
                        - name: PMA_PORT
                            value: {self.database_port}
                        - name: PMA_USER
                            value: {self.database_user}
                        - name: PMA_PASSWORD
                            value: {self.database_password}
                        - name: PMA_ARBITRARY
                            value: 1
        """

    def to_vagrant_vm(self):
        """
        This function returns the vagrant data for the admin panel
        """
        return """
        config.vm.define "admin" do |admin|
            admin.vm.box = "ubuntu/focal64"
            admin.vm.hostname = "admin"
            admin.vm.network "private_network", ip: "
            admin.vm.provider "virtualbox" do |vb|
                vb.memory = "1024"
                vb.cpus = "1"
            end
            admin.vm.provision "shell", inline: <<-SHELL
                sudo apt-get update
                sudo apt-get install -y phpmyadmin
                sudo sed -i 's/
            SHELL
        end
        """


class Proxy:
    """
    Proxy class: This class is used to create a proxy for the website
    """

    def __init__(self, title: str, host: str, website: Website, port: int = 443, username: str = "root"):
        self.website_hostname = f"{website.website_hostname}"
        self.website_admin_email = f"{website.website_admin_email}"
        self.website_admin_username = f"{website.website_admin_username}"
        self.website_admin_password = f"{website.website_admin_email}"
        self.proxy_title = f"{title}"
        self.proxy_host = f"{host}"
        self.proxy_port = f"{port}"
        self.proxy_username = f"{username}"
        self.proxy_email = f"{username}@{host}"
        self.proxy_password = generate_password()

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the proxy
        """
        return f"""
    proxy:
        image: traefik:2.9
        container_name: proxy
        command:
            - "--log.level=WARN"
            - "--accesslog=true"
            - "--api.dashboard=true"
            - "--api.insecure=true"
            - "--ping=true"
            - "--ping.entrypoint=ping"
            - "--entryPoints.ping.address=:8082"
            - "--entryPoints.web.address=:80"
            - "--entryPoints.websecure.address=:443"
            - "--providers.docker=true"
            - "--providers.docker.endpoint=unix:///var/run/docker.sock"
            - "--providers.docker.exposedByDefault=false"
            - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
            - "--certificatesresolvers.letsencrypt.acme.email={self.website_admin_email}"
            - "--certificatesresolvers.letsencrypt.acme.storage=/etc/traefik/acme/acme.json"
            - "--metrics.prometheus=true"
            - "--metrics.prometheus.buckets=0.1,0.3,1.2,5.0"
            - "--global.checkNewVersion=true"
            - "--global.sendAnonymousUsage=false"
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
            - proxy-data:/etc/traefik/acme
        networks:
            - proxy-network
        depends_on:
            - website
        ports:
            - "8080:80"
            - "443:443"
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.dashboard.rule=Host(`traefik.{self.website_hostname}`)"
            - "traefik.http.routers.dashboard.service=api@internal"
            - "traefik.http.routers.dashboard.entrypoints=websecure"
            - "traefik.http.services.dashboard.loadbalancer.server.port=8080"
            - "traefik.http.routers.dashboard.tls=true"
            - "traefik.http.routers.dashboard.tls.certresolver=letsencrypt"
            - "traefik.http.services.dashboard.loadbalancer.passhostheader=true"
#      - "traefik.http.routers.dashboard.middlewares=authtraefik"
#      - "traefik.http.middlewares.authtraefik.basicauth.users={self.website_admin_username}:{self.website_admin_password}"
            - "traefik.http.routers.http-catchall.rule=HostRegexp(`{{host:.+}}`)"
            - "traefik.http.routers.http-catchall.entrypoints=web"
            - "traefik.http.routers.http-catchall.middlewares=redirect-to-https"
            - "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https"
        restart: unless-stopped
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"
        """

    def to_kubernetes(self):
        """
        This function returns the kubernetes data for the proxy
        """
        return f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: proxy
          labels:
            app: proxy
        spec:
            ports:
            - port: 80
                targetPort: 80
            - port: 443
                targetPort: 443
            selector:
                app: proxy
            type: ClusterIP
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
            name: proxy
            labels:
                app: proxy
        spec:
            selector:
                matchLabels:
                    app: proxy
            template:
                metadata:
                    labels:
                        app: proxy
                spec:
                    containers:
                    - name: proxy
                        image: traefik:2.9
                        ports:
                        - containerPort: 80
                        - containerPort: 443
                        args:
                        - "--log.level=WARN"
                        - "--accesslog=true"
                        - "--api.dashboard=true"
                        - "--api.insecure=true"
                        - "--ping=true"
                        - "--ping.entrypoint=ping"
                        - "--entryPoints.ping.address=:8082"
                        - "--entryPoints.web.address=:80"
                        - "--entryPoints.websecure.address=:443"
                        - "--providers.docker=true"
                        - "--providers.docker.endpoint=unix:///var/run/docker.sock"
                        - "--providers.docker.exposedByDefault=false"
                        - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
                        - "--certificatesresolvers.letsencrypt.acme.email={self.website_admin_email}"
                        - "--certificatesresolvers.letsencrypt.acme.storage=/etc/traefik/acme/acme.json"
                        - "--metrics.prometheus=true"
                        - "--metrics.prometheus.buckets=0.1,0.3,1.2,5.0"
                        - "--global.checkNewVersion=true"
                        - "--global.sendAnonymousUsage=false"
                        volumeMounts:
                        - mountPath: /var/run/docker.sock
                            name: docker-socket
                        - mountPath: /etc/traefik/acme
                            name: acme-storage
                    volumes:
                    - name: docker-socket
                        hostPath:
                        path: /var/run/docker.sock
                    - name: acme-storage
                        hostPath:
                        path: /etc/traefik/acme
        """

    def to_vagrant_vm(self):
        """
        This function returns the vagrant data for the proxy
        """
        return """
        config.vm.define "proxy" do |proxy|
            proxy.vm.box = "ubuntu/focal64"
            proxy.vm.hostname = "proxy"
            proxy.vm.network "private_network", ip: "
            proxy.vm.provider "virtualbox" do |vb|
                vb.memory = "1024"
                vb.cpus = "1"
            end
            proxy.vm.provision "shell", inline: <<-SHELL
                sudo apt-get update
                sudo apt-get install -y apache2-utils
                sudo apt-get install -y apt-transport-https
                sudo apt-get install -y ca-certificates
                sudo apt-get install -y curl
                sudo apt-get install -y gnupg
                sudo apt-get install -y lsb-release
                sudo apt-get install -y wget
                sudo apt-get install -y redis-server
                sudo apt-get install -y mariadb-client
                sudo apt-get install -y unzip
                sudo apt-get install -y docker.io
                sudo apt-get install -y docker-compose
                sudo apt-get install -y apache2
                sudo apt-get install -y php
                sudo apt-get install -y php-mysql
                sudo apt-get install -y php-curl
                sudo apt-get install -y php-gd
                sudo apt-get install -y php-intl
                sudo apt-get install -y php-mbstring
                sudo apt-get install -y php-soap
                sudo apt-get install -y php-xml
                sudo apt-get install -y php-xmlrpc
                sudo apt-get install -y php-zip
                sudo systemctl enable docker
                sudo systemctl start docker
                sudo systemctl enable apache2
                sudo systemctl start apache2
                sudo wget
            SHELL
        end
        """


class Monitoring:
    """
    Monitoring class: This class is used to create a monitoring system for the host
    """

    def __init__(self, host_hostname: str, host_ip, host_mac, host_cpu, host_ram, host_os, host_kernel, host_docker,
                 monitoring_host: str = "monitoring", monitoring_port: int = 8080, monitoring_username: str = "root"):
        self.host_hostname = host_hostname
        self.host_ip = host_ip
        self.host_mac = host_mac
        self.host_cpu = host_cpu
        self.host_ram = host_ram
        self.host_os = host_os
        self.host_kernel = host_kernel
        self.host_docker = host_docker
        self.monitoring_host = monitoring_host
        self.monitoring_port = monitoring_port
        self.monitoring_username = monitoring_username
        self.montiroing_email = f"{monitoring_username}@{host_hostname}"
        self.monitoring_password = generate_password()

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the monitoring system
        """
        return f"""
    monitoring:
        image: gcr.io/cadvisor/cadvisor:v0.39.0
        container_name: monitoring
        volumes:
            - /:/rootfs:ro
            - /var/run:/var/run:rw
            - /sys:/sys:ro
            - /var/lib/docker/:/var/lib/docker:ro
        environment:
            - TZ=Europe/Brussels
            - HOST_HOSTNAME={self.host_hostname}
            - HOST_IP={self.host_ip}
            - HOST_MAC={self.host_mac}
            - HOST_CPU={self.host_cpu}
            - HOST_RAM={self.host_ram}
            - HOST_OS={self.host_os}
            - HOST_KERNEL={self.host_kernel}
            - HOST_DOCKER={self.host_docker}
        networks:
            - proxy-network
        depends_on:
            - website
        labels:
            - "traefik.enable=false"
        restart: unless-stopped
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"
        """

    def to_kubernetes(self):
        """
        This function returns the kubernetes data for the monitoring system
        """
        return f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: monitoring
          labels:
            app: monitoring
        spec:
            ports:
            - port: 8080
                targetPort: 8080
            selector:
                app: monitoring
            type: ClusterIP
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
            name: monitoring
            labels:
                app: monitoring
        spec:
            selector:
                matchLabels:
                    app: monitoring
            template:
                metadata:
                    labels:
                        app: monitoring
                spec:
                    containers:
                    - name: monitoring
                        image: gcr.io/cadvisor/cadvisor:v0.39.0
                        ports:
                        - containerPort: 8080
                        volumeMounts:
                        - mountPath: /rootfs
                            name: rootfs
                            readOnly: true
                        - mountPath: /var/run
                            name: var-run
                            readOnly: false
                        - mountPath: /sys
                            name: sys
                            readOnly: true
                        - mountPath: /var/lib/docker
                            name: var-lib-docker
                            readOnly: true
                        env:
                        - name: TZ
                            value: Europe/Brussels
                        - name: HOST_HOSTNAME
                            value: {self.host_hostname}
                        - name: HOST_IP
                            value: {self.host_ip}
                        - name: HOST_MAC
                            value: {self.host_mac}
                        - name: HOST_CPU
                            value: {self.host_cpu}
                        - name: HOST_RAM
                            value: {self.host_ram}
                        - name: HOST_OS
                            value: {self.host_os}
                        - name: HOST_KERNEL
                            value: {self.host_kernel}
                        - name: HOST_DOCKER
                            value: {self.host_docker}
                    volumes:
                    - name: rootfs
                        hostPath:
                        path: /
                    - name: var-run
                        hostPath:
                        path: /var/run
                    - name: sys
                        hostPath:
                        path: /sys
                    - name: var-lib-docker
                        hostPath:
                        path: /var/lib/docker
        """

    def to_vagrant_vm(self):
        """
        This function returns the vagrant data for the monitoring system
        """
        return """
        config.vm.define "monitoring" do |monitoring|
            monitoring.vm.box = "ubuntu/focal64"
            monitoring.vm.hostname = "monitoring"
            monitoring.vm.network "private_network", ip: "
            monitoring.vm.provider "virtualbox" do |vb|
                vb.memory = "1024"
                vb.cpus = "1"
            end
            monitoring.vm.provision "shell", inline: <<-SHELL
                sudo apt-get update
                sudo apt-get install -y apache2-utils
                sudo apt-get install -y apt-transport-https
                sudo apt-get install -y ca-certificates
                sudo apt-get install -y curl
                sudo apt-get install -y gnupg
                sudo apt-get install -y lsb-release
                sudo apt-get install -y wget
                sudo apt-get install -y redis-server
                sudo apt-get install -y mariadb-client
                sudo apt-get install -y unzip
                sudo apt-get install -y docker.io
                sudo apt-get install -y docker-compose
                sudo apt-get install -y apache2
                sudo apt-get install -y php
                sudo apt-get install -y php-mysql
                sudo apt-get install -y php-curl
                sudo apt-get install -y php-gd
                sudo apt-get install -y php-intl
                sudo apt-get install -y php-mbstring
                sudo apt-get install -y php-soap
                sudo apt-get install -y php-xml
                sudo apt-get install -y php-xmlrpc
                sudo apt-get install -y php-zip
                sudo systemctl enable docker
                sudo systemctl start docker
                sudo systemctl enable apache2
                sudo systemctl start apache2
                sudo wget
            SHELL
        end
        """


class Management:
    """
    Management class: This class is used to create a management system for the website
    """

    def __init__(self, website, management_host="management", management_port=9000, management_username="root"):
        self.website_hostname = f"{website.website_hostname}"
        self.website_admin_password = f"{website.website_admin_password}"
        self.management_host = f"{management_host}"
        self.management_port = f"{management_port}"
        self.management_username = f"{management_username}"
        self.management_email = f"{management_username}@{management_host}"
        self.management_password = generate_password()

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the management system
        """
        return f"""
    management:
        image: portainer/portainer-ce:latest
        container_name: management
        command:
            -H unix:///var/run/docker.sock
            --admin-password '{self.website_admin_password}'
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
            - management-data:/data
        networks:
            - proxy-network
        depends_on:
            - website
            - database
            - cache
            - proxy
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.portainer.rule=Host(`portainer.{self.website_hostname}`)"
            - "traefik.http.routers.portainer.service=portainer"
            - "traefik.http.routers.portainer.entrypoints=websecure"
            - "traefik.http.services.portainer.loadbalancer.server.port=9000"
            - "traefik.http.routers.portainer.tls=true"
            - "traefik.http.routers.portainer.tls.certresolver=letsencrypt"
            - "traefik.http.services.portainer.loadbalancer.passhostheader=true"
        restart: unless-stopped
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"
        """

    def to_kubernetes(self):
        """
        This function returns the kubernetes data for the management system
        """
        return """
        apiVersion: v1
        kind: Service
        metadata:
          name: management
          labels:
            app: management
        spec:
            ports:
            - port: 9000
                targetPort: 9000
            selector:
                app: management
            type: ClusterIP
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
            name: management
            labels:
                app: management
        spec:
            selector:
                matchLabels:
                    app: management
            template:
                metadata:
                    labels:
                        app: management
                spec:
                    containers:
                    - name: management
                        image: portainer/portainer-ce:latest
                        ports:
                        - containerPort: 9000
                        volumeMounts:
                        - mountPath: /var/run/docker.sock
                            name: docker-socket
                        - mountPath: /data
                            name: data
                        env:
                        - name: TZ
                            value: Europe/Brussels
                    volumes:
                    - name: docker-socket
                        hostPath:
                        path: /var/run/docker.sock
                    - name: data
                        hostPath:
                        path: /data
        """

    def to_vagrant_vm(self):
        """
        This function returns the vagrant data for the management system
        """
        return """
        config.vm.define "management" do |management|
            management.vm.box = "ubuntu/focal64"
            management.vm.hostname = "management"
            management.vm.network "private_network", ip: "
            management.vm.provider "virtualbox" do |vb|
                vb.memory = "1024"
                vb.cpus = "1"
            end
            management.vm.provision "shell", inline: <<-SHELL
                sudo apt-get update
                sudo apt-get install -y apache2-utils
                sudo apt-get install -y apt-transport-https
                sudo apt-get install -y ca-certificates
                sudo apt-get install -y curl
                sudo apt-get install -y gnupg
                sudo apt-get install -y lsb-release
                sudo apt-get install -y wget
                sudo apt-get install -y redis-server
                sudo apt-get install -y mariadb-client
                sudo apt-get install -y unzip
                sudo apt-get install -y docker.io
                sudo apt-get install -y docker-compose
                sudo apt-get install -y apache2
                sudo apt-get install -y php
                sudo apt-get install -y php-mysql
                sudo apt-get install -y php-curl
                sudo apt-get install -y php-gd
                sudo apt-get install -y php-intl
                sudo apt-get install -y php-mbstring
                sudo apt-get install -y php-soap
                sudo apt-get install -y php-xml
                sudo apt-get install -y php-xmlrpc
                sudo apt-get install -y php-zip
                sudo systemctl enable docker
                sudo systemctl start docker
                sudo systemctl enable apache2
                sudo systemctl start apache2
                sudo wget
            SHELL
        end
        """


class Networks:
    """
    Networks class: This class is used to create networks for the website and the proxy
    """

    def __init__(self, website_network: str = 'website-network', proxy_network: str = 'proxy-network'):
        self.website_network = website_network
        self.proxy_network = proxy_network

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the networks
        """
        return f"""
networks:
    {self.website_network}:
        external: true
    {self.proxy_network}:
        external: true
"""


class Volumes:
    """
    Volumes class: This class is used to create volumes for the website and the proxy
    """

    def __init__(self, database_data: str = 'database-data', website_data: str = 'website-data',
                 proxy_data: str = 'proxy-data', admin_data: str = 'admin-data', cache_data: str = 'cache-data',
                 management_data: str = 'management-data', code_data: str = 'vscode-data'):
        self.database_data = database_data
        self.website_data = website_data
        self.proxy_data = proxy_data
        self.admin_data = admin_data
        self.cache_data = cache_data
        self.management_data = management_data
        self.code_data = code_data

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the volumes
        """
        return f"""
volumes:
    {self.database_data}:
    {self.website_data}:
    {self.proxy_data}:
    {self.admin_data}:
    {self.cache_data}:
    {self.management_data}:
    {self.code_data}:
"""


class Vault:
    """
    Vault class: This class is used to create a vault for the website
    """

    def __init__(self, website: Website, vault_host: str = "vault", vault_port: int = 8080,
                 vault_username: str = "root"):
        self.website_hostname = f"{website.website_hostname}"
        self.website_admin_username = f"{website.website_admin_username}"
        self.website_admin_password = f"{website.website_admin_password}"
        self.vault_host = f"{vault_host}"
        self.vault_port = f"{vault_port}"
        self.vault_username = f"{vault_username}"
        self.vault_email = f"{vault_username}@{vault_host}"
        self.vault_password = generate_password()

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the vault
        """
        return f"""
    vault:
        image: alpine:latest
        container_name: vault
        command: >
            /bin/sh -c "echo -n '{self.website_hostname}' | sha256sum &&
            echo -n '{self.website_admin_username}' | sha256sum &&
            echo -n '{self.website_admin_password}' | sha256sum"
        networks:
            - proxy-network
        depends_on:
            - website
        labels:
            - "traefik.enable=false"
        restart: unless-stopped
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"
        """

    def to_kubernetes(self):
        """
        This function returns the kubernetes data for the vault
        """
        return """
        apiVersion: v1
        kind: Service
        metadata:
          name: sha256
          labels:
            app: sha256
        spec:
            ports:
            - port: 80
                targetPort: 80
            selector:
                app: sha256
            type: ClusterIP
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
            name: sha256
            labels:
                app: sha256
        spec:
            selector:
                matchLabels:
                    app: sha256
            template:
                metadata:
                    labels:
                        app: sha256
                spec:
                    containers:
                    - name: sha256
                        image: alpine:latest
                        ports:
                        - containerPort: 80
                        command: ["/bin/sh", "-c", "while true; do sleep 30; done;"]
        """


class Code:
    """
    Code class: This class is used to create a code server for the website
    """

    def __init__(self, website: Website, code_host: str = "code", code_port: int = 8080, code_username: str = "root",
                 proxy_domain: str = "proxy", proxy_port: int = 8080):
        self.website_hostname = f"{website.website_hostname}"
        self.website_admin_password = f"{website.website_admin_password}"
        self.website_admin_username = f"{website.website_admin_username}"
        self.code_host = f"{code_host}"
        self.code_port = f"{code_port}"
        self.code_username = f"{code_username}"
        self.code_email = f"{code_username}@{code_host}"
        self.code_password = generate_password()
        self.proxy_domain = f"{proxy_domain}"
        self.proxy_port = f"{proxy_port}"

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the code server
        """
        return f"""
    code:
        image: codercom/code-server
        container_name: code
        environment:
            PASSWORD: {self.code_password}
            SUDO_PASSWORD: {self.code_password}
            TZ: Europe/Brussels
            PROXY_DOMAIN: {self.proxy_domain}
            PROXY_PORT: {self.proxy_port}
        volumes:
            - vscode-data:/home/coder/project
        networks:
            - proxy-network
        depends_on:
            - website
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.vscode.rule=Host(`vscode.{self.website_hostname}`)"
            - "traefik.http.routers.vscode.service=vscode"
            - "traefik.http.routers.vscode.entrypoints=websecure"
            - "traefik.http.services.vscode.loadbalancer.server.port=8080"
            - "traefik.http.routers.vscode.tls=true"
            - "traefik.http.routers.vscode.tls.certresolver=letsencrypt"
            - "traefik.http.services.vscode.loadbalancer.passhostheader=true"
        restart: unless-stopped
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"
        """

    def to_kubernetes(self):
        """
        This function returns the kubernetes data for the code server
        """
        return f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: code
          labels:
            app: code
        spec:
            ports:
            - port: 8080
                targetPort: 8080
            selector:
                app: code
            type: ClusterIP
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
            name: code
            labels:
                app: code
        spec:
            selector:
                matchLabels:
                    app: code
            template:
                metadata:
                    labels:
                        app: code
                spec:
                    containers:
                    - name: code
                        image: codercom/code-server
                        ports:
                        - containerPort: 8080
                        env:
                        - name: PASSWORD
                            value: {self.code_password}
                        - name: SUDO_PASSWORD
                            value: {self.code_password}
                        - name: TZ
                            value: Europe/Brussels
                        - name: PROXY_DOMAIN
                            value: {self.proxy_domain}
                        - name: PROXY_PORT
                            value: {self.proxy_port}
        """

    def to_vagrant_vm(self):
        """
        Converts the current object to a Vagrant virtual machine configuration.

        Returns:
            str: Vagrant virtual machine configuration as a multi-line string.
        """
        return """
        config.vm.define "code" do |code|
            code.vm.box = "ubuntu/focal64"
            code.vm.hostname = "code"
            code.vm.network "private_network", ip: "
            code.vm.provider "virtualbox" do |vb|
                vb.memory = "1024"
                vb.cpus = "1"
            end
            code.vm.provision "shell", inline: <<-SHELL
                sudo apt-get update
                sudo apt-get install -y apache2-utils
                sudo apt-get install -y apt-transport-https
                sudo apt-get install -y ca-certificates
                sudo apt-get install -y curl
                sudo apt-get install -y gnupg
                sudo apt-get install -y lsb-release
                sudo apt-get install -y wget
                sudo apt-get install -y redis-server
                sudo apt-get install -y mariadb-client
                sudo apt-get install -y unzip
                sudo apt-get install -y docker.io
                sudo apt-get install -y docker-compose
                sudo apt-get install -y apache2
                sudo apt-get install -y php
                sudo apt-get install -y php-mysql
                sudo apt-get install -y php-curl
                sudo apt-get install -y php-gd
                sudo apt-get install -y php-intl
                sudo apt-get install -y php-mbstring
                sudo apt-get install -y php-soap
                sudo apt-get install -y php-xml
                sudo apt-get install -y php-xmlrpc
                sudo apt-get install -y php-zip
                sudo systemctl enable docker
                sudo systemctl start docker
                sudo systemctl enable apache2
                sudo systemctl start apache2
                sudo wget
            SHELL
        end
        """


class Application:
    """
    Represents an application associated with a website.

    Attributes:
        website (Website): The website object associated with the application.
        version (str): The version of the application (default is "1.0").
    """

    def __init__(self, website: Website, version: str = "1.0"):
        """
        Initializes a new instance of the Application class.

        Args:
            website (Website): The website object associated with the application.
            version (str, optional): The version of the application (default is "1.0").
        """
        self.project_name = website.website_hostname
        self.app_name = website.website_hostname
        # reverse the host name. for example if the host url is "h2oheating.xyz" then the bundle will be "xyz.h2oheating"
        self.bundle = ".".join(website.website_hostname.split(".")[::-1])
        self.version = version
        self.url = website.website_hostname
        self.license = "MIT license"
        self.author = website.website_admin_username
        self.author_email = website.website_admin_email
        self.formal_name = website.website_hostname
        self.description = website.website_description
        self.long_description = website.website_description

    def to_docker_compose(self):
        """
        Converts the Application object to a docker-compose.yml data string.

        Returns:
            str: The docker-compose.yml data string representing the Application object.
        """

        return """
    application:
        image: woopy-app:latest
        container_name: application
        command: >
            /bin/bash -c "/app/entrypoint.sh"
        networks:
            - website-network
        depends_on:
            - website
        labels:
            - "traefik.enable=false"
        restart: unless-stopped
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"
        """

    def to_kubernetes(self):
        """
        Converts the Application object to a Kubernetes data string.

        Returns:
            str: The Kubernetes data string representing the Application object.
        """
        return """
        apiVersion: v1
        kind: Service
        metadata:
          name: application
          labels:
            app: application
        spec:
            ports:
            - port: 80
                targetPort: 80
            selector:
                app: application
            type: ClusterIP
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
            name: application
            labels:
                app: application
        spec:
            selector:
                matchLabels:
                    app: application
            template:
                metadata:
                    labels:
                        app: application
                spec:
                    containers:
                    - name: application
                        image: alpine:latest
                        command:
                        - /bin/sh
                        - -c
                        - |
                        -   # Install vim, nano, and git
                        -   apk add vim
                        -   apk add nano
                        -   apk add git
                        -   # Install JDK17, Ant, Maven, Gradle, and Python
                        -   apk add openjdk17
                        -   apk add ant
                        -   apk add maven
                        -   apk add gradle
                        -   apk add python3
                        -   apk add py3-pip
                        -   apk add py3-virtualenv
                        -   apk add py3-wheel
                        -   apk add py3-setuptools
                        -   apk add py3-cffi
                        -   apk add py3-cryptography
                        -   apk add py3-openssl
                        -   apk add py3-pycparser
                        -   apk add py3-idna
                        -   apk add py3-requests
                        -   apk add py3-urllib3
                        -   apk add py3-chardet
                        -   apk add py3-certifi
                        -   # Install Android Studio
                        -   apk add android-studio
                        -   apk add android-sdk
                        -   apk add android-sdk-platform-tools
                        -   # Install Briefcase and Toga
                        -   pip install briefcase toga
                        -   briefcase new -Q "project_name={self.project_name}" -Q "app_name={self.app_name}" -Q "bundle={self.bundle}" -Q "version={self.version}" -Q "url={self.url}" -Q "license={self.license}" -Q "author={self.author}" -Q "author_email={self.author_email}" -Q "formal_name={self.formal_name}" -Q "description={self.description}" -Q "long_description={self.long_description}" --no-input
                        -   pushd {self.project_name} || exit
                        -   app_py_path="src/{self.app_name}/app.py"
                        -   if [ -f $app_py_path ]; then
                        -       rm -rf $app_py_path
                        -   fi
                        -   echo "Updating app.py code to include webview..."
                        -   echo "import toga" > $app_py_path
                        -   echo "from toga.style import Pack" >> $app_py_path
                        -   echo -e "\n" >> $app_py_path
                        -   echo -e "\n" >> $app_py_path
                        -   echo "class {self.app_name}(toga.App):" >> $app_py_path
                        -   echo -e "\n" >> $app_py_path
                        -   echo "    def startup(self):" >> $app_py_path
                        -   echo "        self.main_window = toga.MainWindow()" >> $app_py_path
                        -   echo "        load_webview(self.main_window, "{self.url}")" >> $app_py_path
                        -   echo "        self.main_window.show()" >> $app_py_path
                        -   echo -e "\n" >> $app_py_path
                        -   echo "def load_webview(widget, url):" >> $app_py_path
                        -   echo "    webview = toga.WebView(style=Pack(flex=1))" >> $app_py_path
                        -   echo "    webview.url = url" >> $app_py_path
                        -   echo "    widget.content = webview" >> $app_py_path
                        -   echo -e "\n" >> $app_py_path
                        -   echo "def main():" >> $app_py_path
                        -   echo "    return {self.app_name}()" >> $app_py_path
                        -   echo -e "\n" >> $app_py_path
                        -   echo -e "\n" >> $app_py_path
                        -   echo "if __name__ == '__main__':" >> $app_py_path
                        -   echo "    main().main_loop()" >> $app_py_path
                        -   echo -e "\n" >> $app_py_path
                        -   echo "Updating app.py code to include webview...done"
                        -   echo "Building the application..."
                        -   briefcase package linux
                        -   briefcase package android
                        -   echo "Building the application...done"
                        -   popd || exit
                    ports:
                    - containerPort: 80
                    volumeMounts:
                    - mountPath: /var/run/docker.sock
                        name: docker-socket
                    - mountPath: /data
                        name: data
                    env:
                    - name: TZ
                        value: Europe/Brussels
                    
                    volumes:
                    - name: docker-socket
                        hostPath:
                        path: /var/run/docker.sock
                    - name: data
                        hostPath:
                        path: /data
                        
        """

    def to_vagrant_vm(self):
        """
        Converts the Application object to a Vagrant virtual machine configuration.

        Returns:
            str: Vagrant virtual machine configuration as a multi-line string.
        """
        return """
        config.vm.define "application" do |application|
            application.vm.box = "ubuntu/focal64"
            application.vm.hostname = "application"
            application.vm.network "private_network", ip: "
            application.vm.provider "virtualbox" do |vb|
                vb.memory = "1024"
                vb.cpus = "1"
            end
            application.vm.provision "shell", inline: <<-SHELL
                sudo apt-get update
                sudo apt-get install -y apache2-utils
                sudo apt-get install -y apt-transport-https
                sudo apt-get install -y ca-certificates
                sudo apt-get install -y curl
                sudo apt-get install -y gnupg
                sudo apt-get install -y lsb-release
                sudo apt-get install -y wget
                sudo apt-get install -y redis-server
                sudo apt-get install -y mariadb-client
                sudo apt-get install -y unzip
                sudo apt-get install -y docker.io
                sudo apt-get install -y docker-compose
                sudo apt-get install -y apache2
                sudo apt-get install -y php
                sudo apt-get install -y php-mysql
                sudo apt-get install -y php-curl
                sudo apt-get install -y php-gd
                sudo apt-get install -y php-intl
                sudo apt-get install -y php-mbstring
                sudo apt-get install -y php-soap
                sudo apt-get install -y php-xml
                sudo apt-get install -y php-xmlrpc
                sudo apt-get install -y php-zip
                sudo systemctl enable docker
                sudo systemctl start docker
                sudo systemctl enable apache2
                sudo systemctl start apache2
                sudo wget
                
                
            SHELL
        end
        """


class Project:
    """
    Represents a project with multiple services.
    """

    def __init__(self,
                 project_base_dir: str = None,
                 project_name: str = os.path.basename(os.getcwd()),
                 project_description: str = "Project description",
                 project_author: str = os.getenv("USER"),
                 project_email: str = "Project email",
                 website: Website = None,
                 database: Database = None,
                 cache: Cache = None,
                 admin: Admin = None,
                 proxy: Proxy = None,
                 monitoring: Monitoring = None,
                 management: Management = None,
                 vault: Vault = None,
                 code: Code = None,
                 application: Application = None,
                 networks: Networks = None,
                 volumes: Volumes = None
                 ):
        """
        Initializes a new instance of the Project class.
        """
        if project_base_dir is None:
            project_base_dir = os.path.join(os.getcwd(), project_name)
        self.project_base_dir = project_base_dir
        self.project_name = project_name
        self.project_description = project_description
        self.project_author = project_author
        self.project_email = project_email
        self.database = database
        self.website = website
        self.admin = admin
        self.proxy = proxy
        self.cache = cache
        self.monitoring = monitoring
        self.management = management
        self.networks = networks
        self.volumes = volumes
        self.vault = vault
        self.code = code
        self.application = application

    def get_docker_compose_data(self):
        """
        Converts the Project object to a docker-compose.yml data string.
        """
        docker_compose_yaml = f"""
version: "3.9"

services:
    {self.database.to_docker_compose()}
    {self.website.to_docker_compose()}
    {self.admin.to_docker_compose()}
    {self.proxy.to_docker_compose()}
    {self.cache.to_docker_compose()}
    {self.monitoring.to_docker_compose()}
    {self.management.to_docker_compose()}
    {self.vault.to_docker_compose()}
    {self.code.to_docker_compose()}
    {self.application.to_docker_compose()}
{self.networks.to_docker_compose()}
{self.volumes.to_docker_compose()}
"""

        return docker_compose_yaml

    def get_project_report(self):
        """
        Generates a report for the project.
        """
        report = f"""
Project: {self.project_name}
Description: {self.project_description}
Author: {self.project_author}
Email: {self.project_email}
-------------------------------------------------------------
Database Hostname: {self.database.database_host}
Database Port: {self.database.database_port}
Database Username: {self.database.database_user}
Database Password: {self.database.database_password}
-------------------------------------------------------------
Website Hostname: {self.website.website_hostname}
Website Email: {self.website.website_admin_email}
Website Username: {self.website.website_admin_username}
Website Password: {self.website.website_admin_password}
-------------------------------------------------------------
Proxy Hostname: {self.proxy.proxy_host}
Proxy Port: {self.proxy.proxy_port}
Proxy Email: {self.proxy.proxy_email}
Proxy Username: {self.proxy.proxy_username}
Proxy Password: {self.proxy.proxy_password}
-------------------------------------------------------------
Cache Hostname: {self.cache.cache_host}
Cache Port: {self.cache.cache_port}
-------------------------------------------------------------
Monitoring Hostname: {self.monitoring.monitoring_host}
Monitoring Port: {self.monitoring.monitoring_port}
Monitoring Username: {self.monitoring.monitoring_username}
Monitoring Password: {self.monitoring.monitoring_password}
-------------------------------------------------------------
Management Hostname: {self.management.management_host}
Management Port: {self.management.management_port}
Management Username: {self.management.management_username}
Management Password: {self.management.management_password}
-------------------------------------------------------------
Vault Hostname: {self.vault.vault_host}
Vault Port: {self.vault.vault_port}
Vault Username: {self.vault.vault_username}
Vault Password: {self.vault.vault_password}
-------------------------------------------------------------
Code Hostname: {self.code.code_host}
Code Port: {self.code.code_port}
Code Username: {self.code.code_username}
Code Password: {self.code.code_password}
-------------------------------------------------------------
Application Name: {self.application.app_name}
Application Version: {self.application.version}
Application URL: {self.application.url}
Application License: {self.application.license}
Application Author: {self.application.author}
Application Author Email: {self.application.author_email}
Application Formal Name: {self.application.formal_name}
Application Description: {self.application.description}
Application Long Description: {self.application.long_description}'
-------------------------------------------------------------

Networks:
{self.networks.to_docker_compose()}
-------------------------------------------------------------
Volumes:
{self.volumes.to_docker_compose()}
-------------------------------------------------------------
        """

        return report

    def get_kubernetes_data(self):
        """
        Converts the Project object to a Kubernetes data string.
        """
        kubernetes_yaml = f"""
apiVersion: v1
kind: Namespace
metadata:
  name: {self.project_name}
---
{self.database.to_kubernetes()}
---
{self.website.to_kubernetes()}
---
{self.admin.to_kubernetes()}
---
{self.proxy.to_kubernetes()}
---
{self.cache.to_kubernetes()}
---
{self.monitoring.to_kubernetes()}
---
{self.management.to_kubernetes()}
---
{self.vault.to_kubernetes()}
---
{self.code.to_kubernetes()}
"""

        return kubernetes_yaml


class Health(Resource):
    def get(self):
        return jsonify({
            'status': 'ok',
            'message': 'server is running',
            'version': '1.0.0'
        })


api.add_resource(Health, '/health')


class DockerCompose(Resource):
    """
    Class to generate a docker-compose.yml file
    Args:
        Resource (_type_): _description_
    """
    def post(self):
        """
        Get the docker-compose.yml file
        ---
        tags:
          - Docker Compose
        responses:
            200:
                description: docker-compose.yml file
                content:
                application/json:
                    schema:
                    type: object
                    properties:
                        status:
                        type: string
                        example: ok
                        message:
                        type: string
                        example: docker-compose.yml file created
                        version:
                        type: string
                        example: 1.0.0
                        file:
                        type: string
                        example: docker-compose.yml file
        """
        # create a dictionary from the .env file
        env = {}
        env_data = request.data.decode().split('\n')
        for line in env_data:
            if line:
                key, value = line.split('=')
                env[key] = value

        database = Database(database_name=env['DATABASE_NAME'], database_user=env['DATABASE_USER'],
                            database_host=env['DATABASE_HOST'])
        email = Mail(env['MAIL_SMTP_HOST'], env['MAIL_SMTP_USER'])
        cache = Cache(env['CACHE_HOST'], env['CACHE_PORT'])
        website = Website(title=env['WEBSITE_TITLE'], description=env['WEBSITE_DESCRIPTION'],
                          host=env['WEBSITE_HOSTNAME'], user=env['WEBSITE_ADMIN_USERNAME'],
                          email=env['WEBSITE_ADMIN_EMAIL'], database=database, mail=email, cache=cache)
        admin = Admin(database, website)
        proxy = Proxy(env['PROXY_TITLE'], env['PROXY_HOSTNAME'], website)
        monitoring = Monitoring(env['HOST_HOSTNAME'], env['HOST_IP'], env['HOST_MAC'], env['HOST_CPU'], env['HOST_RAM'],
                                env['HOST_OS'], env['HOST_KERNEL'], env['HOST_DOCKER'])
        management = Management(website)
        vault = Vault(website)
        code = Code(website)
        
        application = Application(website, version="1.0")

        networks = Networks()
        volumes = Volumes()

        project = Project(
            project_base_dir=os.path.join(os.getcwd(), website.website_title),
            project_name=website.website_title,
            project_description=f"WooCommerce project for {website.website_description}",
            project_author=website.website_admin_username,
            project_email=website.website_admin_email,
            website=website,
            database=database,
            cache=cache,
            admin=admin,
            proxy=proxy,
            monitoring=monitoring,
            management=management,
            vault=vault,
            code=code,
            application=application,
            networks=networks,
            volumes=volumes
        )

        # Create docker-compose.yaml file in current working directory / website_title / docker-compose.yml
        project_docker_compose_file = os.path.join(project.project_base_dir, 'docker-compose.yml')
        if not os.path.exists(project.project_base_dir):
            os.makedirs(project.project_base_dir)
        with open(project_docker_compose_file, 'w', encoding='utf-8') as f:
            docker_compose_data = project.get_docker_compose_data()
            f.write(docker_compose_data)
            logging.info(
                '################################################################################################')
            logging.info(
                f'Generated docker-compose.yml file for {website.website_title} in {project_docker_compose_file}')
            logging.info(
                '################################################################################################')

            # generate project-report.txt file
            project_report_file = os.path.join(project.project_base_dir, 'project-report.txt')
            with open(project_report_file, 'w', encoding='utf-8') as f:
                project_report_data = project.get_project_report()
                f.write(project_report_data)
                logging.info(
                    '################################################################################################')
                logging.info(
                    f'Generated project-report.txt file for {website.website_title} in {project_report_file}')
                logging.info(
                    '################################################################################################')

        try:
            return send_file(project_docker_compose_file, mimetype='text/yaml', as_attachment=True)
        except Exception as e:
            return str(e)


api.add_resource(DockerCompose, '/docker-compose')


# Create a class that has an endpoint to get the project report.
# website_title is a parameter in the endpoint
# The project report is a text file that contains the following information:

class ProjectReport(Resource):
    # require website_title as a parameter
    @app.route('/project-report/<website_title>')
    def get(self, website_title):
        """
        Get the project report
        ---
        tags:
          - Project Report
        parameters:
            - name: website_title
                in: path
                description: Website title
                required: true
                schema:
                type: string
        responses:
            200:
                description: project report
                content:
                application/json:
                    schema:
                    type: object
                    properties:
                        status:
                        type: string
                        example: ok
                        message:
                        type: string
                        example: project report created
                        version:
                        type: string
                        example: 1.0.0
                        file:
                        type: string
                        example: project report
        """
        # Create project report file in current working directory / website_title / project-report.txt
        # Get project report file from request as website_title / project-report.txt

        project_base_dir = os.path.join(os.getcwd(), website_title)
        project_report_file = os.path.join(project_base_dir, 'project-report.txt')
        with open(project_report_file, 'r', encoding='utf-8') as f:
            project_report_data = f.read()
            logging.info(
                '################################################################################################')
            logging.info(f'Getting project report for {website_title} from {project_report_file}')
            logging.info(
                '################################################################################################')

        try:
            return jsonify(
                status='ok',
                message='project report generated',
                version='1.0.0',
                file=project_report_data
            )
        except Exception as e:
            return str(e)


# Configure Swagger UI
SWAGGER_URL = '/api'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Docker Compose Generator"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger.json')
def swagger():
    return f"""
{{
    "openapi": "3.0.0",
    "info": {{
        "title": "Docker Compose Generator",
        "description": "Generate a docker-compose.yml file",
        "version": "1.0.0"
    }},
    "servers": [
        {{
            "url": "http://localhost:5000",
            "description": "Local server"
        }}
    ],
    "tags": [
        {{
            "name": "Docker Compose",
            "description": "Generate a docker-compose.yml file"
        }}
    ],
    "paths": {{
        "/health": {{
            "get": {{
                "tags": [
                    "Health"
                ],
                "summary": "Get the server health",
                "description": "Get the server health",
                "operationId": "getHealth",
                "responses": {{
                    "200": {{
                        "description": "server is running",
                        "content": {{
                            "application/json": {{
                                "schema": {{
                                    "type": "object",
                                    "properties": {{
                                        "status": {{
                                            "type": "string",
                                            "example": "ok"
                                        }},
                                        "message": {{
                                            "type": "string",
                                            "example": "server is running"
                                        }},
                                        "version": {{
                                            "type": "string",
                                            "example": "1.0.0"
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }},
        "/docker-compose": {{
            "post": {{
                "tags": [
                    "Docker Compose"
                ],
                "summary": "Get the docker-compose.yml file",
                "description": "Get the docker-compose.yml file",
                "operationId": "postDockerCompose",
                "requestBody": {{
                    "description": "Environment variables",
                    "content": {{
                        "text/plain": {{
                            "schema": {{
                                "type": "string"
                            }}
                        }}
                    }}
                }},
                "responses": {{
                    "200": {{
                        "description": "docker-compose.yml file",
                        "content": {{
                            "application/json": {{
                                "schema": {{
                                    "type": "object",
                                    "properties": {{
                                        "status": {{
                                            "type": "string",
                                            "example": "ok"
                                        }},
                                        "message": {{
                                            "type": "string",
                                            "example": "docker-compose.yml file created"
                                        }},
                                        "version": {{
                                            "type": "string",
                                            "example": "1.0.0"
                                        }},
                                        "file": {{
                                            "type": "string",
                                            "example": "docker-compose.yml file"
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }},
        "/project-report": {{
            "get": {{
                "tags": [
                    "Project Report"
                ],
                "summary": "Get the project report",
                "description": "Get the project report",
                "operationId": "getProjectReport",
                "parameters": [
                    {{
                        "name": "website_title",
                        "in": "path",
                        "description": "Website title",
                        "required": true,
                        "schema": {{
                            "type": "string"
                        }}
                    }}
                ],
                "responses": {{
                    "200": {{
                        "description": "project report",
                        "content": {{
                            "application/json": {{
                                "schema": {{
                                    "type": "object",
                                    "properties": {{
                                        "status": {{
                                            "type": "string",
                                            "example": "ok"
                                        }},
                                        "message": {{
                                            "type": "string",
                                            "example": "project report created"
                                        }},
                                        "version": {{
                                            "type": "string",
                                            "example": "1.0.0"
                                        }},
                                        "file": {{
                                            "type": "string",
                                            "example": "project report"
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}

"""
