import logging
import os
import secrets
import tempfile
from datetime import datetime


from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from zipfile import ZipFile, ZIP_DEFLATED

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

def generate_username() -> str:
    """
    Generate a random username
    """
    # Generate a random token
    token = secrets.token_urlsafe(8)
    return token


def generate_service(site_title: str) -> str:
    """
    Generate a random database name
    """
    # Generate a random token and append it to the site title
    token = secrets.token_urlsafe(8)
    return f"{site_title}-{token}"

def get_port(service: str) -> int:
    """
    Get the default port number for a service: 
        Options:
            WordPress: 80
            MySQL: 3306
            Redis: 6379
            Mailhog: 8025

    """
    if service == "WordPress":
        return 80
    elif service == "Shopify":
        return 80
    elif service == "Joomla":
        return 80
    elif service == "MySQL":
        return 3306
    elif service == "Redis":
        return 6379
    elif service == "Mailhog":
        return 8025
    elif service == "Traefik":
        return 8080
    elif service == "Prometheus":
        return 9090
    elif service == "Grafana":
        return 3000
    elif service == "Alertmanager":
        return 9093
    elif service == "cAdvisor":
        return 8080
    elif service == "Code-server":
        return 8080
    elif service == "Jenkins":
        return 8080
    elif service == "GitLab":
        return 80
    elif service == "SonarQube":
        return 9000
    elif service == "Portainer":
        return 9000
    elif service == "Kibana":
        return 5601
    elif service == "Elasticsearch":
        return 9200
    elif service == "Logstash":
        return 9600
    elif service == "Vault":
        return 8200
    elif service == "Consul":
        return 8500
    elif service == "Nomad":
        return 4646
    elif service == "Packer":
        return 8080
    elif service == "Terraform":
        return 8080
    elif service == "Ansible":
        return 80
    elif service == "Nginx":
        return 80
    elif service == "Apache":
        return 80
    elif service == "HAProxy":
        return 80
    elif service == "Varnish":
        return 80
    elif service == "Squid":
        return 80
    elif service == "Postfix":
        return 25
    elif service == "Dovecot":
        return 143
    elif service == "OpenLDAP":
        return 389
    elif service == "FreeIPA":
        return 80
    elif service == "Keycloak":
        return 8080
    elif service == "Gitea":
        return 80
    else:
        return 80
    

def generate_email(website_host: str, service_name: str) -> str:
    """
    Generate a random email
    """
    # Generate a random token and append it to the website host
    token = secrets.token_urlsafe(8)
    return f"{service_name}-{token}@{website_host}"


def is_local_setup() -> bool:
    """
    Check if the setup is local
    """
    # Check if the hostname is localhost
    import socket
    return socket.gethostname() == "localhost"


def get_logging() -> str:
    """
    Get the logging configuration
    """
    if is_local_setup():
        return """
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "5"
        """
    else:
        return """
            driver: "syslog"
            options:
                tag: "{{.Name}}"
        """


class Database:
    """
    Database class: This class is used to create a database for the website
    """

    def __init__(self, site_title):
        self.database_name = generate_service(site_title)
        self.database_user = generate_username()
        self.database_password = generate_password()
        self.database_root_password = generate_password()
        self.database_host = f"{site_title}-database"
        self.database_port = get_port("MySQL")
        self.database_character_set = "utf8mb4"
        self.database_table_prefix = "woopy_"

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
            {get_logging()}
        """



class Cache:
    """
    Cache class: This class is used to create a cache for the website
    """

    def __init__(self, site_title: str):
        self.cache_host = f"{site_title}-cache"
        self.cache_port = get_port("Redis")
        self.cache_username = generate_username()
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
            {get_logging()}
        """


class Mail:
    """
    Mail class: This class is used to create a mail server for the website
    """

    def __init__(self, site_title: str, site_url: str):
        self.mail_host = f"{site_title}-mail"
        self.mail_base_url = f"{site_url}"
        self.mail_username = generate_username()
        self.mail_password = generate_password()
        self.mail_port = get_port("Mailhog")
        self.mail_encryption = "TLS"
        self.mail_protocol = "smtp"

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the mail server
        """
        return f"""
    mail:
        image: mailhog/mailhog
        container_name: mail
        environment:
            - MH_UI_BIND_ADDR={self.mail_host}:8025
            - MH_SMTP_BIND_ADDR={self.mail_host}:1025
            - MH_API_BIND_ADDR={self.mail_host}:8025
            - MH_UI_WEB_PATH=/
        ports:
            - "8025:8025"
            - "1025:{self.mail_port}"
            - "587:587"
            - "465:465"
        networks:
            - proxy-network
        depends_on:
            - website
        labels:
            - "traefik.enable=false"
        restart: unless-stopped
        logging:
            {get_logging()}
        """

    

class Website:
    """
    Website class: This class is used to create a website for the user
    """

    def __init__(self, site_title: str, site_url: str, database_props: Database, mail_props: Mail, cache_props: Cache):
        self.database_host = f"{database_props.database_host}"
        self.database_port = f"{database_props.database_port}"
        self.database_name = f"{database_props.database_name}"
        self.database_user = f"{database_props.database_user}"
        self.database_password = f"{database_props.database_password}"
        self.database_table_prefix = f"{database_props.database_table_prefix}"
        self.website_host = f"{site_url}-website"
        self.website_title = f"{site_title}"
        self.website_url = f"{site_url}"
        self.website_description = f"Add description here for {site_title}: {datetime.now()}"
        self.website_admin_username = generate_username()
        # generate a hashed password with SHA-256 and base64 encoding
        self.website_admin_password = generate_password()
        self.website_admin_email = generate_email(self.website_host, "website")
        self.mail_smtp_host = f"{mail_props.mail_host}"
        self.mail_smtp_port = f"{mail_props.mail_port}"
        self.mail_smtp_user = f"{mail_props.mail_username}"
        self.mail_smtp_password = f"{mail_props.mail_password}"
        self.mail_smtp_protocol = f"{mail_props.mail_encryption}"
        self.cache_host = f"{cache_props.cache_host}"
        self.cache_port = f"{cache_props.cache_port}"
        self.cache_password = f"{cache_props.cache_password}"

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
            WORDPRESS_SITE_URL: {self.website_url}
        networks:
            - website-network
            - proxy-network
        depends_on:
            - database
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.wordpress.rule=Host(`{self.website_host}`)"
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
            {get_logging()}
        """


class Admin:
    """
    Admin class: This class is used to create an admin panel for the website
    """

    def __init__(self, site_title: str, database_props: Database):
        self.admin_host = f"{site_title}-admin"
        self.database_host = f"{database_props.database_host}"
        self.database_port = f"{database_props.database_port}"
        self.database_user = f"{database_props.database_user}"
        self.database_password = f"{database_props.database_password}"
        self.admin_username = generate_username()
        self.admin_password = generate_password()

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the admin panel
        """
        return f"""
    admin:
        image: phpmyadmin:latest
        container_name: {self.admin_host}
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
            - "traefik.http.routers.phpmyadmin.rule=Host(`phpmyadmin.{self.admin_host}`)"
            - "traefik.http.routers.phpmyadmin.service=phpmyadmin"
            - "traefik.http.routers.phpmyadmin.entrypoints=websecure"
            - "traefik.http.services.phpmyadmin.loadbalancer.server.port=80"
            - "traefik.http.routers.dashboard.middlewares=authtraefik"
            - "traefik.http.middlewares.authtraefik.basicauth.users={self.admin_username}:{self.admin_password}"
            - "traefik.http.routers.phpmyadmin.tls=true"
            - "traefik.http.routers.phpmyadmin.tls.certresolver=letsencrypt"
            - "traefik.http.services.phpmyadmin.loadbalancer.passhostheader=true"
            - "traefik.docker.network=proxy-network"
        restart: unless-stopped
        logging:
            {get_logging()}
        """

    

class Proxy:
    """
    Proxy class: This class is used to create a proxy for the website
    """

    def __init__(self, site_title: str):
        self.proxy_username = generate_username()
        self.proxy_password = generate_password()
        self.proxy_title = f"{site_title}-proxy"
        self.proxy_host = self.proxy_title
        self.proxy_port = get_port("Traefik")
        self.proxy_username = generate_username()
        self.proxy_email = generate_email(self.proxy_host, "proxy")
        self.proxy_password = generate_password()

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the proxy
        """
        return f"""
    proxy:
        image: traefik:2.9
        container_name: {self.proxy_host}
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
            - "--certificatesresolvers.letsencrypt.acme.email={self.proxy_email}"
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
            - "traefik.http.routers.dashboard.rule=Host(`traefik.{self.proxy_host}`)"
            - "traefik.http.routers.dashboard.service=api@internal"
            - "traefik.http.routers.dashboard.entrypoints=websecure"
            - "traefik.http.services.dashboard.loadbalancer.server.port=8080"
            - "traefik.http.routers.dashboard.tls=true"
            - "traefik.http.routers.dashboard.tls.certresolver=letsencrypt"
            - "traefik.http.services.dashboard.loadbalancer.passhostheader=true"
#      - "traefik.http.routers.dashboard.middlewares=authtraefik"
#      - "traefik.http.middlewares.authtraefik.basicauth.users={self.proxy_username}:{self.proxy_password}"
            - "traefik.http.routers.http-catchall.rule=HostRegexp(`{{host:.+}}`)"
            - "traefik.http.routers.http-catchall.entrypoints=web"
            - "traefik.http.routers.http-catchall.middlewares=redirect-to-https"
            - "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https"
        restart: unless-stopped
        logging:
            {get_logging()}
        """

   

class Monitoring:
    """
    Monitoring class: This class is used to create a monitoring system for the host
    """

    def __init__(self, site_title: str):
        self.monitoring_host = f"{site_title}-monitoring"
        self.monitoring_port = get_port("Cadvisor")
        self.monitoring_username = generate_username()
        self.montiroing_email = generate_email(self.monitoring_host, "monitoring")
        self.monitoring_password = generate_password()

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the monitoring system
        """
        return f"""
    monitoring:
        image: gcr.io/cadvisor/cadvisor:v0.39.0
        container_name: {self.monitoring_host}
        privileged: true
        volumes:
            - /var/run:/var/run:ro
            - /sys:/sys:ro
            - /var/lib/docker/:/var/lib/docker:ro
            - /var/run/docker.sock:/var/run/docker.sock:ro
            - /etc/machine-id:/etc/machine-id:ro
            - /var/lib/dbus/machine-id:/var/lib/dbus/machine-id:ro
        environment:
            - TZ=Europe/Brussels
        networks:
            - proxy-network
            - website-network
        depends_on:
            - website
            - database
            - cache
            - proxy
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.phpmyadmin.rule=Host(`phpmyadmin.{self.monitoring_host}`)"
            - "traefik.http.routers.phpmyadmin.service=phpmyadmin"
            - "traefik.http.routers.phpmyadmin.entrypoints=websecure"
            - "traefik.http.services.phpmyadmin.loadbalancer.server.port=80"
            - "traefik.http.routers.dashboard.middlewares=authtraefik"
            - "traefik.http.middlewares.authtraefik.basicauth.users={self.monitoring_username}:{self.monitoring_password}"
            - "traefik.http.routers.phpmyadmin.tls=true"
            - "traefik.http.routers.phpmyadmin.tls.certresolver=letsencrypt"
            - "traefik.http.services.phpmyadmin.loadbalancer.passhostheader=true"
            - "traefik.docker.network=proxy-network"
        restart: unless-stopped
        logging:
            {get_logging()}
        """



class Management:
    """
    Management class: This class is used to create a management system for the website
    """

    def __init__(self, site_title: str):
        self.management_host = f"{site_title}-management"
        self.management_port = get_port("Portainer")
        self.management_username = generate_username()
        self.management_email = generate_email(self.management_host, "management")
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
            --admin-password '{self.management_password}'
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
            - "traefik.http.routers.phpmyadmin.rule=Host(`phpmyadmin.{self.management_host}`)"
            - "traefik.http.routers.phpmyadmin.service=phpmyadmin"
            - "traefik.http.routers.phpmyadmin.entrypoints=websecure"
            - "traefik.http.services.phpmyadmin.loadbalancer.server.port=80"
            - "traefik.http.routers.dashboard.middlewares=authtraefik"
            - "traefik.http.middlewares.authtraefik.basicauth.users={self.management_username}:{self.management_password}"
            - "traefik.http.routers.phpmyadmin.tls=true"
            - "traefik.http.routers.phpmyadmin.tls.certresolver=letsencrypt"
            - "traefik.http.services.phpmyadmin.loadbalancer.passhostheader=true"
            - "traefik.docker.network=proxy-network"
        restart: unless-stopped
        logging:
            {get_logging()}
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

    def __init__(self, site_title: str):
        self.vault_host = f"{site_title}-vault"
        self.vault_port = get_port("Vault")
        self.vault_username = generate_username()
        self.vault_email = generate_email(self.vault_host, "vault")
        self.vault_password = generate_password()

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the vault
        """
        return f"""
    vault:
        image: alpine:latest
        container_name: {self.vault_host}
        command: >
            /bin/sh -c "echo Vault username (encrypted):" && echo -n '{self.vault_username}' | sha256sum &&
            /bin/sh -c "echo Vault password (encrypted):" && echo -n '{self.vault_password}' | sha256sum
            /bin/sh -c "while true; do sleep 300; done;"
        networks:
            - proxy-network
        depends_on:
            - website
        labels:
            - "traefik.enable=false"
        restart: unless-stopped
        logging:
            {get_logging()}
        """



class Code:
    """
    Code class: This class is used to create a code server for the website
    """

    def __init__(self, site_title: str, site_host: str):
        self.code_host = f"{site_title}-code"
        self.code_port = get_port("Code")
        self.code_username = generate_username()
        self.code_email = generate_email(self.code_host, "code")
        self.code_password = generate_password()
        self.proxy_domain = f"{site_host}"
        self.proxy_port = get_port("Traefik")

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
            - "traefik.http.routers.vscode.rule=Host(`vscode.{self.code_host}`)"
            - "traefik.http.routers.vscode.service=vscode"
            - "traefik.http.routers.vscode.entrypoints=websecure"
            - "traefik.http.services.vscode.loadbalancer.server.port=8080"
            - "traefik.http.routers.vscode.tls=true"
            - "traefik.http.routers.vscode.tls.certresolver=letsencrypt"
            - "traefik.http.services.vscode.loadbalancer.passhostheader=true"
        restart: unless-stopped
        logging:
            {get_logging()}
        """

    
class Application:
    """
    Represents an application associated with a website.

    Attributes:
        website (Website): The website object associated with the application.
        version (str): The version of the application (default is "1.0").
    """

    def __init__(self, site_title: str, site_url: str, version: str = "1.0"):
        """
        Initializes a new instance of the Application class.

        Args:
            website (Website): The website object associated with the application.
            version (str, optional): The version of the application (default is "1.0").
        """
        self.app_host= f"{site_title}-app"
        self.project_name = self.app_host
        self.app_name = self.app_host
        # reverse the host name. for example if the host url is "h2oheating.xyz" then the bundle will be "xyz.h2oheating"
        self.bundle = ".".join(site_url.split(".")[::-1])
        self.version = version
        self.url = site_url
        self.license = "MIT license"
        self.author = generate_username()
        self.author_email = generate_email(self.app_host, "app")
        self.formal_name = self.app_host
        self.description = f"{self.app_name} is a native application for {self.app_host}."
        self.long_description = f"{self.app_name} is designed to provide a user-friendly interface for {self.app_host}. It can be installed on Linux, macOS, Windows, Android, iOS. It is written in Python using Toga and Briefcase frameworks."

    def to_docker_compose(self):
        """
        Converts the Application object to a docker-compose.yml data string.

        Returns:
            str: The docker-compose.yml data string representing the Application object.
        """

        return f"""
    application:
        image: docker.io/yilmazchef/woopy-app:latest
        container_name: {self.app_host}
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
            {get_logging()}
        """


class ReadMe():
    """
    ReadMe class: This class is to provide ReadMe.md document for the project.
    It must explain all the services and how to use them.
    
    It must provide documentation to 3 different level of users:
    - Beginner
    - Intermediate
    - Advanced
    """
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.readme_content = f"""
# {self.project_name}

## Introduction

This project is a collection of services that can be used to create a website, database, cache, admin, proxy, monitoring, management, vault, code, and application.

## Services

### Website

This services is based on WordPress and WooCommerce. It is used to create a website for the project.

#### WordPress

WordPress is a free and open-source content management system written in PHP and paired with a MySQL or MariaDB database. Features include a plugin architecture and a template system, referred to within WordPress as Themes. For further information, please visit [WordPress](https://wordpress.org/).

#### WooCommerce

WooCommerce is an open-source e-commerce plugin for WordPress. It is designed for small to large-sized online merchants using WordPress. For further information, please visit [WooCommerce](https://woocommerce.com/).


### Database

This service is based on MySQL. It is used to store the data for the website. For further information, please visit [MySQL](https://www.mysql.com/).

### Cache

This service is based on Redis. It is used to cache the data for the website. For further information, please visit [Redis](https://redis.io/).

### Admin

This service is based on phpMyAdmin. It is used to manage the database for the website. For further information, please visit [phpMyAdmin](
    
### Proxy

This service is based on Traefik. It is used to route the traffic for the website. For further information, please visit [Traefik](https://traefik.io/).

### Monitoring

This service is based on Cadvisor. It is used to monitor the containers for the website. For further information, please visit [Cadvisor](
    
### Management

This service is based on Portainer. It is used to manage the containers for the website. For further information, please visit [Portainer](https://www.portainer.io/).

### Vault

This service is based on Vault. It is used to store the secrets for the website. For further information, please visit [Vault](https://www.vaultproject.io/).

### Code

This service is based on Code Server. It is used to write the code for the website. For further information, please visit [Code Server](https://coder.com/).

### Application

This service is based on Toga and Briefcase. It is used to create a native application for the website. For further information, please visit [Toga](https://beeware.org/project/projects/libraries/toga/) and [Briefcase](https://beeware.org/project/projects/tools/briefcase/).

## How to Use

### Beginner

To use this project, you need to have Docker and Docker Compose installed on your machine. Then, you can run the following command:
    
    ```bash
    docker-compose up -d
    ```
    
This will start all the services for the project.

### Intermediate

To use this project, you need to have Kubernetes installed on your machine. Then, you can run the following command:
    
    ```bash
    kubectl apply -f kubernetes.yml
    ```
        
This will start all the services for the project.

### Advanced

To use this project, you need to have Vagrant installed on your machine. Then, you can run the following command:

    ```bash
    vagrant up
    ```
        
This will start all the services for the project.

## Conclusion

This project is a collection of services that can be used to create a website, database, cache, admin, proxy, monitoring, management, vault, code, and application. It is designed to be easy to use for beginners, intermediate users, and advanced users.

For further information, please visit [GitHub](https://github.com/atiilla/woopy).

"""



class PreequisitesSetup():
    """
    This class generates a shell script to install the required software on the host machine.
    
    The script should install the following software:
    - Docker
    - Docker Compose
    - Kubernetes
    - Vagrant
    
    The script should be able to run on the following operating systems:
    - Ubuntu
    - CentOS
    - Fedora
    - Red Hat Enterprise Linux
    - Debian
    - openSUSE
    - SUSE Linux Enterprise Server
    - Arch Linux
    - Alpine Linux
    - FreeBSD
    - macOS
    - Rocky Linux
    - Oracle Linux
    - AlmaLinux
    
    The script must be able to detect the operating system and install the required software accordingly.
    
    """
    
    def __init__(self):
        self.prerequisites_setup_content = """
#!/bin/bash

# Check if the script is running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root"
    exit
fi

# Check the operating system
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
elif type lsb_release > /dev/null 2>&1; then
    OS=$(lsb_release -si)
else
    OS=$(uname -s)
fi

# Install Docker

if [ "$OS" == "Ubuntu" ] || [ "$OS" == "Debian" ]; then
    apt-get update
    apt-get install -y docker.io
    systemctl enable docker
    systemctl start docker
elif [ "$OS" == "CentOS Linux" ] || [ "$OS" == "Fedora" ] || [ "$OS" == "Red Hat Enterprise Linux" ]; then
    yum install -y docker
    systemctl enable docker
    systemctl start docker
elif [ "$OS" == "openSUSE Leap" ] || [ "$OS" == "SUSE Linux Enterprise Server" ]; then
    zypper install -y docker
    systemctl enable docker
    systemctl start docker
elif [ "$OS" == "Arch Linux" ]; then
    pacman -S --noconfirm docker
    systemctl enable docker
    systemctl start docker
elif [ "$OS" == "Alpine Linux" ]; then
    apk add docker
    rc-update add docker boot
    service docker start
elif [ "$OS" == "FreeBSD" ]; then
    pkg install -y docker
    sysrc docker_enable=YES
    service docker start
elif [ "$OS" == "macOS" ]; then
    brew install docker
    brew services start docker
elif [ "$OS" == "Rocky Linux" ] || [ "$OS" == "Oracle Linux" ] || [ "$OS" == "AlmaLinux" ]; then
    dnf install -y docker
    systemctl enable docker
    systemctl start docker
else
    echo "Unsupported operating system"
    exit
fi

# Install Docker Compose

if [ "$OS" == "Ubuntu" ] || [ "$OS" == "Debian" ]; then
    apt-get install -y docker-compose
elif [ "$OS" == "CentOS Linux" ] || [ "$OS" == "Fedora" ] || [ "$OS" == "Red Hat Enterprise Linux" ]; then
    yum install -y docker-compose
elif [ "$OS" == "openSUSE Leap" ] || [ "$OS" == "SUSE Linux Enterprise Server" ]; then
    zypper install -y docker-compose
elif [ "$OS" == "Arch Linux" ]; then
    pacman -S --noconfirm docker-compose
elif [ "$OS" == "Alpine Linux" ]; then
    apk add docker-compose
elif [ "$OS" == "FreeBSD" ]; then
    pkg install -y docker-compose
elif [ "$OS" == "macOS" ]; then
    brew install docker-compose
elif [ "$OS" == "Rocky Linux" ] || [ "$OS" == "Oracle Linux" ] || [ "$OS" == "AlmaLinux" ]; then
    dnf install -y docker-compose
else
    echo "Unsupported operating system"
    exit
fi

# Install Kubernetes

if [ "$OS" == "Ubuntu" ] || [ "$OS" == "Debian" ]; then
    apt-get update
    apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    apt-get update
    apt-get install -y kubectl
elif [ "$OS" == "CentOS Linux" ] || [ "$OS" == "Fedora" ] || [ "$OS" == "Red Hat Enterprise Linux" ]; then
    yum install -y kubectl
elif [ "$OS" == "openSUSE Leap" ] || [ "$OS" == "SUSE Linux Enterprise Server" ]; then
    zypper install -y kubectl
elif [ "$OS" == "Arch Linux" ]; then
    pacman -S --noconfirm kubectl
elif [ "$OS" == "Alpine Linux" ]; then
    apk add kubectl
elif [ "$OS" == "FreeBSD" ]; then
    pkg install -y kubectl
elif [ "$OS" == "macOS" ]; then
    brew install kubectl
elif [ "$OS" == "Rocky Linux" ] || [ "$OS" == "Oracle Linux" ] || [ "$OS" == "AlmaLinux" ]; then
    dnf install -y kubectl
else
    echo "Unsupported operating system"
    exit
fi

# Install Vagrant

if [ "$OS" == "Ubuntu" ] || [ "$OS" == "Debian" ]; then
    apt-get update
    apt-get install -y vagrant
elif [ "$OS" == "CentOS Linux" ] || [ "$OS" == "Fedora" ] || [ "$OS" == "Red Hat Enterprise Linux" ]; then
    yum install -y vagrant
elif [ "$OS" == "openSUSE Leap" ] || [ "$OS" == "SUSE Linux Enterprise Server" ]; then
    zypper install -y vagrant
elif [ "$OS" == "Arch Linux" ]; then
    pacman -S --noconfirm vagrant
elif [ "$OS" == "Alpine Linux" ]; then
    apk add vagrant
elif [ "$OS" == "FreeBSD" ]; then
    pkg install -y vagrant
elif [ "$OS" == "macOS" ]; then
    brew install vagrant
elif [ "$OS" == "Rocky Linux" ] || [ "$OS" == "Oracle Linux" ] || [ "$OS" == "AlmaLinux" ]; then
    dnf install -y vagrant
else
    echo "Unsupported operating system"
    exit
fi

echo "Prerequisites setup completed"

"""

    def get_script(self):
        return self.prerequisites_setup_content



class Project:
    """
    Represents a project with multiple services: website, database, cache, admin, proxy, monitoring, management, vault, code, application, networks, volumes and more.
    """

    def __init__(self, website: Website = None, database: Database = None, cache: Cache = None,
                 admin: Admin = None, proxy: Proxy = None, monitoring: Monitoring = None,
                 management: Management = None, vault: Vault = None, code: Code = None,
                 application: Application = None, networks: Networks = None, volumes: Volumes = None):
        """
        Initializes a new instance of the Project class.
        Create a temp directory in the user profile on the project name. For example: $HOME/.woopy/{project_name}
        """

        # Create a project directory in the user profile if not exists
        temp_user_dir = os.path.join(os.path.expanduser("~"), ".woopy")
        if not os.path.exists(temp_user_dir):
            os.makedirs(temp_user_dir)

        self.project_name = generate_service("project")
        self.project_base_dir = os.path.join(temp_user_dir, self.project_name)

        if not os.path.exists(self.project_base_dir):
            os.makedirs(self.project_base_dir)

        self.project_description = f"Project {self.project_name} contains multiple services such as a website, database, cache, admin, proxy, monitoring, management, vault, code, and application."
        self.project_author = "woopy"
        self.project_email = "woopy@katawoo.com"
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
Website Hostname: {self.website.website_host}
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



class Health(Resource):
    def get(self):
        return jsonify({
            'status': 'ok',
            'message': 'server is running',
            'version': '1.0.0'
        })


api.add_resource(Health, '/health')


class ProjectApi(Resource):
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
                # if there are multipe = in the line, split only the first one
                key, value = line.split('=', 1)
                env[key] = value

        site_title=env["SITE_TITLE"]
        site_url=env["SITE_URL"]

        database = Database(site_title=site_title)
        email = Mail(site_title=site_title, site_url=site_url)
        cache = Cache(site_title=site_title)
        website = Website(site_title=site_title, site_url=site_url, database_props=database, mail_props=email, cache_props=cache)
        admin = Admin(site_title=site_title, database_props=database)
        proxy = Proxy(site_title=site_title)
        monitoring = Monitoring(site_title=site_title)
        management = Management(site_title=site_title)
        vault = Vault(site_title=site_title)
        code = Code(site_title=site_title, site_host=website.website_host)
        application = Application(site_title=site_title, site_url=site_url)

        networks = Networks()
        volumes = Volumes()

        project = Project(
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
        
        readme = ReadMe(project_name=project.project_name)
        prerequisites_setup = PreequisitesSetup()
        

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
                
            
            # generate README.md file
            project_readme_file = os.path.join(project.project_base_dir, 'README.md')
            with open(project_readme_file, 'w', encoding='utf-8') as f:
                f.write(readme.readme_content)
                logging.info(
                    '################################################################################################')
                logging.info(
                    f'Generated README.md file for {website.website_title} in {project_readme_file}')
                logging.info(
                    '################################################################################################')
                
                
            # generate prerequisites-setup.sh file for the project
            prerequisites_setup_file = os.path.join(project.project_base_dir, 'prerequisites-setup.sh')
            with open(prerequisites_setup_file, 'w', encoding='utf-8') as f:
                f.write(prerequisites_setup.get_script())
                logging.info(
                    '################################################################################################')
                logging.info(
                    f'Generated prerequisites-setup.sh file for {website.website_title} in {prerequisites_setup_file}')
                logging.info(
                    '################################################################################################')
                

        project_zip_file = os.path.join(project.project_base_dir, 'project.zip')
        with ZipFile(project_zip_file, 'w', compression=ZIP_DEFLATED) as zip:
            zip.write(project_docker_compose_file, 'docker-compose.yml')
            zip.write(project_report_file, 'project-report.txt')
            zip.write(project_readme_file, 'README.md')
            zip.write(prerequisites_setup_file, 'prerequisites-setup.sh')
            logging.info(
                '################################################################################################')
            logging.info(
                f'Generated project.zip file for {website.website_title} in {project_zip_file}')
            logging.info(
                '################################################################################################')

        
        try:
            return send_file(project_zip_file, as_attachment=True)
        except Exception as e:
            return str(e)


api.add_resource(ProjectApi, '/')

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
        "title": "WooPy Project Generator",
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
            "name": "WooPy",
            "description": "Generate a docker-compose.yml, report, and README.md file as well as a script to install the required software on the host machine"
        }}
    ],
    "paths": {{
        "/": {{
            "post": {{
                "tags": [
                    "Docker Compose"
                ],
                "summary": "Get the project as a zip file",
                "description": "Get the project as a zip file",
                "operationId": "get_project",
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
                                            "example": "project.zip file created"
                                        }},
                                        "version": {{
                                            "type": "string",
                                            "example": "1.0.0"
                                        }},
                                        "file": {{
                                            "type": "string",
                                            "example": "project.zip file"
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
