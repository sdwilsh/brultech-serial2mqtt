"""
This type stub file was generated by pyright.
"""

from collections.abc import Awaitable, Callable

from homeassistant.core import HomeAssistant, callback

"""Helpers to help during startup."""

@callback
def async_at_start(
    hass: HomeAssistant, at_start_cb: Callable[[HomeAssistant], Awaitable]
) -> None:
    """Execute something when Home Assistant is started.

    Will execute it now if Home Assistant is already started.
    """
    ...