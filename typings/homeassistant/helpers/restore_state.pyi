"""
This type stub file was generated by pyright.
"""

from datetime import datetime
from typing import Any

from homeassistant.core import HomeAssistant, State, callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.singleton import singleton

"""Support for restoring entity states on startup."""
DATA_RESTORE_STATE_TASK = ...
_LOGGER = ...
STORAGE_KEY = ...
STORAGE_VERSION = ...
STATE_DUMP_INTERVAL = ...
STATE_EXPIRATION = ...

class StoredState:
    """Object to represent a stored state."""

    def __init__(self, state: State, last_seen: datetime) -> None:
        """Initialize a new stored state."""
        ...
    def as_dict(self) -> dict[str, Any]:
        """Return a dict representation of the stored state."""
        ...
    @classmethod
    def from_dict(cls, json_dict: dict) -> StoredState:
        """Initialize a stored state from a dict."""
        ...

class RestoreStateData:
    """Helper class for managing the helper saved data."""

    @staticmethod
    @singleton(DATA_RESTORE_STATE_TASK)
    async def async_get_instance(hass: HomeAssistant) -> RestoreStateData:
        """Get the singleton instance of this data helper."""
        ...
    @classmethod
    async def async_save_persistent_states(cls, hass: HomeAssistant) -> None:
        """Dump states now."""
        ...
    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the restore state data class."""
        ...
    @callback
    def async_get_stored_states(self) -> list[StoredState]:
        """Get the set of states which should be stored.

        This includes the states of all registered entities, as well as the
        stored states from the previous run, which have not been created as
        entities on this run, and have not expired.
        """
        ...
    async def async_dump_states(self) -> None:
        """Save the current state machine to storage."""
        ...
    @callback
    def async_setup_dump(self, *args: Any) -> None:
        """Set up the restore state listeners."""
        ...
    @callback
    def async_restore_entity_added(self, entity_id: str) -> None:
        """Store this entity's state when hass is shutdown."""
        ...
    @callback
    def async_restore_entity_removed(self, entity_id: str) -> None:
        """Unregister this entity from saving state."""
        ...

class RestoreEntity(Entity):
    """Mixin class for restoring previous entity state."""

    async def async_internal_added_to_hass(self) -> None:
        """Register this entity as a restorable entity."""
        ...
    async def async_internal_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass."""
        ...
    async def async_get_last_state(self) -> State | None:
        """Get the entity state from the previous run."""
        ...
