"""
This type stub file was generated by pyright.
"""

from collections import OrderedDict

"""Helpers for script and automation tracing and debugging."""

class LimitedSizeDict(OrderedDict):
    """OrderedDict limited in size."""

    def __init__(self, *args, **kwds) -> None:
        """Initialize OrderedDict limited in size."""
        ...
    def __setitem__(self, key, value):  # -> None:
        """Set item and check dict size."""
        ...