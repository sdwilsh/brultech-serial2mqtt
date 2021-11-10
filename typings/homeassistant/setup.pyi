"""
This type stub file was generated by pyright.
"""

import contextlib
from collections.abc import Awaitable, Callable, Generator, Iterable
from types import ModuleType

from homeassistant import core, loader
from homeassistant.helpers.typing import ConfigType

"""All methods needed to bootstrap a Home Assistant instance."""
_LOGGER = ...
ATTR_COMPONENT = ...
BASE_PLATFORMS = ...
DATA_SETUP_DONE = ...
DATA_SETUP_STARTED = ...
DATA_SETUP_TIME = ...
DATA_SETUP = ...
DATA_DEPS_REQS = ...
SLOW_SETUP_WARNING = ...
SLOW_SETUP_MAX_WAIT = ...

@core.callback
def async_set_domains_to_be_loaded(hass: core.HomeAssistant, domains: set[str]) -> None:
    """Set domains that are going to be loaded from the config.

    This will allow us to properly handle after_dependencies.
    """
    ...

def setup_component(hass: core.HomeAssistant, domain: str, config: ConfigType) -> bool:
    """Set up a component and all its dependencies."""
    ...

async def async_setup_component(
    hass: core.HomeAssistant, domain: str, config: ConfigType
) -> bool:
    """Set up a component and all its dependencies.

    This method is a coroutine.
    """
    ...

async def async_prepare_setup_platform(
    hass: core.HomeAssistant, hass_config: ConfigType, domain: str, platform_name: str
) -> ModuleType | None:
    """Load a platform and makes sure dependencies are setup.

    This method is a coroutine.
    """
    ...

async def async_process_deps_reqs(
    hass: core.HomeAssistant, config: ConfigType, integration: loader.Integration
) -> None:
    """Process all dependencies and requirements for a module.

    Module is a Python module of either a component or platform.
    """
    ...

@core.callback
def async_when_setup(
    hass: core.HomeAssistant,
    component: str,
    when_setup_cb: Callable[[core.HomeAssistant, str], Awaitable[None]],
) -> None:
    """Call a method when a component is setup."""
    ...

@core.callback
def async_when_setup_or_start(
    hass: core.HomeAssistant,
    component: str,
    when_setup_cb: Callable[[core.HomeAssistant, str], Awaitable[None]],
) -> None:
    """Call a method when a component is setup or state is fired."""
    ...

@core.callback
def async_get_loaded_integrations(hass: core.HomeAssistant) -> set[str]:
    """Return the complete list of loaded integrations."""
    ...

@contextlib.contextmanager
def async_start_setup(
    hass: core.HomeAssistant, components: Iterable[str]
) -> Generator[None, None, None]:
    """Keep track of when setup starts and finishes."""
    ...
