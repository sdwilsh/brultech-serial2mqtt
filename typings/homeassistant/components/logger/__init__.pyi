"""
This type stub file was generated by pyright.
"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.core import callback

"""Support for setting the level of logging for components."""
DOMAIN = ...
SERVICE_SET_DEFAULT_LEVEL = ...
SERVICE_SET_LEVEL = ...
LOGSEVERITY = ...
DEFAULT_LOGSEVERITY = ...
LOGGER_DEFAULT = ...
LOGGER_LOGS = ...
LOGGER_FILTERS = ...
ATTR_LEVEL = ...
_VALID_LOG_LEVEL = ...
SERVICE_SET_DEFAULT_LEVEL_SCHEMA = ...
SERVICE_SET_LEVEL_SCHEMA = ...
CONFIG_SCHEMA = ...

async def async_setup(hass, config):  # -> Literal[True]:
    """Set up the logger component."""
    ...