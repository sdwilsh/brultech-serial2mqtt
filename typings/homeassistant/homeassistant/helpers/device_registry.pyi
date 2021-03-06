"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING, NamedTuple

import attr
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.loader import bind_hass

from . import entity_registry
from .typing import UndefinedType

"""
This type stub file was generated by pyright.
"""
if TYPE_CHECKING: ...
_LOGGER = ...
DATA_REGISTRY = ...
EVENT_DEVICE_REGISTRY_UPDATED = ...
STORAGE_KEY = ...
STORAGE_VERSION = ...
SAVE_DELAY = ...
CLEANUP_DELAY = ...
CONNECTION_NETWORK_MAC = ...
CONNECTION_UPNP = ...
CONNECTION_ZIGBEE = ...
DISABLED_CONFIG_ENTRY = ...
DISABLED_INTEGRATION = ...
DISABLED_USER = ...
ORPHANED_DEVICE_KEEP_SECONDS = ...

class _DeviceIndex(NamedTuple):
    identifiers: dict[tuple[str, str], str]
    connections: dict[tuple[str, str], str]
    ...

@attr.s(slots=True, frozen=True)
class DeviceEntry:
    """Device Registry Entry."""

    area_id: str | None = ...
    config_entries: set[str] = ...
    configuration_url: str | None = ...
    connections: set[tuple[str, str]] = ...
    disabled_by: str | None = ...
    entry_type: str | None = ...
    id: str = ...
    identifiers: set[tuple[str, str]] = ...
    manufacturer: str | None = ...
    model: str | None = ...
    name_by_user: str | None = ...
    name: str | None = ...
    suggested_area: str | None = ...
    sw_version: str | None = ...
    via_device_id: str | None = ...
    is_new: bool = ...
    @property
    def disabled(self) -> bool:
        """Return if entry is disabled."""
        ...

@attr.s(slots=True, frozen=True)
class DeletedDeviceEntry:
    """Deleted Device Registry Entry."""

    config_entries: set[str] = ...
    connections: set[tuple[str, str]] = ...
    identifiers: set[tuple[str, str]] = ...
    id: str = ...
    orphaned_timestamp: float | None = ...
    def to_device_entry(
        self,
        config_entry_id: str,
        connections: set[tuple[str, str]],
        identifiers: set[tuple[str, str]],
    ) -> DeviceEntry:
        """Create DeviceEntry from DeletedDeviceEntry."""
        ...

def format_mac(mac: str) -> str:
    """Format the mac address string for entry into dev reg."""
    ...

class DeviceRegistry:
    """Class to hold a registry of devices."""

    devices: dict[str, DeviceEntry]
    deleted_devices: dict[str, DeletedDeviceEntry]
    _registered_index: _DeviceIndex
    _deleted_index: _DeviceIndex
    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the device registry."""
        ...
    @callback
    def async_get(self, device_id: str) -> DeviceEntry | None:
        """Get device."""
        ...
    @callback
    def async_get_device(
        self,
        identifiers: set[tuple[str, str]],
        connections: set[tuple[str, str]] | None = ...,
    ) -> DeviceEntry | None:
        """Check if device is registered."""
        ...
    @callback
    def async_get_or_create(
        self,
        *,
        config_entry_id: str,
        configuration_url: str | None | UndefinedType = ...,
        connections: set[tuple[str, str]] | None = ...,
        default_manufacturer: str | None | UndefinedType = ...,
        default_model: str | None | UndefinedType = ...,
        default_name: str | None | UndefinedType = ...,
        disabled_by: str | None | UndefinedType = ...,
        entry_type: str | None | UndefinedType = ...,
        identifiers: set[tuple[str, str]] | None = ...,
        manufacturer: str | None | UndefinedType = ...,
        model: str | None | UndefinedType = ...,
        name: str | None | UndefinedType = ...,
        suggested_area: str | None | UndefinedType = ...,
        sw_version: str | None | UndefinedType = ...,
        via_device: tuple[str, str] | None = ...
    ) -> DeviceEntry:
        """Get device. Create if it doesn't exist."""
        ...
    @callback
    def async_update_device(
        self,
        device_id: str,
        *,
        add_config_entry_id: str | UndefinedType = ...,
        area_id: str | None | UndefinedType = ...,
        configuration_url: str | None | UndefinedType = ...,
        disabled_by: str | None | UndefinedType = ...,
        manufacturer: str | None | UndefinedType = ...,
        model: str | None | UndefinedType = ...,
        name_by_user: str | None | UndefinedType = ...,
        name: str | None | UndefinedType = ...,
        new_identifiers: set[tuple[str, str]] | UndefinedType = ...,
        remove_config_entry_id: str | UndefinedType = ...,
        suggested_area: str | None | UndefinedType = ...,
        sw_version: str | None | UndefinedType = ...,
        via_device_id: str | None | UndefinedType = ...
    ) -> DeviceEntry | None:
        """Update properties of a device."""
        ...
    @callback
    def async_remove_device(self, device_id: str) -> None:
        """Remove a device from the device registry."""
        ...
    async def async_load(self) -> None:
        """Load the device registry."""
        ...
    @callback
    def async_schedule_save(self) -> None:
        """Schedule saving the device registry."""
        ...
    @callback
    def async_clear_config_entry(self, config_entry_id: str) -> None:
        """Clear config entry from registry entries."""
        ...
    @callback
    def async_purge_expired_orphaned_devices(self) -> None:
        """Purge expired orphaned devices from the registry.

        We need to purge these periodically to avoid the database
        growing without bound.
        """
        ...
    @callback
    def async_clear_area_id(self, area_id: str) -> None:
        """Clear area id from registry entries."""
        ...

@callback
def async_get(hass: HomeAssistant) -> DeviceRegistry:
    """Get device registry."""
    ...

async def async_load(hass: HomeAssistant) -> None:
    """Load device registry."""
    ...

@bind_hass
async def async_get_registry(hass: HomeAssistant) -> DeviceRegistry:
    """Get device registry.

    This is deprecated and will be removed in the future. Use async_get instead.
    """
    ...

@callback
def async_entries_for_area(registry: DeviceRegistry, area_id: str) -> list[DeviceEntry]:
    """Return entries that match an area."""
    ...

@callback
def async_entries_for_config_entry(
    registry: DeviceRegistry, config_entry_id: str
) -> list[DeviceEntry]:
    """Return entries that match a config entry."""
    ...

@callback
def async_config_entry_disabled_by_changed(
    registry: DeviceRegistry, config_entry: ConfigEntry
) -> None:
    """Handle a config entry being disabled or enabled.

    Disable devices in the registry that are associated with a config entry when
    the config entry is disabled, enable devices in the registry that are associated
    with a config entry when the config entry is enabled and the devices are marked
    DISABLED_CONFIG_ENTRY.
    Only disable a device if all associated config entries are disabled.
    """
    ...

@callback
def async_cleanup(
    hass: HomeAssistant,
    dev_reg: DeviceRegistry,
    ent_reg: entity_registry.EntityRegistry,
) -> None:
    """Clean up device registry."""
    ...

@callback
def async_setup_cleanup(hass: HomeAssistant, dev_reg: DeviceRegistry) -> None:
    """Clean up device registry when entities removed."""
    ...
