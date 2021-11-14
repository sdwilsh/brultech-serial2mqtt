"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from typing import Any, TypedDict

from homeassistant import core
from homeassistant.core import CALLBACK_TYPE
from homeassistant.loader import bind_hass

from .typing import ConfigType, DiscoveryInfoType

"""Helper methods to help with platform discovery.

There are two different types of discoveries that can be fired/listened for.
 - listen/discover is for services. These are targeted at a component.
 - listen_platform/discover_platform is for platforms. These are used by
   components to allow discovery of their platforms.
"""
SIGNAL_PLATFORM_DISCOVERED = ...
EVENT_LOAD_PLATFORM = ...
ATTR_PLATFORM = ...
ATTR_DISCOVERED = ...

class DiscoveryDict(TypedDict):
    """Discovery data."""

    service: str
    platform: str | None
    discovered: DiscoveryInfoType | None
    ...

@core.callback
@bind_hass
def async_listen(
    hass: core.HomeAssistant, service: str, callback: CALLBACK_TYPE
) -> None:
    """Set up listener for discovery of specific service.

    Service can be a string or a list/tuple.
    """
    ...

@bind_hass
def discover(
    hass: core.HomeAssistant,
    service: str,
    discovered: DiscoveryInfoType,
    component: str,
    hass_config: ConfigType,
) -> None:
    """Fire discovery event. Can ensure a component is loaded."""
    ...

@bind_hass
async def async_discover(
    hass: core.HomeAssistant,
    service: str,
    discovered: DiscoveryInfoType | None,
    component: str | None,
    hass_config: ConfigType,
) -> None:
    """Fire discovery event. Can ensure a component is loaded."""
    ...

@bind_hass
def async_listen_platform(
    hass: core.HomeAssistant,
    component: str,
    callback: Callable[[str, dict[str, Any] | None], Any],
) -> None:
    """Register a platform loader listener.

    This method must be run in the event loop.
    """
    ...

@bind_hass
def load_platform(
    hass: core.HomeAssistant,
    component: str,
    platform: str,
    discovered: DiscoveryInfoType,
    hass_config: ConfigType,
) -> None:
    """Load a component and platform dynamically."""
    ...

@bind_hass
async def async_load_platform(
    hass: core.HomeAssistant,
    component: str,
    platform: str,
    discovered: DiscoveryInfoType,
    hass_config: ConfigType,
) -> None:
    """Load a component and platform dynamically.

    Use `async_listen_platform` to register a callback for these events.

    Warning: Do not await this inside a setup method to avoid a dead lock.
    Use `hass.async_create_task(async_load_platform(..))` instead.
    """
    ...