import logging
import os
import secrets
import socket
import tempfile
from datetime import datetime
from zipfile import ZIP_DEFLATED, ZipFile

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
    

def generate_email(site_url: str, service_name: str) -> str:
    """
    Generate a random email
    """
    # Generate a random token and append it to the website host
    token = secrets.token_urlsafe(8)
    return f"{service_name}-{token}@{site_url}"


def get_logging() -> str:
    """
    Get the logging configuration
    """
    return """driver: "json-file"
            options:
                max-size: "10m"
                max-file: "5"
    """


class Database:
    """
    Database class: This class is used to create a database for the website
    """

    def __init__(self, site_title: str, site_url: str, site_profile: str):
        self.database_name = generate_service(site_title)
        self.database_user = generate_username()
        self.database_password = generate_password()
        self.database_root_password = generate_password()
        self.database_host = "database"
        self.database_port = get_port("MySQL")
        self.database_character_set = "utf8mb4"
        self.database_table_prefix = "woopy_"
        self.site_profile = site_profile
        self.site_title = site_title
        self.site_url = site_url

    # String representation of the class is docker-compose.yml data
    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the database
        """
        remote_profile = f"""
    {self.database_host}:
        image: mariadb:latest
        container_name: {self.database_host}
        hostname: {self.database_host}
        volumes:
            - ./{self.database_host}/:/var/lib/mysql
        environment:
            MARIADB_DATABASE: {self.database_name}
            MARIADB_USER: {self.database_user}
            MARIADB_PASSWORD: {self.database_password}
            MARIADB_ROOT_PASSWORD: {self.database_root_password}
            MARIADB_HOST: {self.database_host}
            MARIADB_PORT_NUMBER: {self.database_port}
            MARIADB_CHARACTER_SET: {self.database_character_set}
        networks:
            - {self.site_title}-network
        restart: unless-stopped
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.mysql.rule=Host(`{self.database_host}.{self.site_url}`)"
            - "traefik.http.routers.mysql.service=mysql"
            - "traefik.http.routers.mysql.entrypoints=websecure"
            - "traefik.http.services.mysql.loadbalancer.server.port=3306"
            - "traefik.http.routers.mysql.tls=true"
            - "traefik.http.routers.mysql.tls.certresolver=letsencrypt"
            - "traefik.http.services.mysql.loadbalancer.passhostheader=true"
            - "traefik.docker.network={self.site_title}-network"
            - "traefik.http.routers.mysql.middlewares=compresstraefik"
            - "traefik.http.middlewares.compresstraefik.compress=true"
            - "traefik.http.routers.mysql.middlewares=authtraefik"
            - "traefik.http.middlewares.authtraefik.basicauth.users={self.database_user}:{self.database_password}"
        healthcheck:
            test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
            interval: 10s
            timeout: 5s
            retries: 5
        logging:
            {get_logging()}
        """
        
        return remote_profile



class Cache:
    """
    Cache class: This class is used to create a cache for the website
    """

    def __init__(self, site_title: str, site_url: str, site_profile: str):
        self.cache_host = "cache"
        self.cache_port = get_port("Redis")
        self.cache_username = generate_username()
        self.cache_password = generate_password()
        self.site_profile = site_profile
        self.site_title = site_title
        self.site_url = site_url

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the cache
        """
        remote_profile = f"""
    {self.cache_host}:
        image: redis:latest
        container_name: {self.cache_host}
        hostname: {self.cache_host}
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
            - ./{self.cache_host}/:/data
        networks:
            - {self.site_title}-network
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.redis.rule=Host(`{self.cache_host}.{self.site_url}`)" 
            - "traefik.http.routers.redis.service=redis"
            - "traefik.http.routers.redis.entrypoints=websecure"
            - "traefik.http.services.redis.loadbalancer.server.port=6379"
            - "traefik.http.routers.redis.tls=true"
            - "traefik.http.routers.redis.tls.certresolver=letsencrypt"
            - "traefik.http.services.redis.loadbalancer.passhostheader=true"
            - "traefik.docker.network={self.site_title}-network"
            - "traefik.http.routers.redis.middlewares=compresstraefik"
            - "traefik.http.middlewares.compresstraefik.compress=true"
            - "traefik.http.routers.redis.middlewares=authtraefik"
            - "traefik.http.middlewares.authtraefik.basicauth.users={self.cache_username}:{self.cache_password}"
        restart: unless-stopped
        logging:
            {get_logging()}
        """
        
        return remote_profile


class Mail:
    """
    Mail class: This class is used to create a mail server for the website
    """

    def __init__(self, site_title: str, site_url: str, site_profile: str):
        self.mail_host = "mail"
        self.mail_base_url = f"mail.{site_url}"
        self.mail_username = generate_username()
        self.mail_password = generate_password()
        self.mail_port = get_port("Mailhog")
        self.mail_encryption = "TLS"
        self.mail_protocol = "smtp"
        self.site_profile = site_profile
        self.site_title = site_title
        self.site_url = site_url

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the mail server
        """
        remote_profile = f"""
    {self.mail_host}:
        image: mailhog/mailhog
        container_name: {self.mail_host}
        hostname: {self.mail_host}
        environment:
            - MH_UI_BIND_ADDR={self.mail_host}:8025
            - MH_SMTP_BIND_ADDR={self.mail_host}:1025
            - MH_API_BIND_ADDR={self.mail_host}:8025
            - MH_UI_WEB_PATH=/
        volumes:
            - ./{self.mail_host}/:/mailhog/
        ports:
            - "8025:8025"
            - "1025:{self.mail_port}"
            - "587:587"
            - "465:465"
        networks:
            - {self.site_title}-network
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.mailhog.rule=Host(`{self.mail_host}.{self.site_url}`)"
            - "traefik.http.routers.mailhog.service=mailhog"
            - "traefik.http.routers.mailhog.entrypoints=websecure"
            - "traefik.http.services.mailhog.loadbalancer.server.port=8025"
            - "traefik.http.routers.mailhog.tls=true"
            - "traefik.http.routers.mailhog.tls.certresolver=letsencrypt"
            - "traefik.http.services.mailhog.loadbalancer.passhostheader=true"
            - "traefik.docker.network={self.site_title}-network"
            - "traefik.http.routers.mailhog.middlewares=compresstraefik"
            - "traefik.http.middlewares.compresstraefik.compress=true"
            - "traefik.http.routers.mailhog.middlewares=authtraefik"
            - "traefik.http.middlewares.authtraefik.basicauth.users={self.mail_username}:{self.mail_password}"
        restart: unless-stopped
        logging:
            {get_logging()}
        """
        
        return remote_profile

    

class Website:
    """
    Website class: This class is used to create a website for the user
    """

    def __init__(self, site_title: str, site_url: str, site_profile: str, database_props: Database, mail_props: Mail, cache_props: Cache):
        self.database_host = f"{database_props.database_host}"
        self.database_port = f"{database_props.database_port}"
        self.database_name = f"{database_props.database_name}"
        self.database_user = f"{database_props.database_user}"
        self.database_password = f"{database_props.database_password}"
        self.database_table_prefix = f"{database_props.database_table_prefix}"
        self.site_url = "website"
        self.site_title = f"{site_title}"
        self.site_profile = site_profile
        self.website_description = f"Add description here for {site_title}: {datetime.now()}"
        self.website_admin_username = generate_username()
        # generate a hashed password with SHA-256 and base64 encoding
        self.website_admin_password = generate_password()
        self.website_admin_email = generate_email(self.site_url, "website")
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
        
        remote_profile: str = f"""
    {self.site_url}:
        image: wordpress:latest
        container_name: {self.site_url}
        hostname: {self.site_url}
        volumes:
            - ./{self.site_url}/:/var/www/html
        environment:
            - WORDPRESS_DATABASE_HOST={self.database_host}
            - WORDPRESS_DATABASE_PORT_NUMBER={self.database_port}
            - WORDPRESS_DATABASE_NAME={self.database_name}
            - WORDPRESS_DATABASE_USER={self.database_user}
            - WORDPRESS_DATABASE_PASSWORD={self.database_password}
            - WORDPRESS_TABLE_PREFIX={self.database_table_prefix}
            - WORDPRESS_BLOG_NAME={self.site_title}
            - WORDPRESS_USERNAME={self.website_admin_username}
            - WORDPRESS_PASSWORD={self.website_admin_password}
            - WORDPRESS_EMAIL={self.website_admin_email}
            - WORDPRESS_SMTP_HOST={self.mail_smtp_host}
            - WORDPRESS_SMTP_PORT={self.mail_smtp_port}
            - WORDPRESS_SMTP_USER={self.mail_smtp_user}
            - WORDPRESS_SMTP_PASSWORD={self.mail_smtp_password}
            - WORDPRESS_SMTP_PROTOCOL={self.mail_smtp_protocol}
            - WORDPRESS_CACHE_ENABLED=true
            - WORDPRESS_CACHE_DURATION=1440
            - WORDPRESS_CACHE_TYPE=redis
            - WORDPRESS_REDIS_HOST={self.cache_host}
            - WORDPRESS_REDIS_PORT={self.cache_port}
            - WORDPRESS_REDIS_DATABASE=0
            - WORDPRESS_REDIS_PASSWORD={self.cache_password}
            - WORDPRESS_SITE_URL={self.site_url}
        networks:
            - {self.site_title}-network
        depends_on:
            - {self.database_host}
            - {self.cache_host}
            - {self.mail_smtp_host}
        links:
            - {self.database_host}:{self.database_host}
            - {self.cache_host}:{self.cache_host}
            - {self.mail_smtp_host}:{self.mail_smtp_host}
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.wordpress.rule=Host(`{self.site_url}`)"
            - "traefik.http.routers.wordpress.service=wordpress"
            - "traefik.http.routers.wordpress.entrypoints=websecure"
            - "traefik.http.services.wordpress.loadbalancer.server.port=80"
            - "traefik.http.routers.wordpress.tls=true"
            - "traefik.http.routers.wordpress.tls.certresolver=letsencrypt"
            - "traefik.http.services.wordpress.loadbalancer.passhostheader=true"
            - "traefik.docker.network={self.site_title}-network"
            - "traefik.http.routers.wordpress.middlewares=compresstraefik"
            - "traefik.http.middlewares.compresstraefik.compress=true"
            - "traefik.http.routers.wordpress.middlewares=authtraefik"
            - "traefik.http.middlewares.authtraefik.basicauth.users={self.website_admin_username}:{self.website_admin_password}"
        restart: unless-stopped
        logging:
            {get_logging()}
        """
        
        return remote_profile


class Admin:
    """
    Admin class: This class is used to create an admin panel for the website
    """

    def __init__(self, site_title: str, site_profile: str, site_url: str, database_props: Database):
        self.admin_host = "admin"
        self.database_host = f"{database_props.database_host}"
        self.database_port = f"{database_props.database_port}"
        self.database_user = f"{database_props.database_user}"
        self.database_password = f"{database_props.database_password}"
        self.admin_username = generate_username()
        self.admin_password = generate_password()
        self.site_profile = site_profile
        self.site_title = site_title
        self.site_url = site_url

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the admin panel
        """
        remote_profile = f"""
    {self.admin_host}:
        image: phpmyadmin:latest
        container_name: {self.admin_host}
        hostname: {self.admin_host}
        environment:
            PMA_HOST: {self.database_host}
            PMA_PORT: {self.database_port}
            PMA_USER: {self.database_user}
            PMA_PASSWORD: {self.database_password}
            PMA_ARBITRARY: 1
        networks:
            - {self.site_title}-network
        depends_on:
            - {self.database_host}
        links:
            - {self.database_host}:{self.database_host}
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.phpmyadmin.rule=Host(`{self.admin_host}.{self.site_url}`)"
            - "traefik.http.routers.phpmyadmin.service=phpmyadmin"
            - "traefik.http.routers.phpmyadmin.entrypoints=websecure"
            - "traefik.http.services.phpmyadmin.loadbalancer.server.port=80"
            - "traefik.http.routers.phpmyadmin.tls=true"
            - "traefik.http.routers.phpmyadmin.tls.certresolver=letsencrypt"
            - "traefik.http.services.phpmyadmin.loadbalancer.passhostheader=true"
            - "traefik.docker.network={self.site_title}-network"
            - "traefik.http.routers.phpmyadmin.middlewares=authtraefik"
            - "traefik.http.middlewares.authtraefik.basicauth.users={self.admin_username}:{self.admin_password}"
        restart: unless-stopped
        logging:
            {get_logging()}
        """
        
       
        return remote_profile

    

class Proxy:
    """
    Proxy class: This class is used to create a proxy for the website
    """

    def __init__(self, site_title: str, site_url: str, site_profile: str):
        self.proxy_username = generate_username()
        self.proxy_password = generate_password()
        self.proxy_title = "synapse"
        self.proxy_host = self.proxy_title
        self.proxy_port = get_port("Traefik")
        self.proxy_username = generate_username()
        self.proxy_email = generate_email(self.proxy_host, "proxy")
        self.proxy_password = generate_password()
        self.site_profile = site_profile
        self.site_title = site_title
        self.site_url = site_url

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the proxy
        """
        remote_profile = f"""
    {self.proxy_host}:
        image: traefik:2.9
        container_name: {self.proxy_host}
        hostname: {self.proxy_host}
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
            - ./{self.proxy_host}/:/etc/traefik/acme/
        networks:
            - {self.site_title}-network
        ports:
            - "8080:80"
            - "443:443"
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.dashboard.rule=Host(`{self.proxy_host}.{self.site_url}`)"
            - "traefik.http.routers.dashboard.service=api@internal"
            - "traefik.http.routers.dashboard.entrypoints=websecure"
            - "traefik.http.services.dashboard.loadbalancer.server.port=8080"
            - "traefik.http.routers.dashboard.tls=true"
            - "traefik.http.routers.dashboard.tls.certresolver=letsencrypt"
            - "traefik.http.services.dashboard.loadbalancer.passhostheader=true"
            - "traefik.http.routers.dashboard.middlewares=authtraefik"
            - "traefik.http.middlewares.authtraefik.basicauth.users={self.proxy_username}:{self.proxy_password}"
            - "traefik.http.routers.http-catchall.rule=HostRegexp(`{{host:.+}}`)"
            - "traefik.http.routers.http-catchall.entrypoints=web"
            - "traefik.http.routers.http-catchall.middlewares=redirect-to-https"
            - "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https"
        restart: unless-stopped
        logging:
            {get_logging()}
        """
        
        return remote_profile

   

class Monitoring:
    """
    Monitoring class: This class is used to create a monitoring system for the host
    """

    def __init__(self, site_title: str, site_url: str, site_profile: str):
        self.monitoring_host = "monitoring"
        self.monitoring_port = get_port("Cadvisor")
        self.monitoring_username = generate_username()
        self.montiroing_email = generate_email(self.monitoring_host, "monitoring")
        self.monitoring_password = generate_password()
        self.site_profile = site_profile
        self.site_title = site_title
        self.site_url = site_url

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the monitoring system
        """
        remote_profile = f"""
    {self.monitoring_host}:
        image: gcr.io/cadvisor/cadvisor:v0.39.0
        container_name: {self.monitoring_host}
        hostname: {self.monitoring_host}
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
            - {self.site_title}-network
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.cadvisor.rule=Host(`cadvisor.{self.site_title}.{self.site_url}`)"
            - "traefik.http.routers.cadvisor.service=cadvisor"
            - "traefik.http.routers.cadvisor.entrypoints=websecure"
            - "traefik.http.services.cadvisor.loadbalancer.server.port=8080"
            - "traefik.http.routers.cadvisor.tls=true"
            - "traefik.http.routers.cadvisor.tls.certresolver=letsencrypt"
            - "traefik.http.services.cadvisor.loadbalancer.passhostheader=true"
            - "traefik.docker.network={self.site_title}-network"
        restart: unless-stopped
        logging:
            {get_logging()}
        """
        
       
        return remote_profile


class Management:
    """
    Management class: This class is used to create a management system for the website
    """

    def __init__(self, site_title: str, site_url: str, site_profile: str):
        self.management_host = "management"
        self.management_port = get_port("Portainer")
        self.management_username = generate_username()
        self.management_email = generate_email(self.management_host, "management")
        self.management_password = generate_password()
        self.site_profile = site_profile
        self.site_title = site_title
        self.site_url = site_url

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the management system
        """
        remote_profile = f"""
    {self.management_host}:
        image: portainer/portainer-ce:latest
        container_name: {self.management_host}
        hostname: {self.management_host}
        command:
            -H unix:///var/run/docker.sock
            --admin-password '{self.management_password}'
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
            - ./{self.management_host}/:/data
        networks:
            - {self.site_title}-network
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.portainer.rule=Host(`{self.management_host}.{self.site_url}`)"
            - "traefik.http.routers.portainer.service=portainer"
            - "traefik.http.routers.portainer.entrypoints=websecure"
            - "traefik.http.services.portainer.loadbalancer.server.port=9000"
            - "traefik.http.routers.portainer.tls=true"
            - "traefik.http.routers.portainer.tls.certresolver=letsencrypt"
            - "traefik.http.services.portainer.loadbalancer.passhostheader=true"
            - "traefik.docker.network={self.site_title}-network"
            - "traefik.http.routers.portainer.middlewares=authtraefik"
            - "traefik.http.middlewares.authtraefik.basicauth.users={self.management_username}:{self.management_password}"
        restart: unless-stopped
        logging:
            {get_logging()}
        """
        
        return remote_profile


class Vault:
    """
    Vault class: This class is used to create a vault for the website
    """

    def __init__(self, site_title: str, site_url: str, site_profile: str):
        self.vault_host = "vault"
        self.vault_port = get_port("Vault")
        self.vault_username = generate_username()
        self.vault_email = generate_email(self.vault_host, "vault")
        self.vault_password = generate_password()
        self.site_profile = site_profile
        self.site_title = site_title
        self.site_url = site_url

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the vault
        """
        return f"""
    {self.vault_host}:
        image: alpine:latest
        container_name: {self.vault_host}
        hostname: {self.vault_host}
        command: >
            /bin/sh -c "echo Vault username (encrypted):" && echo -n '{self.vault_username}' | sha256sum &&
            /bin/sh -c "echo Vault password (encrypted):" && echo -n '{self.vault_password}' | sha256sum
            /bin/sh -c "while true; do sleep 300; done;"
        networks:
            - {self.site_title}-network
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.vault.rule=Host(`{self.vault_host}.{self.site_url}`)"
            - "traefik.http.routers.vault.service=vault"
            - "traefik.http.routers.vault.entrypoints=websecure"
            - "traefik.http.services.vault.loadbalancer.server.port=8200"
            - "traefik.http.routers.vault.tls=true"
            - "traefik.http.routers.vault.tls.certresolver=letsencrypt"
            - "traefik.http.services.vault.loadbalancer.passhostheader=true"
            - "traefik.docker.network={self.site_title}-network"
            - "traefik.http.routers.vault.middlewares=authtraefik"
            - "traefik.http.middlewares.authtraefik.basicauth.users={self.vault_username}:{self.vault_password}"
        restart: unless-stopped
        logging:
            {get_logging()}
        """



class Code:
    """
    Code class: This class is used to create a code server for the website
    """

    def __init__(self, site_title: str, site_url: str, site_profile: str):
        self.code_host = "code"
        self.code_port = get_port("Code")
        self.code_username = generate_username()
        self.code_email = generate_email(self.code_host, "code")
        self.code_password = generate_password()
        self.proxy_domain = f"{site_url}"
        self.proxy_port = get_port("Traefik")
        self.site_profile = site_profile
        self.site_title = site_title
        self.site_url = site_url

    def to_docker_compose(self):
        """
        This function returns the docker-compose.yml data for the code server
        """
        remote_profile = f"""
    {self.code_host}:
        image: codercom/code-server
        container_name: {self.code_host}
        hostname: {self.code_host}
        environment:
            PASSWORD: {self.code_password}
            SUDO_PASSWORD: {self.code_password}
            TZ: Europe/Brussels
            PROXY_DOMAIN: {self.proxy_domain}
            PROXY_PORT: {self.proxy_port}
        volumes:
            - ./{self.code_host}/:/home/coder/project
        networks:
            - {self.site_title}-network
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.vscode.rule=Host(`{self.code_host}.{self.site_url}`)"
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
        
        return remote_profile

    
class Application:
    """
    Represents an application associated with a website.

    Attributes:
        website (Website): The website object associated with the application.
        version (str): The version of the application (default is "1.0").
    """

    def __init__(self, site_title: str, site_url: str, site_profile: str, version: str = "1.0"):
        """
        Initializes a new instance of the Application class.

        Args:
            website (Website): The website object associated with the application.
            version (str, optional): The version of the application (default is "1.0").
        """
        self.app_host= f"app"
        self.project_name = self.app_host
        self.app_name = self.app_host
        # reverse the host name. for example if the host url is "example.xyz" then the bundle will be "xyz.example"
        self.bundle = ".".join(site_url.split(".")[::-1])
        self.version = version
        self.url = site_url
        self.license = "MIT license"
        self.author = generate_username()
        self.author_email = generate_email(self.app_host, "app")
        self.formal_name = self.app_host
        self.description = f"{self.app_name} is a native application for {self.app_host}."
        self.long_description = f"{self.app_name} is designed to provide a user-friendly interface for {self.app_host}. It can be installed on Linux, macOS, Windows, Android, iOS. It is written in Python using Toga and Briefcase frameworks."
        self.site_profile = site_profile
        self.site_title = site_title

    def to_docker_compose(self):
        """
        Converts the Application object to a docker-compose.yml data string.

        Returns:
            str: The docker-compose.yml data string representing the Application object.
        """

        remote_profile = f"""
    {self.app_host}:
        image: docker.io/yilmazchef/woopy-app:latest
        container_name: {self.app_host}
        hostname: {self.app_host}
        command: >
            /bin/bash -c "/app/entrypoint.sh"
            /bin/sh -c "while true; do sleep 30000; done;"
        networks:
            - {self.site_title}-network
        labels:
            - "traefik.enable=false"
        restart: unless-stopped
        logging:
            {get_logging()}
        """
        
        return remote_profile



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
        """
        Returns the prerequisites setup content.
        """
        return self.prerequisites_setup_content



class Project:
    """
    Represents a project with multiple services: website, database, cache, admin, proxy, monitoring, management, vault, code, application, networks, volumes and more.
    """

    def __init__(self, website: Website = None, database: Database = None, cache: Cache = None,
                 admin: Admin = None, proxy: Proxy = None, monitoring: Monitoring = None,
                 management: Management = None, vault: Vault = None, code: Code = None,
                 mail: Mail = None, application: Application = None):
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
        self.vault = vault
        self.code = code
        self.application = application
        self.mail = mail

    def get_docker_compose_data(self):
        """
        Converts the Project object to a docker-compose.yml data string.
        """
        docker_compose_yaml = f"""
networks:
    {self.website.site_title}-network: {{}}

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
    {self.mail.to_docker_compose()}
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
Website Hostname: {self.website.site_url}
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
Code Profile: {self.code.site_profile}
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
Application Profile: {self.application.site_profile}
-------------------------------------------------------------
Mail Hostname: {self.mail.mail_host}
Mail Port: {self.mail.mail_port}
Mail Username: {self.mail.mail_username}
Mail Password: {self.mail.mail_password}
Mail Profile: {self.mail.site_profile}
-------------------------------------------------------------
networks:
{self.website.site_title}-network
-------------------------------------------------------------
        """

        return report


class GitIgnore:
    """
    GitIgnore class: This class is used to create a .gitignore file for the project
    Ignored files:
        - Windows Thumbs.db file
        - macOS .DS_Store file
        - Linux .DS_Store file
        - Python __pycache__ directory
        - Java .class files
        - Node.js node_modules directory
        - Visual Studio Code .vscode directory
        - JetBrains IntelliJ IDEA .idea directory
        - Eclipse .metadata directory
        - Docker .docker directory
        - Git .git directory
        - GitHub .github directory
        - Travis CI .travis.yml file
        - Jenkinsfile file
        - CircleCI .circleci directory
        - Dockerfile file
    """
    
    def __init__(self):
        self.gitignore_content = """
# Windows Thumbs.db file
Thumbs.db

# macOS .DS_Store file
.DS_Store

# Linux .DS_Store file
.DS_Store

# Python __pycache__ directory
__pycache__

# Java .class files
*.class

# Node.js node_modules directory
node_modules

# Visual Studio Code .vscode directory
.vscode

# JetBrains IntelliJ IDEA .idea directory
.idea

# Eclipse .metadata directory
.metadata

# Docker .docker directory
.docker

# Git .git directory
.git

# GitHub .github directory
.github

# Travis CI .travis.yml file
.travis.yml

# Jenkinsfile file
Jenkinsfile

# CircleCI .circleci directory
.circleci

# Dockerfile file
Dockerfile

"""

    def get_gitignore(self):
        """
        Returns the gitignore content.
        """
        return self.gitignore_content


class DockerIgnore:
    """
    DockerIgnore class: This class is used to create a .dockerignore file for the project
    Ignored files:
        - Windows Thumbs.db file
        - macOS .DS_Store file
        - Linux .DS_Store file
        - Common files
    """
    
    def __init__(self):
        self.dockerignore_content = """
# Windows Thumbs.db file
Thumbs.db

# macOS .DS_Store file
.DS_Store

# Linux .DS_Store file
.DS_Store

# Common auto-generated files
*.log
/tmp
*.tmp
*.bak
*.swp

"""

    def get_dockerignore(self):
        """
        Returns the dockerignore content.
        """
        return self.dockerignore_content

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
        site_profile=env["SITE_PROFILE"]

        database = Database(site_title=site_title, site_url=site_url, site_profile=site_profile)
        mail = Mail(site_title=site_title, site_url=site_url, site_profile=site_profile)
        cache = Cache(site_title=site_title, site_url=site_url, site_profile=site_profile)
        website = Website(site_title=site_title, site_url=site_url, site_profile=site_profile, database_props=database, mail_props=mail, cache_props=cache)
        admin = Admin(site_title=site_title, site_url=site_url, site_profile=site_profile, database_props=database)
        proxy = Proxy(site_title=site_title, site_url=site_url, site_profile=site_profile)
        monitoring = Monitoring(site_title=site_title, site_url=site_url, site_profile=site_profile)
        management = Management(site_title=site_title, site_url=site_url, site_profile=site_profile)
        vault = Vault(site_title=site_title, site_url=site_url, site_profile=site_profile)
        code = Code(site_title=site_title, site_url=site_url, site_profile=site_profile)
        application = Application(site_title=site_title, site_url=site_url, site_profile=site_profile)

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
            mail=mail
        )
        
        readme = ReadMe(project_name=project.project_name)
        prerequisites_setup = PreequisitesSetup()
        
        gitignore = GitIgnore()
        dockerignore = DockerIgnore()
        

        # Create docker-compose.yaml file in current working directory / site_title / docker-compose.yml
        project_docker_compose_file = os.path.join(project.project_base_dir, 'docker-compose.yml')
        if not os.path.exists(project.project_base_dir):
            os.makedirs(project.project_base_dir)
        with open(project_docker_compose_file, 'w', encoding='utf-8') as f:
            docker_compose_data = project.get_docker_compose_data()
            f.write(docker_compose_data)
            logging.info(
                '################################################################################################')
            logging.info(
                f'Generated docker-compose.yml file for {website.site_title} in {project_docker_compose_file}')
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
                    f'Generated project-report.txt file for {website.site_title} in {project_report_file}')
                logging.info(
                    '################################################################################################')
                
            
            # generate README.md file
            project_readme_file = os.path.join(project.project_base_dir, 'README.md')
            with open(project_readme_file, 'w', encoding='utf-8') as f:
                f.write(readme.readme_content)
                logging.info(
                    '################################################################################################')
                logging.info(
                    f'Generated README.md file for {website.site_title} in {project_readme_file}')
                logging.info(
                    '################################################################################################')
                
                
            # generate prerequisites-setup.sh file for the project
            prerequisites_setup_file = os.path.join(project.project_base_dir, 'prerequisites-setup.sh')
            with open(prerequisites_setup_file, 'w', encoding='utf-8') as f:
                f.write(prerequisites_setup.get_script())
                logging.info(
                    '################################################################################################')
                logging.info(
                    f'Generated prerequisites-setup.sh file for {website.site_title} in {prerequisites_setup_file}')
                logging.info(
                    '################################################################################################')
                
            
            # generate .gitignore file for the project
            gitignore_file = os.path.join(project.project_base_dir, '.gitignore')
            with open(gitignore_file, 'w', encoding='utf-8') as f:
                f.write(gitignore.get_gitignore())
                logging.info(
                    '################################################################################################')
                logging.info(
                    f'Generated .gitignore file for {website.site_title} in {gitignore_file}')
                logging.info(
                    '################################################################################################')
                
                
            # generate .dockerignore file for the project
            dockerignore_file = os.path.join(project.project_base_dir, '.dockerignore')
            with open(dockerignore_file, 'w', encoding='utf-8') as f:
                f.write(dockerignore.get_dockerignore())
                logging.info(
                    '################################################################################################')
                logging.info(
                    f'Generated .dockerignore file for {website.site_title} in {dockerignore_file}')
                logging.info(
                    '################################################################################################')
                

        project_zip_file = os.path.join(project.project_base_dir, 'project.zip')
        with ZipFile(project_zip_file, 'w', compression=ZIP_DEFLATED) as zip:
            zip.write(project_docker_compose_file, 'docker-compose.yml')
            zip.write(project_report_file, 'project-report.txt')
            zip.write(project_readme_file, 'README.md')
            zip.write(prerequisites_setup_file, 'prerequisites-setup.sh')
            zip.write(gitignore_file, '.gitignore')
            zip.write(dockerignore_file, '.dockerignore')
            logging.info(
                '################################################################################################')
            logging.info(
                f'Generated project.zip file for {website.site_title} in {project_zip_file}')
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