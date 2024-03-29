"""
This type stub file was generated by pyright.
"""

import dataclasses
import voluptuous as vol
from collections.abc import Awaitable, Callable, Coroutine, Iterable
from typing import Any, TYPE_CHECKING, TypeVar, TypedDict
from homeassistant.core import (
    Context,
    EntityServiceResponse,
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    callback,
)
from homeassistant.loader import bind_hass
from .typing import ConfigType, TemplateVarsType
from .entity import Entity
from .entity_platform import EntityPlatform

"""Service calling related helpers."""
if TYPE_CHECKING:
    _EntityT = TypeVar("_EntityT", bound=Entity)
CONF_SERVICE_ENTITY_ID = ...
_LOGGER = ...
SERVICE_DESCRIPTION_CACHE = ...
ALL_SERVICE_DESCRIPTIONS_CACHE = ...

def validate_attribute_option(attribute_option: str) -> Any:
    """Validate attribute option."""
    ...

def validate_supported_feature(supported_feature: str) -> Any:
    """Validate supported feature."""
    ...

_FIELD_SCHEMA = ...
_SERVICE_SCHEMA = ...
_SERVICES_SCHEMA = ...

class ServiceParams(TypedDict):
    """Type for service call parameters."""

    domain: str
    service: str
    service_data: dict[str, Any]
    target: dict | None
    ...

class ServiceTargetSelector:
    """Class to hold a target selector for a service."""
    def __init__(self, service_call: ServiceCall) -> None:
        """Extract ids from service call data."""
        ...

    @property
    def has_any_selector(self) -> bool:
        """Determine if any selectors are present."""
        ...

@dataclasses.dataclass(slots=True)
class SelectedEntities:
    """Class to hold the selected entities."""

    referenced: set[str] = ...
    indirectly_referenced: set[str] = ...
    missing_devices: set[str] = ...
    missing_areas: set[str] = ...
    referenced_devices: set[str] = ...
    def log_missing(self, missing_entities: set[str]) -> None:
        """Log about missing items."""
        ...

@bind_hass
def call_from_config(
    hass: HomeAssistant,
    config: ConfigType,
    blocking: bool = ...,
    variables: TemplateVarsType = ...,
    validate_config: bool = ...,
) -> None:
    """Call a service based on a config hash."""
    ...

@bind_hass
async def async_call_from_config(
    hass: HomeAssistant,
    config: ConfigType,
    blocking: bool = ...,
    variables: TemplateVarsType = ...,
    validate_config: bool = ...,
    context: Context | None = ...,
) -> None:
    """Call a service based on a config hash."""
    ...

@callback
@bind_hass
def async_prepare_call_from_config(
    hass: HomeAssistant,
    config: ConfigType,
    variables: TemplateVarsType = ...,
    validate_config: bool = ...,
) -> ServiceParams:
    """Prepare to call a service based on a config hash."""
    ...

@bind_hass
def extract_entity_ids(
    hass: HomeAssistant, service_call: ServiceCall, expand_group: bool = ...
) -> set[str]:
    """Extract a list of entity ids from a service call.

    Will convert group entity ids to the entity ids it represents.
    """
    ...

@bind_hass
async def async_extract_entities(
    hass: HomeAssistant,
    entities: Iterable[_EntityT],
    service_call: ServiceCall,
    expand_group: bool = ...,
) -> list[_EntityT]:
    """Extract a list of entity objects from a service call.

    Will convert group entity ids to the entity ids it represents.
    """
    ...

@bind_hass
async def async_extract_entity_ids(
    hass: HomeAssistant, service_call: ServiceCall, expand_group: bool = ...
) -> set[str]:
    """Extract a set of entity ids from a service call.

    Will convert group entity ids to the entity ids it represents.
    """
    ...

@bind_hass
def async_extract_referenced_entity_ids(
    hass: HomeAssistant, service_call: ServiceCall, expand_group: bool = ...
) -> SelectedEntities:
    """Extract referenced entity IDs from a service call."""
    ...

@bind_hass
async def async_extract_config_entry_ids(
    hass: HomeAssistant, service_call: ServiceCall, expand_group: bool = ...
) -> set:
    """Extract referenced config entry ids from a service call."""
    ...

@bind_hass
async def async_get_all_descriptions(hass: HomeAssistant) -> dict[str, dict[str, Any]]:
    """Return descriptions (i.e. user documentation) for all service calls."""
    ...

@callback
def remove_entity_service_fields(call: ServiceCall) -> dict[Any, Any]:
    """Remove entity service fields."""
    ...

@callback
@bind_hass
def async_set_service_schema(
    hass: HomeAssistant, domain: str, service: str, schema: dict[str, Any]
) -> None:
    """Register a description for a service."""
    ...

@bind_hass
async def entity_service_call(
    hass: HomeAssistant,
    platforms: Iterable[EntityPlatform],
    func: str | Callable[..., Coroutine[Any, Any, ServiceResponse]],
    call: ServiceCall,
    required_features: Iterable[int] | None = ...,
) -> EntityServiceResponse | None:
    """Handle an entity service call.

    Calls all platforms simultaneously.
    """
    ...

@bind_hass
@callback
def async_register_admin_service(
    hass: HomeAssistant,
    domain: str,
    service: str,
    service_func: Callable[[ServiceCall], Awaitable[None] | None],
    schema: vol.Schema = ...,
) -> None:
    """Register a service that requires admin access."""
    ...

@bind_hass
@callback
def verify_domain_control(
    hass: HomeAssistant, domain: str
) -> Callable[[Callable[[ServiceCall], Any]], Callable[[ServiceCall], Any]]:
    """Ensure permission to access any entity under domain in service call."""
    ...

class ReloadServiceHelper:
    """Helper for reload services to minimize unnecessary reloads."""
    def __init__(self, service_func: Callable[[ServiceCall], Awaitable]) -> None:
        """Initialize ReloadServiceHelper."""
        ...

    async def execute_service(self, service_call: ServiceCall) -> None:
        """Execute the service.

        If a previous reload task if currently in progress, wait for it to finish first.
        Once the previous reload task has finished, one of the waiting tasks will be
        assigned to execute the reload, the others will wait for the reload to finish.
        """
        ...
