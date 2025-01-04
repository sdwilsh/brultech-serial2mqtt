FROM ghcr.io/linuxserver/baseimage-ubuntu:jammy

LABEL maintainer="sdwilsh"
LABEL org.opencontainers.image.description="This talks to Brultech devices over a serial port and sends their data to an MQTT server"
LABEL org.opencontainers.image.licenses=MIT
LABEL org.opencontainers.image.source=https://github.com/sdwilsh/brultech-serial2mqtt

# renovate: datasource=docker depName=python versioning=python
ARG PYTHON_VERSION=3.12

ENV PYTHON=python${PYTHON_VERSION}

ENV DEBIAN_FRONTEND="noninteractive"
RUN \
    echo "########## Install Packages ##########" && \
    apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common=0.99.* && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends -q \
    python${PYTHON_VERSION}=${PYTHON_VERSION}.* \
    python${PYTHON_VERSION}-venv=${PYTHON_VERSION}.* \
    && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    echo "########## Install Pip ##########" && \
    ${PYTHON} -m ensurepip

COPY LICENSE /src/brultech_serial2mqtt/LICENSE
COPY pyproject.toml /src/brultech_serial2mqtt/pyproject.toml
COPY requirements.txt /src/brultech_serial2mqtt/requirements.txt
COPY brultech_serial2mqtt /src/brultech_serial2mqtt/brultech_serial2mqtt
WORKDIR /src/brultech_serial2mqtt
RUN \
    echo "########## Install Python Package and Deps ##########" && \
    ${PYTHON} -m pip install --no-cache-dir -r requirements.txt && \
    echo "########## Add User to Dialout Group ##########" && \
    usermod abc -a -G dialout
RUN \
    echo "########## Final Cleanup ##########" && \
    rm -rf \
    /tmp/* \
    /var/lib/apt/lists/* \
    /var/tmp/*

COPY docker/root /

VOLUME /config