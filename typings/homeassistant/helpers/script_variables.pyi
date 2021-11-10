"""
This type stub file was generated by pyright.
"""

from collections.abc import Mapping
from typing import Any

from homeassistant.core import HomeAssistant, callback

"""Script variables."""

class ScriptVariables:
    """Class to hold and render script variables."""

    def __init__(self, variables: dict[str, Any]) -> None:
        """Initialize script variables."""
        ...
    @callback
    def async_render(
        self,
        hass: HomeAssistant,
        run_variables: Mapping[str, Any] | None,
        *,
        render_as_defaults: bool = ...,
        limited: bool = ...
    ) -> dict[str, Any]:
        """Render script variables.

        The run variables are used to compute the static variables.

        If `render_as_defaults` is True, the run variables will not be overridden.

        """
        ...
    def as_dict(self) -> dict[str, Any]:
        """Return dict version of this class."""
        ...
