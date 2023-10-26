ARG PYTHON_VERSION=3.11.4-alpine3.18

FROM python:${PYTHON_VERSION} as base-image

RUN \
    apk update && \
    apk upgrade && \
    pip install --upgrade pip && \
    pip install pipenv

FROM base-image as compile-image

ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1

COPY Pipfile Pipfile.lock ./

RUN \
    apk update && \
    apk upgrade && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    pipenv install --dev --python 3.11 --verbose && \
    apk --purge del .build-deps

FROM base-image as runtime

ENV PYTHONUNBUFFERED=1

COPY --from=compile-image /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /app

RUN \
    apk update && \
    apk upgrade && \
    apk add bash postgresql-libs && \
    rm -rf /var/cache/apk/*

COPY . .

ARG GUNICORN_WORKERS=3

ENV GUNICORN_WORKERS=${GUNICORN_WORKERS}

EXPOSE 8000

CMD gunicorn --workers ${GUNICORN_WORKERS} core.wsgi:application --bind 0.0.0.0:8000
