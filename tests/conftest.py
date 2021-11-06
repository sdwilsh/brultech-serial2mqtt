from typing import Any, Dict

import pytest
from _pytest.config import Config as PytestConfig
from _pytest.fixtures import SubRequest

from brultech_serial2mqtt.config import CONFIG_SCHEMA, Config


def pytest_configure(config: PytestConfig):
    config.addinivalue_line(
        "markers", "local_config(config): mark tests to provide a config for the test"
    )


@pytest.fixture()
def local_config(request: SubRequest):
    marker = request.node.get_closest_marker("local_config")
    assert marker is not None and isinstance(marker.args[0], dict)
    test_config: Dict[str, Any] = marker.args[0]
    valid_config: Dict[str, Any] = CONFIG_SCHEMA(test_config)
    yield Config(valid_config)
