"""
This type stub file was generated by pyright.
"""

from typing import TypeVar

"""Read only dictionary."""
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

class ReadOnlyDict(dict[_KT, _VT]):
    """Read only version of dict that is compatible with dict types."""

    __setitem__ = ...
    __delitem__ = ...
    pop = ...
    popitem = ...
    clear = ...
    update = ...
    setdefault = ...
