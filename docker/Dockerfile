FROM --platform=linux/amd64 ghcr.io/linuxserver/baseimage-ubuntu:focal
FROM --platform=linux/arm/v7 ghcr.io/linuxserver/baseimage-ubuntu:arm32v7-focal
FROM --platform=linux/arm64 ghcr.io/linuxserver/baseimage-ubuntu:arm64v8-focal

LABEL maintainer="sdwilsh"

ENV DEBIAN_FRONTEND="noninteractive"
RUN \
    echo "########## Install Packages ##########" && \
    apt-get update && \
    apt-get install -y --no-install-recommends -q \
    python3 \
    python3-distutils \
    python3-pip \
    && \
    apt-get autoremove && \
    apt-get clean

COPY LICENSE /src/brultech_serial2mqtt/LICENSE
COPY pyproject.toml /src/brultech_serial2mqtt/pyproject.toml
COPY requirements.txt /src/brultech_serial2mqtt/requirements.txt
COPY setup.cfg /src/brultech_serial2mqtt/setup.cfg
COPY setup.py /src/brultech_serial2mqtt/setup.py
COPY brultech_serial2mqtt /src/brultech_serial2mqtt/brultech_serial2mqtt
WORKDIR /src/brultech_serial2mqtt
RUN \
    echo "########## Install Python Deps ##########" && \
    pip install -r requirements.txt
RUN \
    echo "########## Final Cleanup ##########" && \
    rm -rf \
    /tmp/* \
    /var/lib/apt/lists/* \
    /var/tmp/*

COPY docker/root /

VOLUME /config