"""
This type stub file was generated by pyright.
"""

import pathlib
from types import ModuleType
from typing import TYPE_CHECKING, Any, TypedDict

from awesomeversion import AwesomeVersion
from homeassistant.core import HomeAssistant

"""
This type stub file was generated by pyright.
"""
if TYPE_CHECKING: ...
CALLABLE_T = ...
_LOGGER = ...
DATA_COMPONENTS = ...
DATA_INTEGRATIONS = ...
DATA_CUSTOM_COMPONENTS = ...
PACKAGE_CUSTOM_COMPONENTS = ...
PACKAGE_BUILTIN = ...
CUSTOM_WARNING = ...
_UNDEF = ...
MAX_LOAD_CONCURRENTLY = ...

class Manifest(TypedDict, total=False):
    """
    Integration manifest.

    Note that none of the attributes are marked Optional here. However, some of them may be optional in manifest.json
    in the sense that they can be omitted altogether. But when present, they should not have null values in it.
    """

    name: str
    disabled: str
    domain: str
    dependencies: list[str]
    after_dependencies: list[str]
    requirements: list[str]
    config_flow: bool
    documentation: str
    issue_tracker: str
    quality_scale: str
    iot_class: str
    mqtt: list[str]
    ssdp: list[dict[str, str]]
    zeroconf: list[str | dict[str, str]]
    dhcp: list[dict[str, str]]
    usb: list[dict[str, str]]
    homekit: dict[str, list[str]]
    is_built_in: bool
    version: str
    codeowners: list[str]
    ...

def manifest_from_legacy_module(domain: str, module: ModuleType) -> Manifest:
    """Generate a manifest from a legacy module."""
    ...

async def async_get_custom_components(hass: HomeAssistant) -> dict[str, Integration]:
    """Return cached list of custom integrations."""
    ...

async def async_get_config_flows(hass: HomeAssistant) -> set[str]:
    """Return cached list of config flows."""
    ...

async def async_get_zeroconf(hass: HomeAssistant) -> dict[str, list[dict[str, str]]]:
    """Return cached list of zeroconf types."""
    ...

async def async_get_dhcp(hass: HomeAssistant) -> list[dict[str, str]]:
    """Return cached list of dhcp types."""
    ...

async def async_get_usb(hass: HomeAssistant) -> list[dict[str, str]]:
    """Return cached list of usb types."""
    ...

async def async_get_homekit(hass: HomeAssistant) -> dict[str, str]:
    """Return cached list of homekit models."""
    ...

async def async_get_ssdp(hass: HomeAssistant) -> dict[str, list[dict[str, str]]]:
    """Return cached list of ssdp mappings."""
    ...

async def async_get_mqtt(hass: HomeAssistant) -> dict[str, list[str]]:
    """Return cached list of MQTT mappings."""
    ...

class Integration:
    """An integration in Home Assistant."""

    @classmethod
    def resolve_from_root(
        cls, hass: HomeAssistant, root_module: ModuleType, domain: str
    ) -> Integration | None:
        """Resolve an integration from a root module."""
        ...
    def __init__(
        self,
        hass: HomeAssistant,
        pkg_path: str,
        file_path: pathlib.Path,
        manifest: Manifest,
    ) -> None:
        """Initialize an integration."""
        ...
    @property
    def name(self) -> str:
        """Return name."""
        ...
    @property
    def disabled(self) -> str | None:
        """Return reason integration is disabled."""
        ...
    @property
    def domain(self) -> str:
        """Return domain."""
        ...
    @property
    def dependencies(self) -> list[str]:
        """Return dependencies."""
        ...
    @property
    def after_dependencies(self) -> list[str]:
        """Return after_dependencies."""
        ...
    @property
    def requirements(self) -> list[str]:
        """Return requirements."""
        ...
    @property
    def config_flow(self) -> bool:
        """Return config_flow."""
        ...
    @property
    def documentation(self) -> str | None:
        """Return documentation."""
        ...
    @property
    def issue_tracker(self) -> str | None:
        """Return issue tracker link."""
        ...
    @property
    def quality_scale(self) -> str | None:
        """Return Integration Quality Scale."""
        ...
    @property
    def iot_class(self) -> str | None:
        """Return the integration IoT Class."""
        ...
    @property
    def mqtt(self) -> list[str] | None:
        """Return Integration MQTT entries."""
        ...
    @property
    def ssdp(self) -> list[dict[str, str]] | None:
        """Return Integration SSDP entries."""
        ...
    @property
    def zeroconf(self) -> list[str | dict[str, str]] | None:
        """Return Integration zeroconf entries."""
        ...
    @property
    def dhcp(self) -> list[dict[str, str]] | None:
        """Return Integration dhcp entries."""
        ...
    @property
    def usb(self) -> list[dict[str, str]] | None:
        """Return Integration usb entries."""
        ...
    @property
    def homekit(self) -> dict[str, list[str]] | None:
        """Return Integration homekit entries."""
        ...
    @property
    def is_built_in(self) -> bool:
        """Test if package is a built-in integration."""
        ...
    @property
    def version(self) -> AwesomeVersion | None:
        """Return the version of the integration."""
        ...
    @property
    def all_dependencies(self) -> set[str]:
        """Return all dependencies including sub-dependencies."""
        ...
    @property
    def all_dependencies_resolved(self) -> bool:
        """Return if all dependencies have been resolved."""
        ...
    async def resolve_dependencies(self) -> bool:
        """Resolve all dependencies."""
        ...
    def get_component(self) -> ModuleType:
        """Return the component."""
        ...
    def get_platform(self, platform_name: str) -> ModuleType:
        """Return a platform for an integration."""
        ...
    def __repr__(self) -> str:
        """Text representation of class."""
        ...

async def async_get_integration(hass: HomeAssistant, domain: str) -> Integration:
    """Get an integration."""
    ...

class LoaderError(Exception):
    """Loader base error."""

    ...

class IntegrationNotFound(LoaderError):
    """Raised when a component is not found."""

    def __init__(self, domain: str) -> None:
        """Initialize a component not found error."""
        ...

class CircularDependency(LoaderError):
    """Raised when a circular dependency is found when resolving components."""

    def __init__(self, from_domain: str, to_domain: str) -> None:
        """Initialize circular dependency error."""
        ...

class ModuleWrapper:
    """Class to wrap a Python module and auto fill in hass argument."""

    def __init__(self, hass: HomeAssistant, module: ModuleType) -> None:
        """Initialize the module wrapper."""
        ...
    def __getattr__(self, attr: str) -> Any:
        """Fetch an attribute."""
        ...

class Components:
    """Helper to load components."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the Components class."""
        ...
    def __getattr__(self, comp_name: str) -> ModuleWrapper:
        """Fetch a component."""
        ...

class Helpers:
    """Helper to load helpers."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the Helpers class."""
        ...
    def __getattr__(self, helper_name: str) -> ModuleWrapper:
        """Fetch a helper."""
        ...

def bind_hass(func: CALLABLE_T) -> CALLABLE_T:
    """Decorate function to indicate that first argument is hass."""
    ...
