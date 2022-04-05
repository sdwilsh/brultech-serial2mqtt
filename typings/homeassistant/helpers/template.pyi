"""
This type stub file was generated by pyright.
"""

from collections.abc import Generator, Iterable
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
from typing import Any

import jinja2
from homeassistant.core import HomeAssistant, State, callback
from homeassistant.helpers.typing import TemplateVarsType
from homeassistant.loader import bind_hass
from jinja2 import pass_context
from jinja2.sandbox import ImmutableSandboxedEnvironment

"""Template helper methods for rendering strings with Home Assistant data."""
_LOGGER = ...
_SENTINEL = ...
DATE_STR_FORMAT = ...
_RENDER_INFO = ...
_ENVIRONMENT = ...
_ENVIRONMENT_LIMITED = ...
_ENVIRONMENT_STRICT = ...
_RE_JINJA_DELIMITERS = ...
_IS_NUMERIC = ...
_RESERVED_NAMES = ...
_GROUP_DOMAIN_PREFIX = ...
_COLLECTABLE_STATE_ATTRIBUTES = ...
ALL_STATES_RATE_LIMIT = ...
DOMAIN_STATES_RATE_LIMIT = ...
template_cv: ContextVar[tuple[str, str] | None] = ...

@bind_hass
def attach(hass: HomeAssistant, obj: Any) -> None:
    """Recursively attach hass to all template instances in list and dict."""
    ...

def render_complex(
    value: Any, variables: TemplateVarsType = ..., limited: bool = ...
) -> Any:
    """Recursive template creator helper function."""
    ...

def is_complex(value: Any) -> bool:
    """Test if data structure is a complex template."""
    ...

def is_template_string(maybe_template: str) -> bool:
    """Check if the input is a Jinja2 template."""
    ...

class ResultWrapper:
    """Result wrapper class to store render result."""

    render_result: str | None
    ...

def gen_result_wrapper(kls):  # -> Type[Wrapper]:
    """Generate a result wrapper."""

    class Wrapper(kls, ResultWrapper):
        """Wrapper of a kls that can store render_result."""

        ...

class TupleWrapper(tuple, ResultWrapper):
    """Wrap a tuple."""

    def __new__(cls, value: tuple, *, render_result: str | None = ...) -> TupleWrapper:
        """Create a new tuple class."""
        ...
    def __init__(self, value: tuple, *, render_result: str | None = ...) -> None:
        """Initialize a new tuple class."""
        ...
    def __str__(self) -> str:
        """Return string representation."""
        ...

RESULT_WRAPPERS: dict[type, type] = ...

class RenderInfo:
    """Holds information about a template render."""

    def __init__(self, template: Template) -> None:
        """Initialise."""
        ...
    def __repr__(self) -> str:
        """Representation of RenderInfo."""
        ...
    def result(self) -> str:
        """Results of the template computation."""
        ...

class Template:
    """Class to hold a template and manage caching and rendering."""

    __slots__ = ...
    def __init__(self, template, hass=...) -> None:
        """Instantiate a template."""
        ...
    def ensure_valid(self) -> None:
        """Return if template is valid."""
        ...
    def render(
        self,
        variables: TemplateVarsType = ...,
        parse_result: bool = ...,
        limited: bool = ...,
        **kwargs: Any
    ) -> Any:
        """Render given template.

        If limited is True, the template is not allowed to access any function or filter depending on hass or the state machine.
        """
        ...
    @callback
    def async_render(
        self,
        variables: TemplateVarsType = ...,
        parse_result: bool = ...,
        limited: bool = ...,
        strict: bool = ...,
        **kwargs: Any
    ) -> Any:
        """Render given template.

        This method must be run in the event loop.

        If limited is True, the template is not allowed to access any function or filter depending on hass or the state machine.
        """
        ...
    async def async_render_will_timeout(
        self,
        timeout: float,
        variables: TemplateVarsType = ...,
        strict: bool = ...,
        **kwargs: Any
    ) -> bool:
        """Check to see if rendering a template will timeout during render.

        This is intended to check for expensive templates
        that will make the system unstable.  The template
        is rendered in the executor to ensure it does not
        tie up the event loop.

        This function is not a security control and is only
        intended to be used as a safety check when testing
        templates.

        This method must be run in the event loop.
        """
        ...
    @callback
    def async_render_to_info(
        self, variables: TemplateVarsType = ..., strict: bool = ..., **kwargs: Any
    ) -> RenderInfo:
        """Render the template and collect an entity filter."""
        ...
    def render_with_possible_json_value(self, value, error_value=...):  # -> str:
        """Render template with value exposed.

        If valid JSON will expose value_json too.
        """
        ...
    @callback
    def async_render_with_possible_json_value(
        self, value, error_value=..., variables=...
    ):
        """Render template with value exposed.

        If valid JSON will expose value_json too.

        This method must be run in the event loop.
        """
        ...
    def __eq__(self, other) -> bool:
        """Compare template with another."""
        ...
    def __hash__(self) -> int:
        """Hash code for template."""
        ...
    def __repr__(self) -> str:
        """Representation of Template."""
        ...

class AllStates:
    """Class to expose all HA states as attributes."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize all states."""
        ...
    def __getattr__(self, name):  # -> TemplateState | DomainStates | None:
        """Return the domain state."""
        ...
    __getitem__ = ...
    def __iter__(self):  # -> Generator[Unknown, Unknown, Unknown]:
        """Return all states."""
        ...
    def __len__(self) -> int:
        """Return number of states."""
        ...
    def __call__(self, entity_id):  # -> str:
        """Return the states."""
        ...
    def __repr__(self) -> str:
        """Representation of All States."""
        ...

class DomainStates:
    """Class to expose a specific HA domain as attributes."""

    def __init__(self, hass: HomeAssistant, domain: str) -> None:
        """Initialize the domain states."""
        ...
    def __getattr__(self, name):  # -> TemplateState | None:
        """Return the states."""
        ...
    __getitem__ = ...
    def __iter__(self):  # -> Generator[Unknown, Unknown, Unknown]:
        """Return the iteration over all the states."""
        ...
    def __len__(self) -> int:
        """Return number of states."""
        ...
    def __repr__(self) -> str:
        """Representation of Domain States."""
        ...

class TemplateState(State):
    """Class to represent a state object in a template."""

    __slots__ = ...
    def __init__(self, hass: HomeAssistant, state: State, collect: bool = ...) -> None:
        """Initialize template state."""
        ...
    def __getitem__(self, item):  # -> Any | str:
        """Return a property as an attribute for jinja."""
        ...
    @property
    def entity_id(self):  # -> str:
        """Wrap State.entity_id.

        Intentionally does not collect state
        """
        ...
    @property
    def state(self):  # -> str:
        """Wrap State.state."""
        ...
    @property
    def attributes(self):  # -> MappingProxyType[str, Any]:
        """Wrap State.attributes."""
        ...
    @property
    def last_changed(self):  # -> datetime:
        """Wrap State.last_changed."""
        ...
    @property
    def last_updated(self):  # -> datetime:
        """Wrap State.last_updated."""
        ...
    @property
    def context(self):  # -> Context:
        """Wrap State.context."""
        ...
    @property
    def domain(self):  # -> str:
        """Wrap State.domain."""
        ...
    @property
    def object_id(self):  # -> str:
        """Wrap State.object_id."""
        ...
    @property
    def name(self):  # -> str:
        """Wrap State.name."""
        ...
    @property
    def state_with_unit(self) -> str:
        """Return the state concatenated with the unit if available."""
        ...
    def __eq__(self, other: Any) -> bool:
        """Ensure we collect on equality check."""
        ...
    def __repr__(self) -> str:
        """Representation of Template State."""
        ...

def result_as_boolean(template_result: Any | None) -> bool:
    """Convert the template result to a boolean.

    True/not 0/'1'/'true'/'yes'/'on'/'enable' are considered truthy
    False/0/None/'0'/'false'/'no'/'off'/'disable' are considered falsy

    """
    ...

def expand(hass: HomeAssistant, *args: Any) -> Iterable[State]:
    """Expand out any groups into entity states."""
    ...

def device_entities(hass: HomeAssistant, _device_id: str) -> Iterable[str]:
    """Get entity ids for entities tied to a device."""
    ...

def device_id(hass: HomeAssistant, entity_id_or_device_name: str) -> str | None:
    """Get a device ID from an entity ID or device name."""
    ...

def device_attr(hass: HomeAssistant, device_or_entity_id: str, attr_name: str) -> Any:
    """Get the device specific attribute."""
    ...

def is_device_attr(
    hass: HomeAssistant, device_or_entity_id: str, attr_name: str, attr_value: Any
) -> bool:
    """Test if a device's attribute is a specific value."""
    ...

def area_id(hass: HomeAssistant, lookup_value: str) -> str | None:
    """Get the area ID from an area name, device id, or entity id."""
    ...

def area_name(hass: HomeAssistant, lookup_value: str) -> str | None:
    """Get the area name from an area id, device id, or entity id."""
    ...

def area_entities(hass: HomeAssistant, area_id_or_name: str) -> Iterable[str]:
    """Return entities for a given area ID or name."""
    ...

def area_devices(hass: HomeAssistant, area_id_or_name: str) -> Iterable[str]:
    """Return device IDs for a given area ID or name."""
    ...

def closest(hass, *args):  # -> State | None:
    """Find closest entity.

    Closest to home:
        closest(states)
        closest(states.device_tracker)
        closest('group.children')
        closest(states.group.children)

    Closest to a point:
        closest(23.456, 23.456, 'group.children')
        closest('zone.school', 'group.children')
        closest(states.zone.school, 'group.children')

    As a filter:
        states | closest
        states.device_tracker | closest
        ['group.children', states.device_tracker] | closest
        'group.children' | closest(23.456, 23.456)
        states.device_tracker | closest('zone.school')
        'group.children' | closest(states.zone.school)

    """
    ...

def closest_filter(hass, *args):  # -> State | None:
    """Call closest as a filter. Need to reorder arguments."""
    ...

def distance(hass, *args):
    """Calculate distance.

    Will calculate distance from home to a point or between points.
    Points can be passed in using state objects or lat/lng coordinates.
    """
    ...

def is_state(hass: HomeAssistant, entity_id: str, state: State) -> bool:
    """Test if a state is a specific value."""
    ...

def is_state_attr(hass: HomeAssistant, entity_id: str, name: str, value: Any) -> bool:
    """Test if a state's attribute is a specific value."""
    ...

def state_attr(hass: HomeAssistant, entity_id: str, name: str) -> Any:
    """Get a specific attribute from a state."""
    ...

def now(hass: HomeAssistant) -> datetime:
    """Record fetching now."""
    ...

def utcnow(hass: HomeAssistant) -> datetime:
    """Record fetching utcnow."""
    ...

def warn_no_default(function, value, default):  # -> None:
    """Log warning if no default is specified."""
    ...

def forgiving_round(value, precision=..., method=..., default=...):
    """Filter to round a value."""
    ...

def multiply(value, amount, default=...):
    """Filter to convert value to float and multiply it."""
    ...

def logarithm(value, base=..., default=...):  # -> float:
    """Filter and function to get logarithm of the value with a specific base."""
    ...

def sine(value, default=...):  # -> float:
    """Filter and function to get sine of the value."""
    ...

def cosine(value, default=...):  # -> float:
    """Filter and function to get cosine of the value."""
    ...

def tangent(value, default=...):  # -> float:
    """Filter and function to get tangent of the value."""
    ...

def arc_sine(value, default=...):  # -> float:
    """Filter and function to get arc sine of the value."""
    ...

def arc_cosine(value, default=...):  # -> float:
    """Filter and function to get arc cosine of the value."""
    ...

def arc_tangent(value, default=...):  # -> float:
    """Filter and function to get arc tangent of the value."""
    ...

def arc_tangent2(*args, default=...):
    """Filter and function to calculate four quadrant arc tangent of y / x.

    The parameters to atan2 may be passed either in an iterable or as separate arguments
    The default value may be passed either as a positional or in a keyword argument
    """
    ...

def square_root(value, default=...):  # -> float:
    """Filter and function to get square root of the value."""
    ...

def timestamp_custom(value, date_format=..., local=..., default=...):
    """Filter to convert given timestamp to format."""
    ...

def timestamp_local(value, default=...):  # -> str:
    """Filter to convert given timestamp to local date/time."""
    ...

def timestamp_utc(value, default=...):  # -> str:
    """Filter to convert given timestamp to UTC date/time."""
    ...

def forgiving_as_timestamp(value, default=...):  # -> float | None:
    """Filter and function which tries to convert value to timestamp."""
    ...

def strptime(string, fmt, default=...):  # -> datetime:
    """Parse a time string to datetime."""
    ...

def fail_when_undefined(value):  # -> Undefined:
    """Filter to force a failure when the value is undefined."""
    ...

def average(*args: Any) -> float:
    """
    Filter and function to calculate the arithmetic mean of an iterable or of two or more arguments.

    The parameters may be passed as an iterable or as separate arguments.
    """
    ...

def forgiving_float(value, default=...):  # -> float:
    """Try to convert value to a float."""
    ...

def forgiving_float_filter(value, default=...):  # -> float | Literal[0]:
    """Try to convert value to a float."""
    ...

def forgiving_int(value, default=..., base=...):  # -> int:
    """Try to convert value to an int, and warn if it fails."""
    ...

def forgiving_int_filter(value, default=..., base=...):  # -> int:
    """Try to convert value to an int, and warn if it fails."""
    ...

def is_number(value):  # -> bool:
    """Try to convert value to a float."""
    ...

def regex_match(value, find=..., ignorecase=...):  # -> bool:
    """Match value using regex."""
    ...

def regex_replace(value=..., find=..., replace=..., ignorecase=...):
    """Replace using regex."""
    ...

def regex_search(value, find=..., ignorecase=...):  # -> bool:
    """Search using regex."""
    ...

def regex_findall_index(value, find=..., index=..., ignorecase=...):  # -> Any:
    """Find all matches using regex and then pick specific match index."""
    ...

def regex_findall(value, find=..., ignorecase=...):  # -> list[Any]:
    """Find all matches using regex."""
    ...

def bitwise_and(first_value, second_value):
    """Perform a bitwise and operation."""
    ...

def bitwise_or(first_value, second_value):
    """Perform a bitwise or operation."""
    ...

def base64_encode(value):  # -> str:
    """Perform base64 encode."""
    ...

def base64_decode(value):  # -> str:
    """Perform base64 denode."""
    ...

def ordinal(value):  # -> str:
    """Perform ordinal conversion."""
    ...

def from_json(value):  # -> Any:
    """Convert a JSON string to an object."""
    ...

def to_json(value):  # -> str:
    """Convert an object to a JSON string."""
    ...

@pass_context
def random_every_time(context, values):
    """Choose a random value.

    Unlike Jinja's random filter,
    this is context-dependent to avoid caching the chosen value.
    """
    ...

def today_at(time_str: str = ...) -> datetime:
    """Record fetching now where the time has been replaced with value."""
    ...

def relative_time(value):  # -> datetime | str:
    """
    Take a datetime and return its "age" as a string.

    The age can be in second, minute, hour, day, month or year. Only the
    biggest unit is considered, e.g. if it's 2 days and 3 hours, "2 days" will
    be returned.
    Make sure date is not in the future, or else it will return None.

    If the input are not a datetime object the input will be returned unmodified.
    """
    ...

def urlencode(value):  # -> bytes:
    """Urlencode dictionary and return as UTF-8 string."""
    ...

@contextmanager
def set_template(template_str: str, action: str) -> Generator:
    """Store template being parsed or rendered in a Contextvar to aid error handling."""
    ...

class LoggingUndefined(jinja2.Undefined):
    """Log on undefined variables."""

    def __str__(self) -> str:
        """Log undefined __str___."""
        ...
    def __iter__(self):  # -> Iterator[Any]:
        """Log undefined __iter___."""
        ...
    def __bool__(self):  # -> bool:
        """Log undefined __bool___."""
        ...

class TemplateEnvironment(ImmutableSandboxedEnvironment):
    """The Home Assistant template environment."""

    def __init__(self, hass, limited=..., strict=...) -> None:
        """Initialise template environment."""
        ...
    def is_safe_callable(self, obj):  # -> bool:
        """Test if callback is safe."""
        ...
    def is_safe_attribute(self, obj, attr, value):  # -> bool:
        """Test if attribute is safe."""
        ...
    def compile(
        self, source, name=..., filename=..., raw=..., defer_init=...
    ):  # -> CodeType:
        """Compile the template."""
        ...

_NO_HASS_ENV = ...
