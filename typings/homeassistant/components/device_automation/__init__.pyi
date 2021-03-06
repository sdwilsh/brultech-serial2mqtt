"""
This type stub file was generated by pyright.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Iterable, Mapping
from functools import wraps
from types import ModuleType
from typing import Any, NamedTuple

import voluptuous as vol
import voluptuous_serialize
from homeassistant.components import websocket_api
from homeassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.loader import IntegrationNotFound, bind_hass
from homeassistant.requirements import async_get_integration_with_requirements

from .exceptions import DeviceNotFound, InvalidDeviceAutomationConfig

"""Helpers for device automations."""
DOMAIN = ...
DEVICE_TRIGGER_BASE_SCHEMA = ...

class DeviceAutomationDetails(NamedTuple):
    """Details for device automation."""

    section: str
    get_automations_func: str
    get_capabilities_func: str
    ...

TYPES = ...

@bind_hass
async def async_get_device_automations(
    hass: HomeAssistant, automation_type: str, device_ids: Iterable[str] | None = ...
) -> Mapping[str, Any]:
    """Return all the device automations for a type optionally limited to specific device ids."""
    ...

async def async_setup(hass, config):  # -> Literal[True]:
    """Set up device automation."""
    ...

async def async_get_device_automation_platform(
    hass: HomeAssistant, domain: str, automation_type: str
) -> ModuleType:
    """Load device automation platform for integration.

    Throws InvalidDeviceAutomationConfig if the integration is not found or does not support device automation.
    """
    ...

def handle_device_errors(
    func,
):  # -> (hass: Unknown, connection: Unknown, msg: Unknown) -> Coroutine[Any, Any, None]:
    """Handle device automation errors."""
    ...

@websocket_api.websocket_command(
    {
        vol.Required("type"): "device_automation/action/list",
        vol.Required("device_id"): str,
    }
)
@websocket_api.async_response
@handle_device_errors
async def websocket_device_automation_list_actions(hass, connection, msg):  # -> None:
    """Handle request for device actions."""
    ...

@websocket_api.websocket_command(
    {
        vol.Required("type"): "device_automation/condition/list",
        vol.Required("device_id"): str,
    }
)
@websocket_api.async_response
@handle_device_errors
async def websocket_device_automation_list_conditions(
    hass, connection, msg
):  # -> None:
    """Handle request for device conditions."""
    ...

@websocket_api.websocket_command(
    {
        vol.Required("type"): "device_automation/trigger/list",
        vol.Required("device_id"): str,
    }
)
@websocket_api.async_response
@handle_device_errors
async def websocket_device_automation_list_triggers(hass, connection, msg):  # -> None:
    """Handle request for device triggers."""
    ...

@websocket_api.websocket_command(
    {
        vol.Required("type"): "device_automation/action/capabilities",
        vol.Required("action"): dict,
    }
)
@websocket_api.async_response
@handle_device_errors
async def websocket_device_automation_get_action_capabilities(
    hass, connection, msg
):  # -> None:
    """Handle request for device action capabilities."""
    ...

@websocket_api.websocket_command(
    {
        vol.Required("type"): "device_automation/condition/capabilities",
        vol.Required("condition"): cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
            {}, extra=vol.ALLOW_EXTRA
        ),
    }
)
@websocket_api.async_response
@handle_device_errors
async def websocket_device_automation_get_condition_capabilities(
    hass, connection, msg
):  # -> None:
    """Handle request for device condition capabilities."""
    ...

@websocket_api.websocket_command(
    {
        vol.Required("type"): "device_automation/trigger/capabilities",
        vol.Required("trigger"): DEVICE_TRIGGER_BASE_SCHEMA.extend(
            {}, extra=vol.ALLOW_EXTRA
        ),
    }
)
@websocket_api.async_response
@handle_device_errors
async def websocket_device_automation_get_trigger_capabilities(
    hass, connection, msg
):  # -> None:
    """Handle request for device trigger capabilities."""
    ...
