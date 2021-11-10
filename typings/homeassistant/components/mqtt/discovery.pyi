"""
This type stub file was generated by pyright.
"""

from homeassistant.core import HomeAssistant

"""Support for MQTT discovery."""
_LOGGER = ...
TOPIC_MATCHER = ...
SUPPORTED_COMPONENTS = ...
ALREADY_DISCOVERED = ...
PENDING_DISCOVERED = ...
CONFIG_ENTRY_IS_SETUP = ...
DATA_CONFIG_ENTRY_LOCK = ...
DATA_CONFIG_FLOW_LOCK = ...
DISCOVERY_UNSUBSCRIBE = ...
INTEGRATION_UNSUBSCRIBE = ...
MQTT_DISCOVERY_UPDATED = ...
MQTT_DISCOVERY_NEW = ...
MQTT_DISCOVERY_DONE = ...
LAST_DISCOVERY = ...
TOPIC_BASE = ...

def clear_discovery_hash(hass, discovery_hash):  # -> None:
    """Clear entry in ALREADY_DISCOVERED list."""
    ...

def set_discovery_hash(hass, discovery_hash):  # -> None:
    """Clear entry in ALREADY_DISCOVERED list."""
    ...

class MQTTConfig(dict):
    """Dummy class to allow adding attributes."""

    ...

async def async_start(hass: HomeAssistant, discovery_topic, config_entry=...) -> None:
    """Start MQTT Discovery."""
    ...

async def async_stop(hass: HomeAssistant) -> None:
    """Stop MQTT Discovery."""
    ...
