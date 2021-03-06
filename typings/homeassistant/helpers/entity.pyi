"""
This type stub file was generated by pyright.
"""

import asyncio
from abc import ABC
from collections.abc import Awaitable, Iterable, Mapping, MutableMapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Final, Literal, TypedDict, final

from homeassistant.core import CALLBACK_TYPE, Context, HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import EntityPlatform
from homeassistant.helpers.typing import StateType
from homeassistant.loader import bind_hass

"""An abstract class for entities."""
_LOGGER = ...
SLOW_UPDATE_WARNING = ...
DATA_ENTITY_SOURCE = ...
SOURCE_CONFIG_ENTRY = ...
SOURCE_PLATFORM_CONFIG = ...
FLOAT_PRECISION = ...
ENTITY_CATEGORIES: Final[list[str]] = ...
ENTITY_CATEGORIES_SCHEMA: Final = ...

@callback
@bind_hass
def entity_sources(hass: HomeAssistant) -> dict[str, dict[str, str]]:
    """Get the entity sources."""
    ...

def generate_entity_id(
    entity_id_format: str,
    name: str | None,
    current_ids: list[str] | None = ...,
    hass: HomeAssistant | None = ...,
) -> str:
    """Generate a unique entity ID based on given entity IDs or used IDs."""
    ...

@callback
def async_generate_entity_id(
    entity_id_format: str,
    name: str | None,
    current_ids: Iterable[str] | None = ...,
    hass: HomeAssistant | None = ...,
) -> str:
    """Generate a unique entity ID based on given entity IDs or used IDs."""
    ...

def get_capability(hass: HomeAssistant, entity_id: str, capability: str) -> Any | None:
    """Get a capability attribute of an entity.

    First try the statemachine, then entity registry.
    """
    ...

def get_device_class(hass: HomeAssistant, entity_id: str) -> str | None:
    """Get device class of an entity.

    First try the statemachine, then entity registry.
    """
    ...

def get_supported_features(hass: HomeAssistant, entity_id: str) -> int:
    """Get supported features for an entity.

    First try the statemachine, then entity registry.
    """
    ...

def get_unit_of_measurement(hass: HomeAssistant, entity_id: str) -> str | None:
    """Get unit of measurement class of an entity.

    First try the statemachine, then entity registry.
    """
    ...

class DeviceInfo(TypedDict, total=False):
    """Entity device information for device registry."""

    configuration_url: str | None
    connections: set[tuple[str, str]]
    default_manufacturer: str
    default_model: str
    default_name: str
    entry_type: str | None
    identifiers: set[tuple[str, str]]
    manufacturer: str | None
    model: str | None
    name: str | None
    suggested_area: str | None
    sw_version: str | None
    via_device: tuple[str, str]
    ...

@dataclass
class EntityDescription:
    """A class that describes Home Assistant entities."""

    key: str
    device_class: str | None = ...
    entity_category: Literal["config", "diagnostic"] | None = ...
    entity_registry_enabled_default: bool = ...
    force_update: bool = ...
    icon: str | None = ...
    name: str | None = ...
    unit_of_measurement: str | None = ...

class Entity(ABC):
    """An abstract class for Home Assistant entities."""

    entity_id: str = ...
    hass: HomeAssistant = ...
    platform: EntityPlatform | None = ...
    entity_description: EntityDescription
    _slow_reported = ...
    _disabled_reported = ...
    _update_staged = ...
    parallel_updates: asyncio.Semaphore | None = ...
    registry_entry: er.RegistryEntry | None = ...
    _on_remove: list[CALLBACK_TYPE] | None = ...
    _context: Context | None = ...
    _context_set: datetime | None = ...
    _added = ...
    _attr_assumed_state: bool = ...
    _attr_attribution: str | None = ...
    _attr_available: bool = ...
    _attr_context_recent_time: timedelta = ...
    _attr_device_class: str | None
    _attr_device_info: DeviceInfo | None = ...
    _attr_entity_category: str | None
    _attr_entity_picture: str | None = ...
    _attr_entity_registry_enabled_default: bool
    _attr_extra_state_attributes: MutableMapping[str, Any]
    _attr_force_update: bool
    _attr_icon: str | None
    _attr_name: str | None
    _attr_should_poll: bool = ...
    _attr_state: StateType = ...
    _attr_supported_features: int | None = ...
    _attr_unique_id: str | None = ...
    _attr_unit_of_measurement: str | None
    @property
    def should_poll(self) -> bool:
        """Return True if entity has to be polled for state.

        False if entity pushes its state to HA.
        """
        ...
    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        ...
    @property
    def name(self) -> str | None:
        """Return the name of the entity."""
        ...
    @property
    def state(self) -> StateType:
        """Return the state of the entity."""
        ...
    @property
    def capability_attributes(self) -> Mapping[str, Any] | None:
        """Return the capability attributes.

        Attributes that explain the capabilities of an entity.

        Implemented by component base class. Convention for attribute names
        is lowercase snake_case.
        """
        ...
    @property
    def state_attributes(self) -> dict[str, Any] | None:
        """Return the state attributes.

        Implemented by component base class, should not be extended by integrations.
        Convention for attribute names is lowercase snake_case.
        """
        ...
    @property
    def device_state_attributes(self) -> Mapping[str, Any] | None:
        """Return entity specific state attributes.

        This method is deprecated, platform classes should implement
        extra_state_attributes instead.
        """
        ...
    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Return entity specific state attributes.

        Implemented by platform classes. Convention for attribute names
        is lowercase snake_case.
        """
        ...
    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device specific attributes.

        Implemented by platform classes.
        """
        ...
    @property
    def device_class(self) -> str | None:
        """Return the class of this device, from component DEVICE_CLASSES."""
        ...
    @property
    def unit_of_measurement(self) -> str | None:
        """Return the unit of measurement of this entity, if any."""
        ...
    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend, if any."""
        ...
    @property
    def entity_picture(self) -> str | None:
        """Return the entity picture to use in the frontend, if any."""
        ...
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        ...
    @property
    def assumed_state(self) -> bool:
        """Return True if unable to access real state of the entity."""
        ...
    @property
    def force_update(self) -> bool:
        """Return True if state updates should be forced.

        If True, a state change will be triggered anytime the state property is
        updated, not just when the value changes.
        """
        ...
    @property
    def supported_features(self) -> int | None:
        """Flag supported features."""
        ...
    @property
    def context_recent_time(self) -> timedelta:
        """Time that a context is considered recent."""
        ...
    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added to the entity registry."""
        ...
    @property
    def attribution(self) -> str | None:
        """Return the attribution."""
        ...
    @property
    def entity_category(self) -> str | None:
        """Return the category of the entity, if any."""
        ...
    @property
    def enabled(self) -> bool:
        """Return if the entity is enabled in the entity registry.

        If an entity is not part of the registry, it cannot be disabled
        and will therefore always be enabled.
        """
        ...
    @callback
    def async_set_context(self, context: Context) -> None:
        """Set the context the entity currently operates under."""
        ...
    async def async_update_ha_state(self, force_refresh: bool = ...) -> None:
        """Update Home Assistant with current state of entity.

        If force_refresh == True will update entity before setting state.

        This method must be run in the event loop.
        """
        ...
    @callback
    def async_write_ha_state(self) -> None:
        """Write the state to the state machine."""
        ...
    def schedule_update_ha_state(self, force_refresh: bool = ...) -> None:
        """Schedule an update ha state change task.

        Scheduling the update avoids executor deadlocks.

        Entity state and attributes are read when the update ha state change
        task is executed.
        If state is changed more than once before the ha state change task has
        been executed, the intermediate state transitions will be missed.
        """
        ...
    @callback
    def async_schedule_update_ha_state(self, force_refresh: bool = ...) -> None:
        """Schedule an update ha state change task.

        This method must be run in the event loop.
        Scheduling the update avoids executor deadlocks.

        Entity state and attributes are read when the update ha state change
        task is executed.
        If state is changed more than once before the ha state change task has
        been executed, the intermediate state transitions will be missed.
        """
        ...
    async def async_device_update(self, warning: bool = ...) -> None:
        """Process 'update' or 'async_update' from entity.

        This method is a coroutine.
        """
        ...
    @callback
    def async_on_remove(self, func: CALLBACK_TYPE) -> None:
        """Add a function to call when entity removed."""
        ...
    async def async_removed_from_registry(self) -> None:
        """Run when entity has been removed from entity registry.

        To be extended by integrations.
        """
        ...
    @callback
    def add_to_platform_start(
        self,
        hass: HomeAssistant,
        platform: EntityPlatform,
        parallel_updates: asyncio.Semaphore | None,
    ) -> None:
        """Start adding an entity to a platform."""
        ...
    @callback
    def add_to_platform_abort(self) -> None:
        """Abort adding an entity to a platform."""
        ...
    async def add_to_platform_finish(self) -> None:
        """Finish adding an entity to a platform."""
        ...
    async def async_remove(self, *, force_remove: bool = ...) -> None:
        """Remove entity from Home Assistant.

        If the entity has a non disabled entry in the entity registry,
        the entity's state will be set to unavailable, in the same way
        as when the entity registry is loaded.

        If the entity doesn't have a non disabled entry in the entity registry,
        or if force_remove=True, its state will be removed.
        """
        ...
    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass.

        To be extended by integrations.
        """
        ...
    async def async_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass.

        To be extended by integrations.
        """
        ...
    async def async_internal_added_to_hass(self) -> None:
        """Run when entity about to be added to hass.

        Not to be extended by integrations.
        """
        ...
    async def async_internal_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass.

        Not to be extended by integrations.
        """
        ...
    def __eq__(self, other: Any) -> bool:
        """Return the comparison."""
        ...
    def __repr__(self) -> str:
        """Return the representation."""
        ...
    async def async_request_call(self, coro: Awaitable) -> None:
        """Process request batched."""
        ...

@dataclass
class ToggleEntityDescription(EntityDescription):
    """A class that describes toggle entities."""

    ...

class ToggleEntity(Entity):
    """An abstract class for entities that can be turned on and off."""

    entity_description: ToggleEntityDescription
    _attr_is_on: bool
    _attr_state: None = ...
    @property
    @final
    def state(self) -> str | None:
        """Return the state."""
        ...
    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        ...
    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        ...
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        ...
    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        ...
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        ...
    def toggle(self, **kwargs: Any) -> None:
        """Toggle the entity."""
        ...
    async def async_toggle(self, **kwargs: Any) -> None:
        """Toggle the entity."""
        ...
