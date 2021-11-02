import logging
import os
import sys
from typing import Any, Dict

import yaml
from voluptuous import Optional, Required, Schema
from yaml.nodes import Node

from brultech_serial2mqtt.config.typing import EmptyConfigDict
from brultech_serial2mqtt.const import CONFIG_PATH, SECRETS_PATH

from .config_device import DeviceConfig
from .config_logging import LoggingConfig
from .config_mqtt import MQTTConfig

logger = logging.getLogger(__name__)

CONFIG_SCHEMA = Schema(
    {
        Required("device"): DeviceConfig.schema,
        Optional("logging", default=EmptyConfigDict): LoggingConfig.schema,
        Required("mqtt"): MQTTConfig.schema,
    }
)


class Config:
    def __init__(self, config: Dict[str, Any]):
        self._device = DeviceConfig(config["device"])
        self._logging = LoggingConfig(config["logging"])
        self._mqtt = MQTTConfig(config["mqtt"])

    @property
    def device(self) -> DeviceConfig:
        return self._device

    @property
    def logging(self) -> LoggingConfig:
        return self._logging

    @property
    def mqtt(self) -> MQTTConfig:
        return self._mqtt


def load_secrets(root: str) -> Any:
    """Return secrets from secrets.yml."""
    secrets_path = os.path.join(root, SECRETS_PATH)
    try:
        logger.debug(f"Loading secrets in '{secrets_path}'...")
        with open(secrets_path, "r") as secrets_file:
            return yaml.load(secrets_file, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        return None


def load_config(root: str = "/") -> Config:
    """Return contents of config.yml."""
    secrets = load_secrets(root)

    def secret_yaml(_: Any, node: Node):
        if secrets is None:
            raise ValueError(
                "!secret found in config.yml, but no secrets.yml exists. "
                f"Make sure it exists under {os.path.join(root, SECRETS_PATH)}"
            )
        if node.value not in secrets:
            raise ValueError(f"secret {node.value} does not exist in secrets.yaml")
        return secrets[node.value]

    yaml.add_constructor("!secret", secret_yaml, Loader=yaml.SafeLoader)

    config_path = os.path.join(root, CONFIG_PATH)
    try:
        logger.debug(f"Loading config in '{config_path}'...")
        with open(config_path, "r") as config_file:
            raw_config = yaml.load(config_file, Loader=yaml.SafeLoader)
            logger.debug(f"loaded config {raw_config}.  Validating...")
            valid_config: Dict[str, Any] = CONFIG_SCHEMA(raw_config)
            return Config(valid_config)
    except FileNotFoundError:
        print(f"Unable to find configuration.  Please create it in {config_path}")
        sys.exit()
