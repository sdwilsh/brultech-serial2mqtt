import re
import typing

NullableNumber = typing.Union[int, float, None]

class _WithSubValidators:
    def __init__(
        self, *validators, msg=..., required=..., discriminant=...
    ) -> None: ...
    def __call__(self, v=...) -> dict[str, typing.Any]: ...

class All(_WithSubValidators): ...
class Any(_WithSubValidators): ...

class Length:
    def __init__(
        self,
        min: NullableNumber = None,
        max: NullableNumber = None,
        msg: typing.Optional[str] = None,
    ) -> None: ...

class Match:
    def __init__(
        self, pattern: typing.Union[re.Pattern, str], msg: typing.Optional[str] = None
    ) -> None: ...

class Range:
    def __init__(
        self,
        min: NullableNumber = None,
        max: NullableNumber = None,
        min_included: bool = True,
        max_included: bool = True,
        msg: typing.Optional[str] = None,
    ) -> None: ...
