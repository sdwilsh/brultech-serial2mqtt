"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from typing import TypeVar
from homeassistant.core import HomeAssistant

"""Helper to help coordinating calls."""
_T = TypeVar("_T")
_FuncType = Callable[[HomeAssistant], _T]

def singleton(data_key: str) -> Callable[[_FuncType[_T]], _FuncType[_T]]:
    """Decorate a function that should be called once per instance.

    Result will be cached and simultaneous calls will be handled.
    """
    ...
