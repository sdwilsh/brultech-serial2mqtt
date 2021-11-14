"""
This type stub file was generated by pyright.
"""

import logging
from collections.abc import Mapping, MutableMapping
from typing import Any

"""Helpers for logging allowing more advanced logging styles to be used."""

class KeywordMessage:
    """
    Represents a logging message with keyword arguments.

    Adapted from: https://stackoverflow.com/a/24683360/2267718
    """

    def __init__(self, fmt: Any, args: Any, kwargs: Mapping[str, Any]) -> None:
        """Initialize a new KeywordMessage object."""
        ...
    def __str__(self) -> str:
        """Convert the object to a string for logging."""
        ...

class KeywordStyleAdapter(logging.LoggerAdapter):
    """Represents an adapter wrapping the logger allowing KeywordMessages."""

    def __init__(
        self, logger: logging.Logger, extra: Mapping[str, Any] | None = ...
    ) -> None:
        """Initialize a new StyleAdapter for the provided logger."""
        ...
    def log(self, level: int, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Log the message provided at the appropriate level."""
        ...
    def process(
        self, msg: Any, kwargs: MutableMapping[str, Any]
    ) -> tuple[Any, MutableMapping[str, Any]]:
        """Process the keyword args in preparation for logging."""
        ...