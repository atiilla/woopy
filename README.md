# Setup

## Install Docker
```bash
apt-get update
apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common
```

```bash
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
```

```bash
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
```

```bash
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io
```

```bash
docker --version
```

```bash
docker-compose --version
```

```bash
docker run hello-world
```

```bash
usermod -aG docker $USER
```

```bash
su - $USER
```

```bash
docker run hello-world
```

```bash
docker stop $(docker ps -a -q)
```

```bash
docker rm $(docker ps -a -q)
```

## Install Docker Compose
```bash
sudo apt-get install -y python3-pip
```

```bash
pip3 install docker-compose
```

```bash
docker-compose --version
```

```bash
docker-compose up -d
```

```bash
docker-compose down
```


## Install Docker
```bash
cd test
```

## Start Docker Compose Services

```bash
docker-compose up -d
```

## Stop Docker Compose Services

```bash
docker-compose down
```

## Stop Docker Compose Services and Remove Volumes

```bash
docker-compose down --volumes
```

## Stop Docker Compose Services and Remove Images

```bash
docker-compose down --rmi all
```

## Stop Docker Compose Services and Remove Volumes and Images

```bash
docker-compose down --volumes --rmi all
```

## Execute a Command in a Running Container

```bash
docker-compose exec wordpress wp plugin install woocommerce --activate
docker-compose exec wordpress wp plugin install stripe-for-woocommerce --activate
```

## Execute a Command in a Running Container as Root

```bash
docker-compose exec --user root wordpress wp plugin install woocommerce --activate
docker-compose exec --user root wordpress wp plugin install stripe-for-woocommerce --activate
```


# CLI

## Generate Docker Compose File

```bash
python -m cli gen-dc test
```

## Generate Docker Compose File if already exists (overwrite)

```bash
python -m cli gen-dc test --force
```

## Generate Docker Compose File and Start Services

```bash
python -m cli gen-dc test --start
```

## Generate Docker Compose File and Start Services if already exists (overwrite)

```bash
python -m cli gen-dc test --force --start
```

## Generate Docker Compose File and Start Services and Open Browser

```bash
python -m cli gen-dc test --start --open
```

## Generate Docker Compose File and Start Services and Open Browser if already exists (overwrite)

```bash
python -m cli gen-dc test --force --start --open
```

## Generate Docker Compose File and Start Services and Open Browser and Import Products

```bash
python -m cli gen-dc test --start --open --import
```

## Generate Docker Compose File and Start Services and Open Browser and Import Products if already exists (overwrite)

```bash
python -m cli gen-dc test --force --start --open --import
```

## Generate Docker Compose File and Start Services and Install Plugins or Themes

```bash
python -m cli gen-dc test --start --open --plugins --themes
```

## Generate Docker Compose File and Start Services and Install Plugins or Themes if already exists (overwrite)

```bash
python -m cli gen-dc test --force --start --open --plugins --themes
```

## Generate Docker Compose File and Start Services and Install Plugins or Themes and Import Products

```bash
python -m cli gen-dc test --start --open --plugins --themes --import
```

# API (Swagger)

## Generate Docker Compose File and Start Services and Open Browser and Import Products

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

## Generate Docker Compose File and Start Services:

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

```bash
docker-compose up -d
```
