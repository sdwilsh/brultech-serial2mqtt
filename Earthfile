VERSION 0.7
FROM alpine

# renovate: datasource=docker depName=python
ARG --global PYTHON_VERSION=3.12

brultech-serial2mqtt:
    ARG PYTHON_VERSION
    ARG TARGETPLATFORM
    FROM DOCKERFILE \
        --build-arg PYTHON_VERSION=$PYTHON_VERSION \
        -f docker/Dockerfile \
        --platform $TARGETPLATFORM .
    SAVE IMAGE brultech_serial2mqtt:latest

build:
    BUILD --platform linux/amd64 +brultech-serial2mqtt
    BUILD --platform linux/arm64 +brultech-serial2mqtt

python-requirements:
    ARG PYTHON_VERSION
    FROM python:$PYTHON_VERSION
    WORKDIR /usr/src/app
    COPY requirements.txt .
    COPY setup.cfg .
    COPY setup.py .
    RUN pip install --no-cache-dir -r requirements.txt

python-dev-requirements:
    FROM +python-requirements
    WORKDIR /usr/src/app
    COPY pyproject.toml .
    COPY requirements-dev.txt .
    RUN pip install --no-cache-dir -r requirements-dev.txt -r requirements.txt

pyright-image:
    FROM +python-dev-requirements
    RUN nodeenv /.cache/nodeenv
    ENV PYRIGHT_PYTHON_ENV_DIR=/.cache/nodeenv
    WORKDIR /usr/src/app

pyright-validate:
    FROM +pyright-image
    COPY --dir brultech_serial2mqtt/ .
    COPY --dir tests/ .
    COPY --dir typings/ .
    RUN pyright

renovate-validate:
    # renovate: datasource=docker depName=renovate/renovate versioning=docker
    ARG RENOVATE_VERSION=37
    FROM renovate/renovate:$RENOVATE_VERSION
    WORKDIR /usr/src/app
    COPY renovate.json .
    RUN renovate-config-validator

ruff-validate:
    FROM +python-dev-requirements
    WORKDIR /usr/src/app
    COPY pyproject.toml .
    COPY --dir brultech_serial2mqtt .
    COPY --dir tests .
    COPY --dir typings/ .
    RUN ruff check . --diff
    RUN ruff format . --diff

lint:
    BUILD +pyright-validate
    BUILD +renovate-validate
    BUILD +ruff-validate

test:
    FROM +python-dev-requirements
    COPY --dir brultech_serial2mqtt .
    COPY --dir tests .
    RUN pytest
