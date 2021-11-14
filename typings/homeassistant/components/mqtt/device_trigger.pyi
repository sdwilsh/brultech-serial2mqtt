"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from typing import Any

import attr
from homeassistant.components.automation import (
    AutomationActionType,
    AutomationTriggerInfo,
)
from homeassistant.core import CALLBACK_TYPE, HomeAssistant
from homeassistant.helpers.typing import ConfigType

"""Provides device automations for MQTT."""
_LOGGER = ...
CONF_AUTOMATION_TYPE = ...
CONF_DISCOVERY_ID = ...
CONF_SUBTYPE = ...
DEFAULT_ENCODING = ...
DEVICE = ...
MQTT_TRIGGER_BASE = ...
TRIGGER_SCHEMA = ...
TRIGGER_DISCOVERY_SCHEMA = ...
DEVICE_TRIGGERS = ...

@attr.s(slots=True)
class TriggerInstance:
    """Attached trigger settings."""

    action: AutomationActionType = ...
    automation_info: AutomationTriggerInfo = ...
    trigger: Trigger = ...
    remove: CALLBACK_TYPE | None = ...
    async def async_attach_trigger(self):  # -> None:
        """Attach MQTT trigger."""
        ...

@attr.s(slots=True)
class Trigger:
    """Device trigger settings."""

    device_id: str = ...
    discovery_data: dict | None = ...
    hass: HomeAssistant = ...
    payload: str | None = ...
    qos: int | None = ...
    remove_signal: Callable[[], None] | None = ...
    subtype: str = ...
    topic: str | None = ...
    type: str = ...
    value_template: str | None = ...
    trigger_instances: list[TriggerInstance] = ...
    async def add_trigger(self, action, automation_info):  # -> () -> None:
        """Add MQTT trigger."""
        ...
    async def update_trigger(self, config, discovery_hash, remove_signal):  # -> None:
        """Update MQTT device trigger."""
        ...
    def detach_trigger(self):  # -> None:
        """Remove MQTT device trigger."""
        ...

async def async_setup_trigger(hass, config, config_entry, discovery_data):  # -> None:
    """Set up the MQTT device trigger."""
    ...

async def async_device_removed(hass: HomeAssistant, device_id: str):  # -> None:
    """Handle the removal of a device."""
    ...

async def async_get_triggers(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, Any]]:
    """List device triggers for MQTT devices."""
    ...

async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: AutomationActionType,
    automation_info: AutomationTriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    ...