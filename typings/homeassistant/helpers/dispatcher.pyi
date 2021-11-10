"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.loader import bind_hass

"""Helpers for Home Assistant dispatcher & internal component/platform."""
_LOGGER = ...
DATA_DISPATCHER = ...

@bind_hass
def dispatcher_connect(
    hass: HomeAssistant, signal: str, target: Callable[..., None]
) -> Callable[[], None]:
    """Connect a callable function to a signal."""
    ...

@callback
@bind_hass
def async_dispatcher_connect(
    hass: HomeAssistant, signal: str, target: Callable[..., Any]
) -> Callable[[], None]:
    """Connect a callable function to a signal.

    This method must be run in the event loop.
    """
    ...

@bind_hass
def dispatcher_send(hass: HomeAssistant, signal: str, *args: Any) -> None:
    """Send signal and data."""
    ...

@callback
@bind_hass
def async_dispatcher_send(hass: HomeAssistant, signal: str, *args: Any) -> None:
    """Send signal and data.

    This method must be run in the event loop.
    """
    ...
