"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable, Hashable
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant, callback

"""Ratelimit helper."""
_LOGGER = ...

class KeyedRateLimit:
    """Class to track rate limits."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize ratelimit tracker."""
        ...
    @callback
    def async_has_timer(self, key: Hashable) -> bool:
        """Check if a rate limit timer is running."""
        ...
    @callback
    def async_triggered(self, key: Hashable, now: datetime | None = ...) -> None:
        """Call when the action we are tracking was triggered."""
        ...
    @callback
    def async_cancel_timer(self, key: Hashable) -> None:
        """Cancel a rate limit time that will call the action."""
        ...
    @callback
    def async_remove(self) -> None:
        """Remove all timers."""
        ...
    @callback
    def async_schedule_action(
        self,
        key: Hashable,
        rate_limit: timedelta | None,
        now: datetime,
        action: Callable,
        *args: Any
    ) -> datetime | None:
        """Check rate limits and schedule an action if we hit the limit.

        If the rate limit is hit:
            Schedules the action for when the rate limit expires
            if there are no pending timers. The action must
            be called in async.

            Returns the time the rate limit will expire

        If the rate limit is not hit:

            Return None
        """
        ...