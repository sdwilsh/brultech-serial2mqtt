# Lists all targets
[private]
default:
    @just --list

# Builds the docker container for the specified platform
[group('build')]
build-image platform:
    docker buildx build \
        -f docker/Dockerfile \
        --platform {{ platform }} \
        .

# Run `hadolint` on all `Dockerfile`s
[group('lint')]
hadolint:
    #!/usr/bin/env bash
    set -eou pipefail
    find . -type f -name "Dockerfile*" | while read -r file; do
        echo -n "Running \`hadolint\` on ${file}..."
        hadolint ${file}
        echo "{{ BOLD + GREEN }}OK{{ NORMAL }}"
    done

# Check `just` syntax
[group('lint')]
just-check:
    #!/usr/bin/env bash
    set -eou pipefail
    find . -type f -name "justfile" | while read -r file; do
        echo -n "Running \`just --fmt --check\` on ${file}..."
        just --unstable --fmt --check -f ${file}
        echo "{{ BOLD + GREEN }}OK{{ NORMAL }}"
    done

# Fixes `just` syntax
[group('format')]
[group('lint')]
just-format:
    #!/usr/bin/env bash
    set -eou pipefail
    find . -type f -name "justfile" | while read -r file; do
        echo "Running \`just --fmt\` on ${file}..."
        just --unstable --fmt -f ${file}
    done

# Runs all linters
lint: hadolint just-check just-format pyright renovate-validate ruff-check ruff-format yamllint

# Check Python code with Pyright

[group('lint')]
pyright:
    pyright

# Run pytest tests
[group('test')]
pytest:
    @pytest

# Validate `renovate.json` file
[group('lint')]
renovate-validate:
    renovate-config-validator

# Check Python code with Ruff
[group('lint')]
ruff-check:
    ruff check . --diff

# Check Python code formatting with Ruff
[group('format')]
[group('lint')]
ruff-format:
    ruff format . --diff

# Check YAML files with yamllint
[group('lint')]
yamllint:
    yamllint .
