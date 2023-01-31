FROM ghcr.io/linuxserver/baseimage-ubuntu:focal

LABEL maintainer="sdwilsh"

ENV DEBIAN_FRONTEND="noninteractive"
RUN \
    echo "########## Install Packages ##########" && \
    apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common=0.99.* && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends -q \
    python3.10=3.10.* \
    python3.10-distutils=3.10.* \
    python3.10-venv=3.10.* \
    && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    echo "########## Install Pip ##########" && \
    python3.10 -m ensurepip

COPY LICENSE /src/brultech_serial2mqtt/LICENSE
COPY pyproject.toml /src/brultech_serial2mqtt/pyproject.toml
COPY requirements.txt /src/brultech_serial2mqtt/requirements.txt
COPY setup.cfg /src/brultech_serial2mqtt/setup.cfg
COPY setup.py /src/brultech_serial2mqtt/setup.py
COPY brultech_serial2mqtt /src/brultech_serial2mqtt/brultech_serial2mqtt
WORKDIR /src/brultech_serial2mqtt
RUN \
    echo "########## Install Python Package and Deps ##########" && \
    python3.10 -m pip install --no-cache-dir -r requirements.txt && \
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