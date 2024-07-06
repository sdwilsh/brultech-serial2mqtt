import collections
import typing

Schemable = typing.Union[
    "Schema",
    "Object",
    collections.Mapping,
    list,
    tuple,
    frozenset,
    set,
    bool,
    bytes,
    int,
    str,
    float,
    complex,
    type,
    object,
    dict,
    None,
    typing.Callable,
]


class Marker(object):
    def __init__(
        self,
        schema_: Schemable,
        msg: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
    ) -> None: ...


class Object(dict):
    def __init__(self, schema: typing.Any, cls: object = ...) -> None: ...


class Optional(Marker):
    def __init__(
        self,
        schema: Schemable,
        msg: typing.Optional[str] = None,
        default: typing.Any = ...,
        description: typing.Optional[str] = None,
    ) -> None: ...


class Required(Marker):
    def __init__(
        self,
        schema: Schemable,
        msg: typing.Optional[str] = None,
        default: typing.Any = ...,
        description: typing.Optional[str] = None,
    ) -> None: ...


class Schema:
    def __init__(
        self, schema: Schemable, required: bool = False, extra: int = ...
    ) -> None: ...

    def __call__(self, data) -> dict[str, typing.Any]: ...
