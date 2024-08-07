"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable, Coroutine
from typing import Any, Concatenate, TypeVar, overload
from aiohttp.web import Request, Response
from homeassistant.exceptions import Unauthorized
from .view import HomeAssistantView

"""Decorators for the Home Assistant API."""
_HomeAssistantViewT = TypeVar("_HomeAssistantViewT", bound=HomeAssistantView)
_P = ...
_FuncType = Callable[
    Concatenate[_HomeAssistantViewT, Request, _P], Coroutine[Any, Any, Response]
]

@overload
def require_admin(
    _func: None = ..., *, error: Unauthorized | None = ...
) -> Callable[
    [_FuncType[_HomeAssistantViewT, _P]], _FuncType[_HomeAssistantViewT, _P]
]: ...
@overload
def require_admin(
    _func: _FuncType[_HomeAssistantViewT, _P],
) -> _FuncType[_HomeAssistantViewT, _P]: ...
def require_admin(
    _func: _FuncType[_HomeAssistantViewT, _P] | None = ...,
    *,
    error: Unauthorized | None = ...,
) -> (
    Callable[[_FuncType[_HomeAssistantViewT, _P]], _FuncType[_HomeAssistantViewT, _P]]
    | _FuncType[_HomeAssistantViewT, _P]
):
    """Home Assistant API decorator to require user to be an admin."""
    ...
