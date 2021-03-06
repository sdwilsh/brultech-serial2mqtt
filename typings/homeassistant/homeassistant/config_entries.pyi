"""
This type stub file was generated by pyright.
"""

from collections.abc import Iterable, Mapping
from contextvars import ContextVar
from enum import Enum
from typing import Any, Callable

from homeassistant import data_entry_flow, loader
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType, UndefinedType

"""
This type stub file was generated by pyright.
"""
_LOGGER = ...
SOURCE_DISCOVERY = ...
SOURCE_HASSIO = ...
SOURCE_HOMEKIT = ...
SOURCE_IMPORT = ...
SOURCE_INTEGRATION_DISCOVERY = ...
SOURCE_MQTT = ...
SOURCE_SSDP = ...
SOURCE_USB = ...
SOURCE_USER = ...
SOURCE_ZEROCONF = ...
SOURCE_DHCP = ...
SOURCE_IGNORE = ...
SOURCE_UNIGNORE = ...
SOURCE_REAUTH = ...
HANDLERS = ...
STORAGE_KEY = ...
STORAGE_VERSION = ...
PATH_CONFIG = ...
SAVE_DELAY = ...

class ConfigEntryState(Enum):
    """Config entry state."""

    LOADED = ...
    SETUP_ERROR = ...
    MIGRATION_ERROR = ...
    SETUP_RETRY = ...
    NOT_LOADED = ...
    FAILED_UNLOAD = ...
    _recoverable: bool
    def __new__(cls: type[object], value: str, recoverable: bool) -> ConfigEntryState:
        """Create new ConfigEntryState."""
        ...
    @property
    def recoverable(self) -> bool:
        """Get if the state is recoverable."""
        ...

DEFAULT_DISCOVERY_UNIQUE_ID = ...
DISCOVERY_NOTIFICATION_ID = ...
DISCOVERY_SOURCES = ...
RECONFIGURE_NOTIFICATION_ID = ...
EVENT_FLOW_DISCOVERED = ...
DISABLED_USER = ...
RELOAD_AFTER_UPDATE_DELAY = ...
CONN_CLASS_CLOUD_PUSH = ...
CONN_CLASS_CLOUD_POLL = ...
CONN_CLASS_LOCAL_PUSH = ...
CONN_CLASS_LOCAL_POLL = ...
CONN_CLASS_ASSUMED = ...
CONN_CLASS_UNKNOWN = ...

class ConfigError(HomeAssistantError):
    """Error while configuring an account."""

    ...

class UnknownEntry(ConfigError):
    """Unknown entry specified."""

    ...

class OperationNotAllowed(ConfigError):
    """Raised when a config entry operation is not allowed."""

    ...

UpdateListenerType = Callable[[HomeAssistant, "ConfigEntry"], Any]

class ConfigEntry:
    """Hold a configuration entry."""

    __slots__ = ...
    def __init__(
        self,
        version: int,
        domain: str,
        title: str,
        data: Mapping[str, Any],
        source: str,
        pref_disable_new_entities: bool | None = ...,
        pref_disable_polling: bool | None = ...,
        options: Mapping[str, Any] | None = ...,
        unique_id: str | None = ...,
        entry_id: str | None = ...,
        state: ConfigEntryState = ...,
        disabled_by: str | None = ...,
    ) -> None:
        """Initialize a config entry."""
        ...
    async def async_setup(
        self,
        hass: HomeAssistant,
        *,
        integration: loader.Integration | None = ...,
        tries: int = ...
    ) -> None:
        """Set up an entry."""
        ...
    async def async_shutdown(self) -> None:
        """Call when Home Assistant is stopping."""
        ...
    @callback
    def async_cancel_retry_setup(self) -> None:
        """Cancel retry setup."""
        ...
    async def async_unload(
        self, hass: HomeAssistant, *, integration: loader.Integration | None = ...
    ) -> bool:
        """Unload an entry.

        Returns if unload is possible and was successful.
        """
        ...
    async def async_remove(self, hass: HomeAssistant) -> None:
        """Invoke remove callback on component."""
        ...
    async def async_migrate(self, hass: HomeAssistant) -> bool:
        """Migrate an entry.

        Returns True if config entry is up-to-date or has been migrated.
        """
        ...
    def add_update_listener(self, listener: UpdateListenerType) -> CALLBACK_TYPE:
        """Listen for when entry is updated.

        Returns function to unlisten.
        """
        ...
    def as_dict(self) -> dict[str, Any]:
        """Return dictionary version of this entry."""
        ...
    @callback
    def async_on_unload(self, func: CALLBACK_TYPE) -> None:
        """Add a function to call when config entry is unloaded."""
        ...
    @callback
    def async_start_reauth(self, hass: HomeAssistant) -> None:
        """Start a reauth flow."""
        ...

current_entry: ContextVar[ConfigEntry | None] = ...

class ConfigEntriesFlowManager(data_entry_flow.FlowManager):
    """Manage all the config entry flows that are in progress."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entries: ConfigEntries,
        hass_config: ConfigType,
    ) -> None:
        """Initialize the config entry flow manager."""
        ...
    async def async_finish_flow(
        self, flow: data_entry_flow.FlowHandler, result: data_entry_flow.FlowResult
    ) -> data_entry_flow.FlowResult:
        """Finish a config flow and add an entry."""
        ...
    async def async_create_flow(
        self, handler_key: Any, *, context: dict | None = ..., data: Any = ...
    ) -> ConfigFlow:
        """Create a flow for specified handler.

        Handler key is the domain of the component that we want to set up.
        """
        ...
    async def async_post_init(
        self, flow: data_entry_flow.FlowHandler, result: data_entry_flow.FlowResult
    ) -> None:
        """After a flow is initialised trigger new flow notifications."""
        ...

class ConfigEntries:
    """Manage the configuration entries.

    An instance of this object is available via `hass.config_entries`.
    """

    def __init__(self, hass: HomeAssistant, hass_config: ConfigType) -> None:
        """Initialize the entry manager."""
        ...
    @callback
    def async_domains(
        self, include_ignore: bool = ..., include_disabled: bool = ...
    ) -> list[str]:
        """Return domains for which we have entries."""
        ...
    @callback
    def async_get_entry(self, entry_id: str) -> ConfigEntry | None:
        """Return entry with matching entry_id."""
        ...
    @callback
    def async_entries(self, domain: str | None = ...) -> list[ConfigEntry]:
        """Return all entries or entries for a specific domain."""
        ...
    async def async_add(self, entry: ConfigEntry) -> None:
        """Add and setup an entry."""
        ...
    async def async_remove(self, entry_id: str) -> dict[str, Any]:
        """Remove an entry."""
        ...
    async def async_initialize(self) -> None:
        """Initialize config entry config."""
        ...
    async def async_setup(self, entry_id: str) -> bool:
        """Set up a config entry.

        Return True if entry has been successfully loaded.
        """
        ...
    async def async_unload(self, entry_id: str) -> bool:
        """Unload a config entry."""
        ...
    async def async_reload(self, entry_id: str) -> bool:
        """Reload an entry.

        If an entry was not loaded, will just load.
        """
        ...
    async def async_set_disabled_by(
        self, entry_id: str, disabled_by: str | None
    ) -> bool:
        """Disable an entry.

        If disabled_by is changed, the config entry will be reloaded.
        """
        ...
    @callback
    def async_update_entry(
        self,
        entry: ConfigEntry,
        *,
        unique_id: str | None | UndefinedType = ...,
        title: str | UndefinedType = ...,
        data: dict | UndefinedType = ...,
        options: Mapping[str, Any] | UndefinedType = ...,
        pref_disable_new_entities: bool | UndefinedType = ...,
        pref_disable_polling: bool | UndefinedType = ...
    ) -> bool:
        """Update a config entry.

        If the entry was changed, the update_listeners are
        fired and this function returns True

        If the entry was not changed, the update_listeners are
        not fired and this function returns False
        """
        ...
    @callback
    def async_setup_platforms(
        self, entry: ConfigEntry, platforms: Iterable[str]
    ) -> None:
        """Forward the setup of an entry to platforms."""
        ...
    async def async_forward_entry_setup(self, entry: ConfigEntry, domain: str) -> bool:
        """Forward the setup of an entry to a different component.

        By default an entry is setup with the component it belongs to. If that
        component also has related platforms, the component will have to
        forward the entry to be setup by that component.

        You don't want to await this coroutine if it is called as part of the
        setup of a component, because it can cause a deadlock.
        """
        ...
    async def async_unload_platforms(
        self, entry: ConfigEntry, platforms: Iterable[str]
    ) -> bool:
        """Forward the unloading of an entry to platforms."""
        ...
    async def async_forward_entry_unload(self, entry: ConfigEntry, domain: str) -> bool:
        """Forward the unloading of an entry to a different component."""
        ...

class ConfigFlow(data_entry_flow.FlowHandler):
    """Base class for config flows with some helpers."""

    def __init_subclass__(cls, domain: str | None = ..., **kwargs: Any) -> None:
        """Initialize a subclass, register if possible."""
        ...
    @property
    def unique_id(self) -> str | None:
        """Return unique ID if available."""
        ...
    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        ...
    async def async_set_unique_id(
        self, unique_id: str | None = ..., *, raise_on_progress: bool = ...
    ) -> ConfigEntry | None:
        """Set a unique ID for the config flow.

        Returns optionally existing config entry with same ID.
        """
        ...
    async def async_step_ignore(
        self, user_input: dict[str, Any]
    ) -> data_entry_flow.FlowResult:
        """Ignore this config flow."""
        ...
    async def async_step_unignore(
        self, user_input: dict[str, Any]
    ) -> data_entry_flow.FlowResult:
        """Rediscover a config entry by it's unique_id."""
        ...
    async def async_step_user(
        self, user_input: dict[str, Any] | None = ...
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initiated by the user."""
        ...
    async def async_step_discovery(
        self, discovery_info: DiscoveryInfoType
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by discovery."""
        ...
    @callback
    def async_abort(
        self, *, reason: str, description_placeholders: dict | None = ...
    ) -> data_entry_flow.FlowResult:
        """Abort the config flow."""
        ...
    async def async_step_hassio(
        self, discovery_info: DiscoveryInfoType
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by HASS IO discovery."""
        ...
    async def async_step_homekit(
        self, discovery_info: DiscoveryInfoType
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by Homekit discovery."""
        ...
    async def async_step_mqtt(
        self, discovery_info: DiscoveryInfoType
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by MQTT discovery."""
        ...
    async def async_step_ssdp(
        self, discovery_info: DiscoveryInfoType
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by SSDP discovery."""
        ...
    async def async_step_zeroconf(
        self, discovery_info: DiscoveryInfoType
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by Zeroconf discovery."""
        ...
    async def async_step_dhcp(
        self, discovery_info: DiscoveryInfoType
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by DHCP discovery."""
        ...
    async def async_step_usb(
        self, discovery_info: DiscoveryInfoType
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by USB discovery."""
        ...
    @callback
    def async_create_entry(
        self,
        *,
        title: str,
        data: Mapping[str, Any],
        description: str | None = ...,
        description_placeholders: dict | None = ...,
        options: Mapping[str, Any] | None = ...
    ) -> data_entry_flow.FlowResult:
        """Finish config flow and create a config entry."""
        ...

class OptionsFlowManager(data_entry_flow.FlowManager):
    """Flow to set options for a configuration entry."""

    async def async_create_flow(
        self,
        handler_key: Any,
        *,
        context: dict[str, Any] | None = ...,
        data: dict[str, Any] | None = ...
    ) -> OptionsFlow:
        """Create an options flow for a config entry.

        Entry_id and flow.handler is the same thing to map entry with flow.
        """
        ...
    async def async_finish_flow(
        self, flow: data_entry_flow.FlowHandler, result: data_entry_flow.FlowResult
    ) -> data_entry_flow.FlowResult:
        """Finish an options flow and update options for configuration entry.

        Flow.handler and entry_id is the same thing to map flow with entry.
        """
        ...

class OptionsFlow(data_entry_flow.FlowHandler):
    """Base class for config option flows."""

    handler: str
    ...

class EntityRegistryDisabledHandler:
    """Handler to handle when entities related to config entries updating disabled_by."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the handler."""
        ...
    @callback
    def async_setup(self) -> None:
        """Set up the disable handler."""
        ...

async def support_entry_unload(hass: HomeAssistant, domain: str) -> bool:
    """Test if a domain supports entry unloading."""
    ...
