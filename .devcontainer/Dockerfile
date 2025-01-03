# renovate: datasource=docker depName=python
ARG PYTHON_VERSION=3.12
FROM mcr.microsoft.com/devcontainers/python:1-${PYTHON_VERSION}

# Install Python Dependencies
WORKDIR /tmp
COPY pyproject.toml pyproject.toml
COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
RUN pip3 install --no-cache-dir -r requirements-dev.txt -r requirements.txt \
  && rm pyproject.toml requirements.txt requirements-dev.txt

# Pre-cache Node for Pyright
RUN nodeenv /.cache/nodeenv
ENV PYRIGHT_PYTHON_ENV_DIR=/.cache/nodeenv
