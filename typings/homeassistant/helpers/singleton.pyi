"""
This type stub file was generated by pyright.
"""

from typing import Callable

from homeassistant.core import HomeAssistant

"""Helper to help coordinating calls."""
T = ...
FUNC = Callable[[HomeAssistant], T]

def singleton(data_key: str) -> Callable[[FUNC], FUNC]:
    """Decorate a function that should be called once per instance.

    Result will be cached and simultaneous calls will be handled.
    """
    ...