"""
This type stub file was generated by pyright.
"""

from collections.abc import Generator, Sequence
from typing import TYPE_CHECKING

import attr

from .core import Context

"""The exceptions used by Home Assistant."""
if TYPE_CHECKING: ...

class HomeAssistantError(Exception):
    """General Home Assistant exception occurred."""

    ...

class InvalidEntityFormatError(HomeAssistantError):
    """When an invalid formatted entity is encountered."""

    ...

class NoEntitySpecifiedError(HomeAssistantError):
    """When no entity is specified."""

    ...

class TemplateError(HomeAssistantError):
    """Error during template rendering."""

    def __init__(self, exception: Exception) -> None:
        """Init the error."""
        ...

@attr.s
class ConditionError(HomeAssistantError):
    """Error during condition evaluation."""

    type: str = ...
    def output(self, indent: int) -> Generator[str, None, None]:
        """Yield an indented representation."""
        ...
    def __str__(self) -> str:
        """Return string representation."""
        ...

@attr.s
class ConditionErrorMessage(ConditionError):
    """Condition error message."""

    message: str = ...
    def output(self, indent: int) -> Generator[str, None, None]:
        """Yield an indented representation."""
        ...

@attr.s
class ConditionErrorIndex(ConditionError):
    """Condition error with index."""

    index: int = ...
    total: int = ...
    error: ConditionError = ...
    def output(self, indent: int) -> Generator[str, None, None]:
        """Yield an indented representation."""
        ...

@attr.s
class ConditionErrorContainer(ConditionError):
    """Condition error with subconditions."""

    errors: Sequence[ConditionError] = ...
    def output(self, indent: int) -> Generator[str, None, None]:
        """Yield an indented representation."""
        ...

class IntegrationError(HomeAssistantError):
    """Base class for platform and config entry exceptions."""

    def __str__(self) -> str:
        """Return a human readable error."""
        ...

class PlatformNotReady(IntegrationError):
    """Error to indicate that platform is not ready."""

    ...

class ConfigEntryNotReady(IntegrationError):
    """Error to indicate that config entry is not ready."""

    ...

class ConfigEntryAuthFailed(IntegrationError):
    """Error to indicate that config entry could not authenticate."""

    ...

class InvalidStateError(HomeAssistantError):
    """When an invalid state is encountered."""

    ...

class Unauthorized(HomeAssistantError):
    """When an action is unauthorized."""

    def __init__(
        self,
        context: Context | None = ...,
        user_id: str | None = ...,
        entity_id: str | None = ...,
        config_entry_id: str | None = ...,
        perm_category: str | None = ...,
        permission: str | None = ...,
    ) -> None:
        """Unauthorized error."""
        ...

class UnknownUser(Unauthorized):
    """When call is made with user ID that doesn't exist."""

    ...

class ServiceNotFound(HomeAssistantError):
    """Raised when a service is not found."""

    def __init__(self, domain: str, service: str) -> None:
        """Initialize error."""
        ...
    def __str__(self) -> str:
        """Return string representation."""
        ...

class MaxLengthExceeded(HomeAssistantError):
    """Raised when a property value has exceeded the max character length."""

    def __init__(self, value: str, property_name: str, max_length: int) -> None:
        """Initialize error."""
        ...

class RequiredParameterMissing(HomeAssistantError):
    """Raised when a required parameter is missing from a function call."""

    def __init__(self, parameter_names: list[str]) -> None:
        """Initialize error."""
        ...
