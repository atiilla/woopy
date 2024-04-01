# WooPy

![woopy](https://raw.githubusercontent.com/atiilla/woopy/main/logo.svg)

## What does this application do for your website?
What will docker-compose contain?
- Database: `mysql/mariadb`
- Website: `wordpress`
- Admin: `phpmyadmin`
- Proxy: `traefik`
- Cache: `redis`
- Monitoring: `cadvisor`
- Management: `portainer`
- Vault: `a tool for securely accessing secrets`
- Code: `online vscode`


# CLI

## Generate Docker Compose File

```bash
python -m cli gen-dc test
```

# API (Swagger)

## Generate Docker Compose File for testing purposes 

```bash
mkdir -p /tmp/test
cd /tmp/test
```

```bash
curl -X 'POST' \
  'http://localhost:5000/docker-compose' \
  -H 'accept: application/json' \
  -H 'Content-Type: text/plain' \
  -d 'HOST_HOSTNAME=website
HOST_IP=127.0.0.1
HOST_MAC=00:00:00:00:00:00
HOST_CPU=4
HOST_RAM=8GB
HOST_OS=Ubuntu
HOST_KERNEL=5.4.0
HOST_DOCKER=true
CACHE_HOST=cache
CACHE_PORT=6379
DATABASE_HOST=database
DATABASE_PORT=3306
DATABASE_NAME=vinci
DATABASE_USER=vinci
DATABASE_TABLE_PREFIX=wpapp_
WEBSITE_TITLE=VinciPizzeria
WEBSITE_HOSTNAME=vincipizzeria.nl
WEBSITE_NAME=vinci
WEBSITE_ADMIN_FIRSTNAME=Vakif
WEBSITE_ADMIN_LASTNAME=Inci
WEBSITE_ADMIN_USERNAME=vinci
WEBSITE_ADMIN_EMAIL=admin@vincipizzeria.nl
MAIL_SMTP_HOST=smtp.vincipizzeria.nl
MAIL_SMTP_PORT=587
MAIL_SMTP_USER=admin@vincipizzeria.nl
MAIL_SMTP_PROTOCOL=tls
WORDPRESS_REDIS_HOST=cache
WORDPRESS_REDIS_PORT=6379
WORDPRESS_CACHE_ENABLED=true
WORDPRESS_CACHE_DURATION=1440
WORDPRESS_CACHE_TYPE=redis
PMA_USER=phpmyadmin_user
WOOCOMMERCE_ENABLED=true
WOOCOMMERCE_TAX_ENABLED=true
WOOCOMMERCE_TAX_COUNTRY=BE
WOOCOMMERCE_TAX_STATE=Vlaams-Brabant
WOOCOMMERCE_TAX_RATE=21
WOOCOMMERCE_TAX_SHIPPING_ENABLED=true
WOOCOMMERCE_TAX_SHIPPING_TAX_CLASS=standard
WOOCOMMERCE_TAX_SHIPPING_TAX_RATE=21
WOOCOMMERCE_TAX_SHIPPING_TAX_PRIORITY=1
WOOCOMMERCE_URL=https://vincipizzeria.nl
WOOCOMMERCE_KEY=ck_cc98aff2b3e87a082f0bed39f42d5e618ae2e354
WOOCOMMERCE_SECRET=cs_bedb5887c9294e347eb3579ea18ce72fbbf6f633
WOOCOMMERCE_CURRENCY=EUR
WOOCOMMERCE_CURRENCY_POSITION=right
WOOCOMMERCE_CURRENCY_THOUSANDS_SEPARATOR=.
WOOCOMMERCE_CURRENCY_DECIMAL_SEPARATOR=,
WOOCOMMERCE_CURRENCY_DECIMALS=2
REMOTE_SERVER_USERNAME=root
REMOTE_SERVER_IP=vincipizzeria.nl
REMOTE_SERVER_PORT=22
REMOTE_SERVER_PATH=/tmp
PROXY_TITLE=proxy
PROXY_HOSTNAME=proxy
' >> docker-compose.yml
```
