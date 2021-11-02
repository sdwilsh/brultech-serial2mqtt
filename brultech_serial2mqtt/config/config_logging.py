from __future__ import annotations

import logging
from enum import Enum, unique
from typing import Dict

from voluptuous import All, Invalid, Length, Optional, Schema


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
            f"Must be a valid, named logging level ({', '.join([l.name for l in LogLevel])})"
        )


SCHEMA = Schema(
    {
        Optional("level", default="info"): LogLevel.fromValue,
        Optional("logs", default={}): {All(str, Length(min=1)): LogLevel.fromValue},
    },
)


class LoggingConfig:
    """Logging config."""

    schema = SCHEMA

    def __init__(self, logging_config: dict):
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
