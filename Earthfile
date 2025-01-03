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
