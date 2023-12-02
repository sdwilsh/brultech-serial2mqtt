"""
This type stub file was generated by pyright.
"""

import datetime as dt
from functools import partial
from typing import Any

"""Helper methods to handle the time in Home Assistant."""
DATE_STR_FORMAT = ...
UTC = ...
DEFAULT_TIME_ZONE: dt.tzinfo = ...
CLOCK_MONOTONIC_COARSE = ...
EPOCHORDINAL = ...
DATETIME_RE = ...
STANDARD_DURATION_RE = ...
ISO8601_DURATION_RE = ...
POSTGRES_INTERVAL_RE = ...

def set_default_time_zone(time_zone: dt.tzinfo) -> None:
    """Set a default time zone to be used when none is specified.

    Async friendly.
    """
    ...

def get_time_zone(time_zone_str: str) -> dt.tzinfo | None:
    """Get time zone from string. Return None if unable to determine.

    Async friendly.
    """
    ...

utcnow: partial[dt.datetime] = ...

def now(time_zone: dt.tzinfo | None = ...) -> dt.datetime:
    """Get now in specified time zone."""
    ...

def as_utc(dattim: dt.datetime) -> dt.datetime:
    """Return a datetime as UTC time.

    Assumes datetime without tzinfo to be in the DEFAULT_TIME_ZONE.
    """
    ...

def as_timestamp(dt_value: dt.datetime | str) -> float:
    """Convert a date/time into a unix time (seconds since 1970)."""
    ...

def as_local(dattim: dt.datetime) -> dt.datetime:
    """Convert a UTC datetime object to local time zone."""
    ...

utc_from_timestamp = ...

def utc_to_timestamp(utc_dt: dt.datetime) -> float:
    """Fast conversion of a datetime in UTC to a timestamp."""
    ...

def start_of_local_day(dt_or_d: dt.date | dt.datetime | None = ...) -> dt.datetime:
    """Return local datetime object of start of day from date or datetime."""
    ...

def parse_datetime(dt_str: str) -> dt.datetime | None:
    """Parse a string and return a datetime.datetime.

    This function supports time zone offsets. When the input contains one,
    the output uses a timezone with a fixed offset from UTC.
    Raises ValueError if the input is well formatted but not a valid datetime.
    Returns None if the input isn't well formatted.
    """
    ...

def parse_date(dt_str: str) -> dt.date | None:
    """Convert a date string to a date object."""
    ...

def parse_duration(value: str) -> dt.timedelta | None:
    """Parse a duration string and return a datetime.timedelta.

    Also supports ISO 8601 representation and PostgreSQL's day-time interval
    format.
    """
    ...

def parse_time(time_str: str) -> dt.time | None:
    """Parse a time string (00:20:00) into Time object.

    Return None if invalid.
    """
    ...

def get_age(date: dt.datetime) -> str:
    """Take a datetime and return its "age" as a string.

    The age can be in second, minute, hour, day, month or year. Only the
    biggest unit is considered, e.g. if it's 2 days and 3 hours, "2 days" will
    be returned.
    Make sure date is not in the future, or else it won't work.
    """
    ...

def parse_time_expression(parameter: Any, min_value: int, max_value: int) -> list[int]:
    """Parse the time expression part and return a list of times to match."""
    ...

def find_next_time_expression_time(
    now: dt.datetime, seconds: list[int], minutes: list[int], hours: list[int]
) -> dt.datetime:
    """Find the next datetime from now for which the time expression matches.

    The algorithm looks at each time unit separately and tries to find the
    next one that matches for each. If any of them would roll over, all
    time units below that are reset to the first matching value.

    Timezones are also handled (the tzinfo of the now object is used),
    including daylight saving time.
    """
    ...

monotonic_time_coarse = ...
