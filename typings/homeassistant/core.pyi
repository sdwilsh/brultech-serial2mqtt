"""
This type stub file was generated by pyright.
"""

import asyncio
import datetime
import enum
import functools
import threading
import voluptuous as vol
from collections import UserDict
from collections.abc import (
    Callable,
    Collection,
    Coroutine,
    Iterable,
    KeysView,
    Mapping,
    ValuesView,
)
from typing import Any, Generic, Literal, Self, TYPE_CHECKING, TypeVar, overload
from .backports.functools import cached_property
from .util.json import JsonObjectType
from .util.read_only_dict import ReadOnlyDict
from .auth import AuthManager
from .components.http import HomeAssistantHTTP
from .config_entries import ConfigEntries
from .helpers.entity import StateInfo

"""Core components of Home Assistant.

Home Assistant is a Home Automation framework for observing the state
of entities and react to changes.
"""
if TYPE_CHECKING: ...
STAGE_1_SHUTDOWN_TIMEOUT = ...
STAGE_2_SHUTDOWN_TIMEOUT = ...
STAGE_3_SHUTDOWN_TIMEOUT = ...
_T = TypeVar("_T")
_R = TypeVar("_R")
_R_co = TypeVar("_R_co", covariant=True)
_P = ...
_UNDEF: dict[Any, Any] = ...
_CallableT = TypeVar("_CallableT", bound=Callable[..., Any])
CALLBACK_TYPE = Callable[[], None]
CORE_STORAGE_KEY = ...
CORE_STORAGE_VERSION = ...
CORE_STORAGE_MINOR_VERSION = ...
DOMAIN = ...
BLOCK_LOG_TIMEOUT = ...
ServiceResponse = JsonObjectType | None
EntityServiceResponse = dict[str, ServiceResponse]

class ConfigSource(enum.StrEnum):
    """Source of core configuration."""

    DEFAULT = ...
    DISCOVERED = ...
    STORAGE = ...
    YAML = ...

SOURCE_DISCOVERED = ...
SOURCE_STORAGE = ...
SOURCE_YAML = ...
TIMEOUT_EVENT_START = ...
MAX_EXPECTED_ENTITY_IDS = ...
_LOGGER = ...

@functools.lru_cache(MAX_EXPECTED_ENTITY_IDS)
def split_entity_id(entity_id: str) -> tuple[str, str]:
    """Split a state entity ID into domain and object ID."""
    ...

_OBJECT_ID = ...
_DOMAIN = ...
VALID_DOMAIN = ...
VALID_ENTITY_ID = ...

@functools.lru_cache(64)
def valid_domain(domain: str) -> bool:
    """Test if a domain a valid format."""
    ...

@functools.lru_cache(512)
def valid_entity_id(entity_id: str) -> bool:
    """Test if an entity ID is a valid format.

    Format: <domain>.<entity> where both are slugs.
    """
    ...

def validate_state(state: str) -> str:
    """Validate a state, raise if it not valid."""
    ...

def callback(func: _CallableT) -> _CallableT:
    """Annotation to mark method as safe to call from within the event loop."""
    ...

def is_callback(func: Callable[..., Any]) -> bool:
    """Check if function is safe to be called in the event loop."""
    ...

def is_callback_check_partial(target: Callable[..., Any]) -> bool:
    """Check if function is safe to be called in the event loop.

    This version of is_callback will also check if the target is a partial
    and walk the chain of partials to find the original function.
    """
    ...

class _Hass(threading.local):
    """Container which makes a HomeAssistant instance available to the event loop."""

    hass: HomeAssistant | None = ...

_hass = ...

@callback
def async_get_hass() -> HomeAssistant:
    """Return the HomeAssistant instance.

    Raises HomeAssistantError when called from the wrong thread.

    This should be used where it's very cumbersome or downright impossible to pass
    hass to the code which needs it.
    """
    ...

@callback
def get_release_channel() -> Literal["beta", "dev", "nightly", "stable"]:
    """Find release channel based on version number."""
    ...
@enum.unique
class HassJobType(enum.Enum):
    """Represent a job type."""

    Coroutinefunction = ...
    Callback = ...
    Executor = ...

class HassJob(Generic[_P, _R_co]):
    """Represent a job to be run later.

    We check the callable type in advance
    so we can avoid checking it every time
    we run the job.
    """

    __slots__ = ...
    def __init__(
        self,
        target: Callable[_P, _R_co],
        name: str | None = ...,
        *,
        cancel_on_shutdown: bool | None = ...,
        job_type: HassJobType | None = ...,
    ) -> None:
        """Create a job object."""
        ...

    @property
    def cancel_on_shutdown(self) -> bool | None:
        """Return if the job should be cancelled on shutdown."""
        ...

    def __repr__(self) -> str:
        """Return the job."""
        ...

class CoreState(enum.Enum):
    """Represent the current state of Home Assistant."""

    not_running = ...
    starting = ...
    running = ...
    stopping = ...
    final_write = ...
    stopped = ...
    def __str__(self) -> str:
        """Return the event."""
        ...

class HomeAssistant:
    """Root object of the Home Assistant home automation."""

    auth: AuthManager
    http: HomeAssistantHTTP = ...
    config_entries: ConfigEntries = ...
    def __new__(cls, config_dir: str) -> HomeAssistant:
        """Set the _hass thread local data."""
        ...

    def __repr__(self) -> str:
        """Return the representation."""
        ...

    def __init__(self, config_dir: str) -> None:
        """Initialize new Home Assistant object."""
        ...

    @property
    def is_running(self) -> bool:
        """Return if Home Assistant is running."""
        ...

    @property
    def is_stopping(self) -> bool:
        """Return if Home Assistant is stopping."""
        ...

    def start(self) -> int:
        """Start Home Assistant.

        Note: This function is only used for testing.
        For regular use, use "await hass.run()".
        """
        ...

    async def async_run(self, *, attach_signals: bool = ...) -> int:
        """Home Assistant main entry point.

        Start Home Assistant and block until stopped.

        This method is a coroutine.
        """
        ...

    async def async_start(self) -> None:
        """Finalize startup from inside the event loop.

        This method is a coroutine.
        """
        ...

    def add_job(
        self, target: Callable[..., Any] | Coroutine[Any, Any, Any], *args: Any
    ) -> None:
        """Add a job to be executed by the event loop or by an executor.

        If the job is either a coroutine or decorated with @callback, it will be
        run by the event loop, if not it will be run by an executor.

        target: target to call.
        args: parameters for method to call.
        """
        ...

    @overload
    @callback
    def async_add_job(
        self, target: Callable[..., Coroutine[Any, Any, _R]], *args: Any
    ) -> asyncio.Future[_R] | None: ...
    @overload
    @callback
    def async_add_job(
        self, target: Callable[..., Coroutine[Any, Any, _R] | _R], *args: Any
    ) -> asyncio.Future[_R] | None: ...
    @overload
    @callback
    def async_add_job(
        self, target: Coroutine[Any, Any, _R], *args: Any
    ) -> asyncio.Future[_R] | None: ...
    @callback
    def async_add_job(
        self,
        target: Callable[..., Coroutine[Any, Any, _R] | _R] | Coroutine[Any, Any, _R],
        *args: Any,
    ) -> asyncio.Future[_R] | None:
        """Add a job to be executed by the event loop or by an executor.

        If the job is either a coroutine or decorated with @callback, it will be
        run by the event loop, if not it will be run by an executor.

        This method must be run in the event loop.

        target: target to call.
        args: parameters for method to call.
        """
        ...

    @overload
    @callback
    def async_add_hass_job(
        self, hassjob: HassJob[..., Coroutine[Any, Any, _R]], *args: Any
    ) -> asyncio.Future[_R] | None: ...
    @overload
    @callback
    def async_add_hass_job(
        self, hassjob: HassJob[..., Coroutine[Any, Any, _R] | _R], *args: Any
    ) -> asyncio.Future[_R] | None: ...
    @callback
    def async_add_hass_job(
        self, hassjob: HassJob[..., Coroutine[Any, Any, _R] | _R], *args: Any
    ) -> asyncio.Future[_R] | None:
        """Add a HassJob from within the event loop.

        This method must be run in the event loop.
        hassjob: HassJob to call.
        args: parameters for method to call.
        """
        ...

    def create_task(
        self, target: Coroutine[Any, Any, Any], name: str | None = ...
    ) -> None:
        """Add task to the executor pool.

        target: target to call.
        """
        ...

    @callback
    def async_create_task(
        self, target: Coroutine[Any, Any, _R], name: str | None = ...
    ) -> asyncio.Task[_R]:
        """Create a task from within the event loop.

        This method must be run in the event loop. If you are using this in your
        integration, use the create task methods on the config entry instead.

        target: target to call.
        """
        ...

    @callback
    def async_create_background_task(
        self, target: Coroutine[Any, Any, _R], name: str
    ) -> asyncio.Task[_R]:
        """Create a task from within the event loop.

        This is a background task which will not block startup and will be
        automatically cancelled on shutdown. If you are using this in your
        integration, use the create task methods on the config entry instead.

        This method must be run in the event loop.
        """
        ...

    @callback
    def async_add_executor_job(
        self, target: Callable[..., _T], *args: Any
    ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        ...

    @overload
    @callback
    def async_run_hass_job(
        self, hassjob: HassJob[..., Coroutine[Any, Any, _R]], *args: Any
    ) -> asyncio.Future[_R] | None: ...
    @overload
    @callback
    def async_run_hass_job(
        self, hassjob: HassJob[..., Coroutine[Any, Any, _R] | _R], *args: Any
    ) -> asyncio.Future[_R] | None: ...
    @callback
    def async_run_hass_job(
        self, hassjob: HassJob[..., Coroutine[Any, Any, _R] | _R], *args: Any
    ) -> asyncio.Future[_R] | None:
        """Run a HassJob from within the event loop.

        This method must be run in the event loop.

        hassjob: HassJob
        args: parameters for method to call.
        """
        ...

    @overload
    @callback
    def async_run_job(
        self, target: Callable[..., Coroutine[Any, Any, _R]], *args: Any
    ) -> asyncio.Future[_R] | None: ...
    @overload
    @callback
    def async_run_job(
        self, target: Callable[..., Coroutine[Any, Any, _R] | _R], *args: Any
    ) -> asyncio.Future[_R] | None: ...
    @overload
    @callback
    def async_run_job(
        self, target: Coroutine[Any, Any, _R], *args: Any
    ) -> asyncio.Future[_R] | None: ...
    @callback
    def async_run_job(
        self,
        target: Callable[..., Coroutine[Any, Any, _R] | _R] | Coroutine[Any, Any, _R],
        *args: Any,
    ) -> asyncio.Future[_R] | None:
        """Run a job from within the event loop.

        This method must be run in the event loop.

        target: target to call.
        args: parameters for method to call.
        """
        ...

    def block_till_done(self) -> None:
        """Block until all pending work is done."""
        ...

    async def async_block_till_done(self) -> None:
        """Block until all pending work is done."""
        ...

    def stop(self) -> None:
        """Stop Home Assistant and shuts down all threads."""
        ...

    async def async_stop(self, exit_code: int = ..., *, force: bool = ...) -> None:
        """Stop Home Assistant and shuts down all threads.

        The "force" flag commands async_stop to proceed regardless of
        Home Assistant's current state. You should not set this flag
        unless you're testing.

        This method is a coroutine.
        """
        ...

class Context:
    """The context that triggered something."""

    __slots__ = ...
    def __init__(
        self,
        user_id: str | None = ...,
        parent_id: str | None = ...,
        id: str | None = ...,
    ) -> None:
        """Init the context."""
        ...

    def __eq__(self, other: Any) -> bool:
        """Compare contexts."""
        ...

    def as_dict(self) -> ReadOnlyDict[str, str | None]:
        """Return a dictionary representation of the context."""
        ...

class EventOrigin(enum.Enum):
    """Represent the origin of an event."""

    local = ...
    remote = ...
    def __str__(self) -> str:
        """Return the event."""
        ...

class Event:
    """Representation of an event within the bus."""

    __slots__ = ...
    def __init__(
        self,
        event_type: str,
        data: dict[str, Any] | None = ...,
        origin: EventOrigin = ...,
        time_fired: datetime.datetime | None = ...,
        context: Context | None = ...,
    ) -> None:
        """Initialize a new event."""
        ...

    def as_dict(self) -> ReadOnlyDict[str, Any]:
        """Create a dict representation of this Event.

        Async friendly.
        """
        ...

    def __repr__(self) -> str:
        """Return the representation."""
        ...

_FilterableJobType = tuple[
    HassJob[[Event], Coroutine[Any, Any, None] | None],
    Callable[[Event], bool] | None,
    bool,
]

class EventBus:
    """Allow the firing of and listening for events."""

    __slots__ = ...
    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize a new event bus."""
        ...

    @callback
    def async_listeners(self) -> dict[str, int]:
        """Return dictionary with events and the number of listeners.

        This method must be run in the event loop.
        """
        ...

    @property
    def listeners(self) -> dict[str, int]:
        """Return dictionary with events and the number of listeners."""
        ...

    def fire(
        self,
        event_type: str,
        event_data: dict[str, Any] | None = ...,
        origin: EventOrigin = ...,
        context: Context | None = ...,
    ) -> None:
        """Fire an event."""
        ...

    @callback
    def async_fire(
        self,
        event_type: str,
        event_data: dict[str, Any] | None = ...,
        origin: EventOrigin = ...,
        context: Context | None = ...,
        time_fired: datetime.datetime | None = ...,
    ) -> None:
        """Fire an event.

        This method must be run in the event loop.
        """
        ...

    def listen(
        self,
        event_type: str,
        listener: Callable[[Event], Coroutine[Any, Any, None] | None],
    ) -> CALLBACK_TYPE:
        """Listen for all events or events of a specific type.

        To listen to all events specify the constant ``MATCH_ALL``
        as event_type.
        """
        ...

    @callback
    def async_listen(
        self,
        event_type: str,
        listener: Callable[[Event], Coroutine[Any, Any, None] | None],
        event_filter: Callable[[Event], bool] | None = ...,
        run_immediately: bool = ...,
    ) -> CALLBACK_TYPE:
        """Listen for all events or events of a specific type.

        To listen to all events specify the constant ``MATCH_ALL``
        as event_type.

        An optional event_filter, which must be a callable decorated with
        @callback that returns a boolean value, determines if the
        listener callable should run.

        If run_immediately is passed, the callback will be run
        right away instead of using call_soon. Only use this if
        the callback results in scheduling another task.

        This method must be run in the event loop.
        """
        ...

    def listen_once(
        self,
        event_type: str,
        listener: Callable[[Event], Coroutine[Any, Any, None] | None],
    ) -> CALLBACK_TYPE:
        """Listen once for event of a specific type.

        To listen to all events specify the constant ``MATCH_ALL``
        as event_type.

        Returns function to unsubscribe the listener.
        """
        ...

    @callback
    def async_listen_once(
        self,
        event_type: str,
        listener: Callable[[Event], Coroutine[Any, Any, None] | None],
    ) -> CALLBACK_TYPE:
        """Listen once for event of a specific type.

        To listen to all events specify the constant ``MATCH_ALL``
        as event_type.

        Returns registered listener that can be used with remove_listener.

        This method must be run in the event loop.
        """
        ...

class State:
    """Object to represent a state within the state machine.

    entity_id: the entity that is represented.
    state: the state of the entity
    attributes: extra information on entity and state
    last_changed: last time the state was changed, not the attributes.
    last_updated: last time this object was updated.
    context: Context in which it was created
    domain: Domain of this state.
    object_id: Object id of this state.
    """
    def __init__(
        self,
        entity_id: str,
        state: str,
        attributes: Mapping[str, Any] | None = ...,
        last_changed: datetime.datetime | None = ...,
        last_updated: datetime.datetime | None = ...,
        context: Context | None = ...,
        validate_entity_id: bool | None = ...,
        state_info: StateInfo | None = ...,
    ) -> None:
        """Initialize a new state."""
        ...

    @property
    def name(self) -> str:
        """Name of this state."""
        ...

    def as_dict(self) -> ReadOnlyDict[str, Collection[Any]]:
        """Return a dict representation of the State.

        Async friendly.

        To be used for JSON serialization.
        Ensures: state == State.from_dict(state.as_dict())
        """
        ...

    @cached_property
    def as_dict_json(self) -> str:
        """Return a JSON string of the State."""
        ...

    @cached_property
    def as_compressed_state(self) -> dict[str, Any]:
        """Build a compressed dict of a state for adds.

        Omits the lu (last_updated) if it matches (lc) last_changed.

        Sends c (context) as a string if it only contains an id.
        """
        ...

    @cached_property
    def as_compressed_state_json(self) -> str:
        """Build a compressed JSON key value pair of a state for adds.

        The JSON string is a key value pair of the entity_id and the compressed state.

        It is used for sending multiple states in a single message.
        """
        ...

    @classmethod
    def from_dict(cls, json_dict: dict[str, Any]) -> Self | None:
        """Initialize a state from a dict.

        Async friendly.

        Ensures: state == State.from_json_dict(state.to_json_dict())
        """
        ...

    def expire(self) -> None:
        """Mark the state as old.

        We give up the original reference to the context to ensure
        the context can be garbage collected by replacing it with
        a new one with the same id to ensure the old state
        can still be examined for comparison against the new state.

        Since we are always going to fire a EVENT_STATE_CHANGED event
        after we remove a state from the state machine we need to make
        sure we don't end up holding a reference to the original context
        since it can never be garbage collected as each event would
        reference the previous one.
        """
        ...

    def __repr__(self) -> str:
        """Return the representation of the states."""
        ...

class States(UserDict[str, State]):
    """Container for states, maps entity_id -> State.

    Maintains an additional index:
    - domain -> dict[str, State]
    """
    def __init__(self) -> None:
        """Initialize the container."""
        ...

    def values(self) -> ValuesView[State]:
        """Return the underlying values to avoid __iter__ overhead."""
        ...

    def __setitem__(self, key: str, entry: State) -> None:
        """Add an item."""
        ...

    def __delitem__(self, key: str) -> None:
        """Remove an item."""
        ...

    def domain_entity_ids(self, key: str) -> KeysView[str] | tuple[()]:
        """Get all entity_ids for a domain."""
        ...

    def domain_states(self, key: str) -> ValuesView[State] | tuple[()]:
        """Get all states for a domain."""
        ...

class StateMachine:
    """Helper class that tracks the state of different entities."""

    __slots__ = ...
    def __init__(self, bus: EventBus, loop: asyncio.events.AbstractEventLoop) -> None:
        """Initialize state machine."""
        ...

    def entity_ids(self, domain_filter: str | None = ...) -> list[str]:
        """List of entity ids that are being tracked."""
        ...

    @callback
    def async_entity_ids(
        self, domain_filter: str | Iterable[str] | None = ...
    ) -> list[str]:
        """List of entity ids that are being tracked.

        This method must be run in the event loop.
        """
        ...

    @callback
    def async_entity_ids_count(
        self, domain_filter: str | Iterable[str] | None = ...
    ) -> int:
        """Count the entity ids that are being tracked.

        This method must be run in the event loop.
        """
        ...

    def all(self, domain_filter: str | Iterable[str] | None = ...) -> list[State]:
        """Create a list of all states."""
        ...

    @callback
    def async_all(self, domain_filter: str | Iterable[str] | None = ...) -> list[State]:
        """Create a list of all states matching the filter.

        This method must be run in the event loop.
        """
        ...

    def get(self, entity_id: str) -> State | None:
        """Retrieve state of entity_id or None if not found.

        Async friendly.
        """
        ...

    def is_state(self, entity_id: str, state: str) -> bool:
        """Test if entity exists and is in specified state.

        Async friendly.
        """
        ...

    def remove(self, entity_id: str) -> bool:
        """Remove the state of an entity.

        Returns boolean to indicate if an entity was removed.
        """
        ...

    @callback
    def async_remove(self, entity_id: str, context: Context | None = ...) -> bool:
        """Remove the state of an entity.

        Returns boolean to indicate if an entity was removed.

        This method must be run in the event loop.
        """
        ...

    def set(
        self,
        entity_id: str,
        new_state: str,
        attributes: Mapping[str, Any] | None = ...,
        force_update: bool = ...,
        context: Context | None = ...,
    ) -> None:
        """Set the state of an entity, add entity if it does not exist.

        Attributes is an optional dict to specify attributes of this state.

        If you just update the attributes and not the state, last changed will
        not be affected.
        """
        ...

    @callback
    def async_reserve(self, entity_id: str) -> None:
        """Reserve a state in the state machine for an entity being added.

        This must not fire an event when the state is reserved.

        This avoids a race condition where multiple entities with the same
        entity_id are added.
        """
        ...

    @callback
    def async_available(self, entity_id: str) -> bool:
        """Check to see if an entity_id is available to be used."""
        ...

    @callback
    def async_set(
        self,
        entity_id: str,
        new_state: str,
        attributes: Mapping[str, Any] | None = ...,
        force_update: bool = ...,
        context: Context | None = ...,
        state_info: StateInfo | None = ...,
    ) -> None:
        """Set the state of an entity, add entity if it does not exist.

        Attributes is an optional dict to specify attributes of this state.

        If you just update the attributes and not the state, last changed will
        not be affected.

        This method must be run in the event loop.
        """
        ...

class SupportsResponse(enum.StrEnum):
    """Service call response configuration."""

    NONE = ...
    OPTIONAL = ...
    ONLY = ...

class Service:
    """Representation of a callable service."""

    __slots__ = ...
    def __init__(
        self,
        func: Callable[
            [ServiceCall],
            Coroutine[Any, Any, ServiceResponse | EntityServiceResponse]
            | ServiceResponse
            | EntityServiceResponse
            | None,
        ],
        schema: vol.Schema | None,
        domain: str,
        service: str,
        context: Context | None = ...,
        supports_response: SupportsResponse = ...,
    ) -> None:
        """Initialize a service."""
        ...

class ServiceCall:
    """Representation of a call to a service."""

    __slots__ = ...
    def __init__(
        self,
        domain: str,
        service: str,
        data: dict[str, Any] | None = ...,
        context: Context | None = ...,
        return_response: bool = ...,
    ) -> None:
        """Initialize a service call."""
        ...

    def __repr__(self) -> str:
        """Return the representation of the service."""
        ...

class ServiceRegistry:
    """Offer the services over the eventbus."""

    __slots__ = ...
    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize a service registry."""
        ...

    @property
    def services(self) -> dict[str, dict[str, Service]]:
        """Return dictionary with per domain a list of available services."""
        ...

    @callback
    def async_services(self) -> dict[str, dict[str, Service]]:
        """Return dictionary with per domain a list of available services.

        This method must be run in the event loop.
        """
        ...

    def has_service(self, domain: str, service: str) -> bool:
        """Test if specified service exists.

        Async friendly.
        """
        ...

    def supports_response(self, domain: str, service: str) -> SupportsResponse:
        """Return whether or not the service supports response data.

        This exists so that callers can return more helpful error messages given
        the context. Will return NONE if the service does not exist as there is
        other error handling when calling the service if it does not exist.
        """
        ...

    def register(
        self,
        domain: str,
        service: str,
        service_func: Callable[
            [ServiceCall],
            Coroutine[Any, Any, ServiceResponse] | ServiceResponse | None,
        ],
        schema: vol.Schema | None = ...,
    ) -> None:
        """Register a service.

        Schema is called to coerce and validate the service data.
        """
        ...

    @callback
    def async_register(
        self,
        domain: str,
        service: str,
        service_func: Callable[
            [ServiceCall],
            Coroutine[Any, Any, ServiceResponse | EntityServiceResponse]
            | ServiceResponse
            | EntityServiceResponse
            | None,
        ],
        schema: vol.Schema | None = ...,
        supports_response: SupportsResponse = ...,
    ) -> None:
        """Register a service.

        Schema is called to coerce and validate the service data.

        This method must be run in the event loop.
        """
        ...

    def remove(self, domain: str, service: str) -> None:
        """Remove a registered service from service handler."""
        ...

    @callback
    def async_remove(self, domain: str, service: str) -> None:
        """Remove a registered service from service handler.

        This method must be run in the event loop.
        """
        ...

    def call(
        self,
        domain: str,
        service: str,
        service_data: dict[str, Any] | None = ...,
        blocking: bool = ...,
        context: Context | None = ...,
        target: dict[str, Any] | None = ...,
        return_response: bool = ...,
    ) -> ServiceResponse:
        """Call a service.

        See description of async_call for details.
        """
        ...

    async def async_call(
        self,
        domain: str,
        service: str,
        service_data: dict[str, Any] | None = ...,
        blocking: bool = ...,
        context: Context | None = ...,
        target: dict[str, Any] | None = ...,
        return_response: bool = ...,
    ) -> ServiceResponse:
        """Call a service.

        Specify blocking=True to wait until service is executed.

        If return_response=True, indicates that the caller can consume return values
        from the service, if any. Return values are a dict that can be returned by the
        standard JSON serialization process. Return values can only be used with blocking=True.

        This method will fire an event to indicate the service has been called.

        Because the service is sent as an event you are not allowed to use
        the keys ATTR_DOMAIN and ATTR_SERVICE in your service_data.

        This method is a coroutine.
        """
        ...

class Config:
    """Configuration settings for Home Assistant."""
    def __init__(self, hass: HomeAssistant, config_dir: str) -> None:
        """Initialize a new config object."""
        ...

    def distance(self, lat: float, lon: float) -> float | None:
        """Calculate distance from Home Assistant.

        Async friendly.
        """
        ...

    def path(self, *path: str) -> str:
        """Generate path to the file within the configuration directory.

        Async friendly.
        """
        ...

    def is_allowed_external_url(self, url: str) -> bool:
        """Check if an external URL is allowed."""
        ...

    def is_allowed_path(self, path: str) -> bool:
        """Check if the path is valid for access from outside.

        This function does blocking I/O and should not be called from the event loop.
        Use hass.async_add_executor_job to schedule it on the executor.
        """
        ...

    def as_dict(self) -> dict[str, Any]:
        """Create a dictionary representation of the configuration.

        Async friendly.
        """
        ...

    def set_time_zone(self, time_zone_str: str) -> None:
        """Help to set the time zone."""
        ...

    async def async_update(self, **kwargs: Any) -> None:
        """Update the configuration from a dictionary."""
        ...

    async def async_load(self) -> None:
        """Load [homeassistant] core config."""
        ...
