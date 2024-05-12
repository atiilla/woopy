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
- Application: `a cross-platform native application of your webshop`


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
  -d 'SITE_TITLE=mydemowebsite \
SITE_URL=mydemowebsite.com
SITE_PROFILE=dev
' >> docker-compose.yml
```
