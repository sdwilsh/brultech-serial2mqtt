"""
This type stub file was generated by pyright.
"""

from collections.abc import Iterable
from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.loader import Integration

"""Module to handle installing requirements."""
PIP_TIMEOUT = ...
MAX_INSTALL_FAILURES = ...
DATA_PIP_LOCK = ...
DATA_PKG_CACHE = ...
DATA_INTEGRATIONS_WITH_REQS = ...
DATA_INSTALL_FAILURE_HISTORY = ...
CONSTRAINT_FILE = ...
DISCOVERY_INTEGRATIONS: dict[str, Iterable[str]] = ...
_LOGGER = ...

class RequirementsNotFound(HomeAssistantError):
    """Raised when a component is not found."""

    def __init__(self, domain: str, requirements: list[str]) -> None:
        """Initialize a component not found error."""
        ...

async def async_get_integration_with_requirements(
    hass: HomeAssistant, domain: str, done: set[str] | None = ...
) -> Integration:
    """Get an integration with all requirements installed, including the dependencies.

    This can raise IntegrationNotFound if manifest or integration
    is invalid, RequirementNotFound if there was some type of
    failure to install requirements.
    """
    ...

@callback
def async_clear_install_history(hass: HomeAssistant) -> None:
    """Forget the install history."""
    ...

async def async_process_requirements(
    hass: HomeAssistant, name: str, requirements: list[str]
) -> None:
    """Install the requirements for a component or platform.

    This method is a coroutine. It will raise RequirementsNotFound
    if an requirement can't be satisfied.
    """
    ...

def pip_kwargs(config_dir: str | None) -> dict[str, Any]:
    """Return keyword arguments for PIP install."""
    ...
