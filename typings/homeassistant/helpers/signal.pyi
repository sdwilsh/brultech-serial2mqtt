"""
This type stub file was generated by pyright.
"""

from homeassistant.core import HomeAssistant, callback
from homeassistant.loader import bind_hass

"""Signal handling related helpers."""
_LOGGER = ...

@callback
@bind_hass
def async_register_signal_handling(hass: HomeAssistant) -> None:
    """Register system signal handler for core."""
    ...
