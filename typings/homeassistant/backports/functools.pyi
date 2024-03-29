"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from typing import Any, Generic, Self, TypeVar, overload

"""Functools backports from standard lib."""
_T = TypeVar("_T")

class cached_property(Generic[_T]):
    """Backport of Python 3.12's cached_property.

    Includes https://github.com/python/cpython/pull/101890/files
    """
    def __init__(self, func: Callable[[Any], _T]) -> None:
        """Initialize."""
        ...

    def __set_name__(self, owner: type[Any], name: str) -> None:
        """Set name."""
        ...

    @overload
    def __get__(self, instance: None, owner: type[Any] | None = ...) -> Self: ...
    @overload
    def __get__(self, instance: Any, owner: type[Any] | None = ...) -> _T: ...
    def __get__(self, instance: Any | None, owner: type[Any] | None = ...) -> _T | Self:
        """Get."""
        ...

    __class_getitem__ = ...
