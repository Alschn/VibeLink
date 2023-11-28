<div align="center" style="padding-bottom: 20px;">
    <h1>VibeLink</h1>
    <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Celery-8C9A41?&style=for-the-badge&logo=celery&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Docker-008FCC?style=for-the-badge&logo=docker&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Railway-%23000000.svg?&style=for-the-badge&logo=railway&logoColor=white" alt=""/>
</div>

<p align="center">VibeLink - Share links to music with your friends once a day.</p>

## Setup

### Environment variables

Create a `env` directory with following dotenv files:

`env/backend.env`

```dotenv
DJANGO_SETTINGS_MODULE=core.settings.base
DEBUG=True
SECRET_KEY=randomsecretkey
ALLOWED_HOSTS=backend,localhost,127.0.0.1,host.docker.internal,*
SIMPLE_JWT_ISSUER=vibelink
FRONTEND_SITE_NAME=VibeLink

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres_db
DB_PORT=5432

REDIS_HOST=redis_db
REDIS_PORT=6379

USE_SMTP=True
EMAIL_HOST=...
EMAIL_PORT=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
EMAIL_USE_TLS=True

# Spotify API keys
# https://developer.spotify.com/dashboard
SPOTIPY_CLIENT_ID=...
SPOTIFT_CLIENT_SECRET=...

# Google API key
# https://console.cloud.google.com/apis/credentials
GOOGLE_CLOUD_API_KEY=...
```

`env/postgres.env`

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

`env/redis.env`

```dotenv
TZ=Europe/Warsaw
```

### Virtual environment

Create a virtual environment in the current directory and install dependencies:

```shell script
mkdir .venv

pipenv shell

pipenv install
```

Set your Python interpreter to the one in the virtual environment.

### Docker

Make sure Docker Engine is running.

While in root directory, build docker images and run them with docker-compose. This might take some time depending on
your internet speed.
Rebuilding image is crucial after installing new packages via pip.

```shell
docker compose build
```

To start containers run:

```shell
docker compose up
```

To stop containers run:

```shell
docker compose down
```

To run commands in an active container:

```shell
docker compose exec -it CONTAINER_NAME COMMAND
```

### Django commands to run

Prepare migrations (if there are any changes to db schema):

```shell
docker exec -it vibe-link-backend python manage.py makemigrations
```

Apply migrations:

```shell
docker exec -it vibe-link-backend python manage.py migrate
```

Create superuser:

```shell
docker exec -it vibe-link-backend python manage.py createsuperuser
```

To run an interactive python shell:

```shell
docker exec -it vibe-link-backend python manage.py shell_plus
```

To run unit tests:

```shell
docker exec -it vibe-link-backend coverage run manage.py test
```

To get coverage report from unit tests run:

```shell
docker exec -it vibe-link-backend coverage report -m
```
