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

test:
    FROM +python-dev-requirements
    COPY --dir brultech_serial2mqtt .
    COPY --dir tests .
    RUN pytest
