"""
This type stub file was generated by pyright.
"""

import attr
from collections.abc import Callable, Coroutine, Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Concatenate, TypeVar, TypedDict
from homeassistant.core import CALLBACK_TYPE, HassJob, HomeAssistant, State, callback
from homeassistant.loader import bind_hass
from .device_registry import EventDeviceRegistryUpdatedData
from .entity_registry import EventEntityRegistryUpdatedData
from .template import Template
from .typing import EventType, TemplateVarsType

"""Helpers for listening to events."""
TRACK_STATE_CHANGE_CALLBACKS = ...
TRACK_STATE_CHANGE_LISTENER = ...
TRACK_STATE_ADDED_DOMAIN_CALLBACKS = ...
TRACK_STATE_ADDED_DOMAIN_LISTENER = ...
TRACK_STATE_REMOVED_DOMAIN_CALLBACKS = ...
TRACK_STATE_REMOVED_DOMAIN_LISTENER = ...
TRACK_ENTITY_REGISTRY_UPDATED_CALLBACKS = ...
TRACK_ENTITY_REGISTRY_UPDATED_LISTENER = ...
TRACK_DEVICE_REGISTRY_UPDATED_CALLBACKS = ...
TRACK_DEVICE_REGISTRY_UPDATED_LISTENER = ...
_ALL_LISTENER = ...
_DOMAINS_LISTENER = ...
_ENTITIES_LISTENER = ...
_LOGGER = ...
RANDOM_MICROSECOND_MIN = ...
RANDOM_MICROSECOND_MAX = ...
_TypedDictT = TypeVar("_TypedDictT", bound=Mapping[str, Any])
_P = ...

@dataclass(slots=True)
class TrackStates:
    """Class for keeping track of states being tracked.

    all_states: All states on the system are being tracked
    entities: Lowercased entities to track
    domains: Lowercased domains to track
    """

    all_states: bool
    entities: set[str]
    domains: set[str]
    ...

@dataclass(slots=True)
class TrackTemplate:
    """Class for keeping track of a template with variables.

    The template is template to calculate.
    The variables are variables to pass to the template.
    The rate_limit is a rate limit on how often the template is re-rendered.
    """

    template: Template
    variables: TemplateVarsType
    rate_limit: timedelta | None = ...

@dataclass(slots=True)
class TrackTemplateResult:
    """Class for result of template tracking.

    template
        The template that has changed.
    last_result
        The output from the template on the last successful run, or None
        if no previous successful run.
    result
        Result from the template run. This will be a string or an
        TemplateError if the template resulted in an error.
    """

    template: Template
    last_result: Any
    result: Any
    ...

class EventStateChangedData(TypedDict):
    """EventStateChanged data."""

    entity_id: str
    old_state: State | None
    new_state: State | None
    ...

def threaded_listener_factory(
    async_factory: Callable[Concatenate[HomeAssistant, _P], Any],
) -> Callable[Concatenate[HomeAssistant, _P], CALLBACK_TYPE]:
    """Convert an async event helper to a threaded one."""
    ...

@callback
@bind_hass
def async_track_state_change(
    hass: HomeAssistant,
    entity_ids: str | Iterable[str],
    action: Callable[
        [str, State | None, State | None], Coroutine[Any, Any, None] | None
    ],
    from_state: None | str | Iterable[str] = ...,
    to_state: None | str | Iterable[str] = ...,
) -> CALLBACK_TYPE:
    """Track specific state changes.

    entity_ids, from_state and to_state can be string or list.
    Use list to match multiple.

    Returns a function that can be called to remove the listener.

    If entity_ids are not MATCH_ALL along with from_state and to_state
    being None, async_track_state_change_event should be used instead
    as it is slightly faster.

    Must be run within the event loop.
    """
    ...

track_state_change = ...

@bind_hass
def async_track_state_change_event(
    hass: HomeAssistant,
    entity_ids: str | Iterable[str],
    action: Callable[[EventType[EventStateChangedData]], Any],
) -> CALLBACK_TYPE:
    """Track specific state change events indexed by entity_id.

    Unlike async_track_state_change, async_track_state_change_event
    passes the full event to the callback.

    In order to avoid having to iterate a long list
    of EVENT_STATE_CHANGED and fire and create a job
    for each one, we keep a dict of entity ids that
    care about the state change events so we can
    do a fast dict lookup to route events.
    """
    ...

@bind_hass
@callback
def async_track_entity_registry_updated_event(
    hass: HomeAssistant,
    entity_ids: str | Iterable[str],
    action: Callable[[EventType[EventEntityRegistryUpdatedData]], Any],
) -> CALLBACK_TYPE:
    """Track specific entity registry updated events indexed by entity_id.

    Entities must be lower case.

    Similar to async_track_state_change_event.
    """
    ...

@callback
def async_track_device_registry_updated_event(
    hass: HomeAssistant,
    device_ids: str | Iterable[str],
    action: Callable[[EventType[EventDeviceRegistryUpdatedData]], Any],
) -> CALLBACK_TYPE:
    """Track specific device registry updated events indexed by device_id.

    Similar to async_track_entity_registry_updated_event.
    """
    ...

@bind_hass
def async_track_state_added_domain(
    hass: HomeAssistant,
    domains: str | Iterable[str],
    action: Callable[[EventType[EventStateChangedData]], Any],
) -> CALLBACK_TYPE:
    """Track state change events when an entity is added to domains."""
    ...

@bind_hass
def async_track_state_removed_domain(
    hass: HomeAssistant,
    domains: str | Iterable[str],
    action: Callable[[EventType[EventStateChangedData]], Any],
) -> CALLBACK_TYPE:
    """Track state change events when an entity is removed from domains."""
    ...

class _TrackStateChangeFiltered:
    """Handle removal / refresh of tracker."""
    def __init__(
        self,
        hass: HomeAssistant,
        track_states: TrackStates,
        action: Callable[[EventType[EventStateChangedData]], Any],
    ) -> None:
        """Handle removal / refresh of tracker init."""
        ...

    @callback
    def async_setup(self) -> None:
        """Create listeners to track states."""
        ...

    @property
    def listeners(self) -> dict[str, bool | set[str]]:
        """State changes that will cause a re-render."""
        ...

    @callback
    def async_update_listeners(self, new_track_states: TrackStates) -> None:
        """Update the listeners based on the new TrackStates."""
        ...

    @callback
    def async_remove(self) -> None:
        """Cancel the listeners."""
        ...

@callback
@bind_hass
def async_track_state_change_filtered(
    hass: HomeAssistant,
    track_states: TrackStates,
    action: Callable[[EventType[EventStateChangedData]], Any],
) -> _TrackStateChangeFiltered:
    """Track state changes with a TrackStates filter that can be updated.

    Parameters
    ----------
    hass
        Home assistant object.
    track_states
        A TrackStates data class.
    action
        Callable to call with results.

    Returns
    -------
    Object used to update the listeners (async_update_listeners) with a new
    TrackStates or cancel the tracking (async_remove).

    """
    ...

@callback
@bind_hass
def async_track_template(
    hass: HomeAssistant,
    template: Template,
    action: Callable[
        [str, State | None, State | None], Coroutine[Any, Any, None] | None
    ],
    variables: TemplateVarsType | None = ...,
) -> CALLBACK_TYPE:
    """Add a listener that fires when a template evaluates to 'true'.

    Listen for the result of the template becoming true, or a true-like
    string result, such as 'On', 'Open', or 'Yes'. If the template results
    in an error state when the value changes, this will be logged and not
    passed through.

    If the initial check of the template is invalid and results in an
    exception, the listener will still be registered but will only
    fire if the template result becomes true without an exception.

    Action arguments
    ----------------
    entity_id
        ID of the entity that triggered the state change.
    old_state
        The old state of the entity that changed.
    new_state
        New state of the entity that changed.

    Parameters
    ----------
    hass
        Home assistant object.
    template
        The template to calculate.
    action
        Callable to call with results. See above for arguments.
    variables
        Variables to pass to the template.

    Returns
    -------
    Callable to unregister the listener.

    """
    ...

track_template = ...

class TrackTemplateResultInfo:
    """Handle removal / refresh of tracker."""
    def __init__(
        self,
        hass: HomeAssistant,
        track_templates: Sequence[TrackTemplate],
        action: TrackTemplateResultListener,
        has_super_template: bool = ...,
    ) -> None:
        """Handle removal / refresh of tracker init."""
        ...

    def __repr__(self) -> str:
        """Return the representation."""
        ...

    def async_setup(
        self, strict: bool = ..., log_fn: Callable[[int, str], None] | None = ...
    ) -> None:
        """Activation of template tracking."""
        ...

    @property
    def listeners(self) -> dict[str, bool | set[str]]:
        """State changes that will cause a re-render."""
        ...

    @callback
    def async_remove(self) -> None:
        """Cancel the listener."""
        ...

    @callback
    def async_refresh(self) -> None:
        """Force recalculate the template."""
        ...

TrackTemplateResultListener = Callable[
    [EventType[EventStateChangedData] | None, list[TrackTemplateResult]],
    Coroutine[Any, Any, None] | None,
]

@callback
@bind_hass
def async_track_template_result(
    hass: HomeAssistant,
    track_templates: Sequence[TrackTemplate],
    action: TrackTemplateResultListener,
    strict: bool = ...,
    log_fn: Callable[[int, str], None] | None = ...,
    has_super_template: bool = ...,
) -> TrackTemplateResultInfo:
    """Add a listener that fires when the result of a template changes.

    The action will fire with the initial result from the template, and
    then whenever the output from the template changes. The template will
    be reevaluated if any states referenced in the last run of the
    template change, or if manually triggered. If the result of the
    evaluation is different from the previous run, the listener is passed
    the result.

    If the template results in an TemplateError, this will be returned to
    the listener the first time this happens but not for subsequent errors.
    Once the template returns to a non-error condition the result is sent
    to the action as usual.

    Parameters
    ----------
    hass
        Home assistant object.
    track_templates
        An iterable of TrackTemplate.
    action
        Callable to call with results.
    strict
        When set to True, raise on undefined variables.
    log_fn
        If not None, template error messages will logging by calling log_fn
        instead of the normal logging facility.
    has_super_template
        When set to True, the first template will block rendering of other
        templates if it doesn't render as True.

    Returns
    -------
    Info object used to unregister the listener, and refresh the template.

    """
    ...

@callback
@bind_hass
def async_track_same_state(
    hass: HomeAssistant,
    period: timedelta,
    action: Callable[[], Coroutine[Any, Any, None] | None],
    async_check_same_func: Callable[[str, State | None, State | None], bool],
    entity_ids: str | Iterable[str] = ...,
) -> CALLBACK_TYPE:
    """Track the state of entities for a period and run an action.

    If async_check_func is None it use the state of orig_value.
    Without entity_ids we track all state changes.
    """
    ...

track_same_state = ...

@callback
@bind_hass
def async_track_point_in_time(
    hass: HomeAssistant,
    action: HassJob[[datetime], Coroutine[Any, Any, None] | None]
    | Callable[[datetime], Coroutine[Any, Any, None] | None],
    point_in_time: datetime,
) -> CALLBACK_TYPE:
    """Add a listener that fires once at or after a specific point in time.

    The listener is passed the time it fires in local time.
    """
    ...

track_point_in_time = ...

@callback
@bind_hass
def async_track_point_in_utc_time(
    hass: HomeAssistant,
    action: HassJob[[datetime], Coroutine[Any, Any, None] | None]
    | Callable[[datetime], Coroutine[Any, Any, None] | None],
    point_in_time: datetime,
) -> CALLBACK_TYPE:
    """Add a listener that fires once at or after a specific point in time.

    The listener is passed the time it fires in UTC time.
    """
    ...

track_point_in_utc_time = ...

@callback
@bind_hass
def async_call_at(
    hass: HomeAssistant,
    action: HassJob[[datetime], Coroutine[Any, Any, None] | None]
    | Callable[[datetime], Coroutine[Any, Any, None] | None],
    loop_time: float,
) -> CALLBACK_TYPE:
    """Add a listener that fires at or after <loop_time>.

    The listener is passed the time it fires in UTC time.
    """
    ...

@callback
@bind_hass
def async_call_later(
    hass: HomeAssistant,
    delay: float | timedelta,
    action: HassJob[[datetime], Coroutine[Any, Any, None] | None]
    | Callable[[datetime], Coroutine[Any, Any, None] | None],
) -> CALLBACK_TYPE:
    """Add a listener that fires at or after <delay>.

    The listener is passed the time it fires in UTC time.
    """
    ...

call_later = ...

@callback
@bind_hass
def async_track_time_interval(
    hass: HomeAssistant,
    action: Callable[[datetime], Coroutine[Any, Any, None] | None],
    interval: timedelta,
    *,
    name: str | None = ...,
    cancel_on_shutdown: bool | None = ...,
) -> CALLBACK_TYPE:
    """Add a listener that fires repetitively at every timedelta interval.

    The listener is passed the time it fires in UTC time.
    """
    ...

track_time_interval = ...

@attr.s
class SunListener:
    """Helper class to help listen to sun events."""

    hass: HomeAssistant = ...
    job: HassJob[[], Coroutine[Any, Any, None] | None] = ...
    event: str = ...
    offset: timedelta | None = ...
    _unsub_sun: CALLBACK_TYPE | None = ...
    _unsub_config: CALLBACK_TYPE | None = ...
    @callback
    def async_attach(self) -> None:
        """Attach a sun listener."""
        ...

    @callback
    def async_detach(self) -> None:
        """Detach the sun listener."""
        ...

@callback
@bind_hass
def async_track_sunrise(
    hass: HomeAssistant, action: Callable[[], None], offset: timedelta | None = ...
) -> CALLBACK_TYPE:
    """Add a listener that will fire a specified offset from sunrise daily."""
    ...

track_sunrise = ...

@callback
@bind_hass
def async_track_sunset(
    hass: HomeAssistant, action: Callable[[], None], offset: timedelta | None = ...
) -> CALLBACK_TYPE:
    """Add a listener that will fire a specified offset from sunset daily."""
    ...

track_sunset = ...
time_tracker_utcnow = ...
time_tracker_timestamp = ...

@callback
@bind_hass
def async_track_utc_time_change(
    hass: HomeAssistant,
    action: Callable[[datetime], Coroutine[Any, Any, None] | None],
    hour: Any | None = ...,
    minute: Any | None = ...,
    second: Any | None = ...,
    local: bool = ...,
) -> CALLBACK_TYPE:
    """Add a listener that will fire every time the UTC or local time matches a pattern.

    The listener is passed the time it fires in UTC or local time.
    """
    ...

track_utc_time_change = ...

@callback
@bind_hass
def async_track_time_change(
    hass: HomeAssistant,
    action: Callable[[datetime], Coroutine[Any, Any, None] | None],
    hour: Any | None = ...,
    minute: Any | None = ...,
    second: Any | None = ...,
) -> CALLBACK_TYPE:
    """Add a listener that will fire every time the local time matches a pattern.

    The listener is passed the time it fires in local time.
    """
    ...

track_time_change = ...

def process_state_match(
    parameter: None | str | Iterable[str], invert: bool = ...
) -> Callable[[str | None], bool]:
    """Convert parameter to function that matches input against parameter."""
    ...
