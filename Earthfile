VERSION 0.7
FROM alpine

python-requirements:
    # renovate: datasource=docker depName=python versioning=docker
    ARG PYTHON_VERSION=3.10
    FROM python:$PYTHON_VERSION
    WORKDIR /usr/src/app
    COPY requirements.txt .
    COPY setup.cfg .
    COPY setup.py .
    RUN pip install --no-cache-dir -r requirements.txt

python-dev-requirements:
    FROM +python-requirements
    WORKDIR /usr/src/app
    COPY requirements-dev.txt .
    RUN pip install --no-cache-dir -r requirements-dev.txt

pyright-validate:
    # renovate: datasource=pypi depName=pyright
    ARG PYRIGHT_VERSION=1.1.296
    FROM +python-dev-requirements
    RUN pip install --no-cache-dir pyright==$PYRIGHT_VERSION
    WORKDIR /usr/src/app
    COPY pyproject.toml .
    COPY brultech_serial2mqtt/ brultech_serial2mqtt/
    COPY tests/ tests/
    COPY typings/ typings/
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
    COPY brultech_serial2mqtt .
    COPY tests .
    RUN ruff check . --diff

lint:
    BUILD +pyright-validate
    BUILD +renovate-validate
    BUILD +ruff-validate