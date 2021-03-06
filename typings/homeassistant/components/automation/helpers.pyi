"""
This type stub file was generated by pyright.
"""

from homeassistant.components import blueprint
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.singleton import singleton

"""Helpers for automation integration."""
DATA_BLUEPRINTS = ...

@singleton(DATA_BLUEPRINTS)
@callback
def async_get_blueprints(hass: HomeAssistant) -> blueprint.DomainBlueprints:
    """Get automation blueprints."""
    ...
