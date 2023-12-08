from __future__ import annotations

import logging
from enum import Enum, unique
from typing import Any, Dict

import voluptuous as vol
import voluptuous.validators as validators
from voluptuous.error import Invalid

from brultech_serial2mqtt.config.typing import EmptyConfigDict


@unique
class LogLevel(Enum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG

    @classmethod
    def fromValue(cls, value: str) -> LogLevel:
        if value.upper() == "CRITICAL":
            return LogLevel.CRITICAL
        if value.upper() == "ERROR":
            return LogLevel.ERROR
        if value.upper() == "WARNING":
            return LogLevel.WARNING
        if value.upper() == "INFO":
            return LogLevel.INFO
        if value.upper() == "DEBUG":
            return LogLevel.DEBUG
        raise Invalid(
            f"Must be a valid, named logging level ({', '.join([level.name for level in LogLevel])})"
        )


SCHEMA = vol.Schema(
    {
        vol.Optional("level", default="info"): LogLevel.fromValue,
        vol.Optional("logs", default=EmptyConfigDict): {
            validators.All(str, validators.Length(min=1)): LogLevel.fromValue
        },
    },
)


class LoggingConfig:
    """Logging config."""

    schema = SCHEMA

    def __init__(self, logging_config: Dict[str, Any]):
        self._level = logging_config["level"]
        self._logs = logging_config["logs"]

    @property
    def level(self) -> LogLevel:
        """Return the configured log level."""
        return self._level

    @property
    def logs(self) -> Dict[str, LogLevel]:
        """Return the configured log level for specific libraries."""
        return self._logs
