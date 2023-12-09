import pytest
from typing import Any, Dict, Generator
from brultech_serial2mqtt.config import CONFIG_SCHEMA, Config


@pytest.fixture()
def local_config(
    config: Dict[str, Any],
) -> Generator[Config, None, None]:
    valid_config: Dict[str, Any] = CONFIG_SCHEMA(config)
    yield Config(valid_config)
