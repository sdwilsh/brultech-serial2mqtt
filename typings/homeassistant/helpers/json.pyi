"""
This type stub file was generated by pyright.
"""

import json
from typing import Any

"""Helpers to help with encoding Home Assistant objects in JSON."""

class JSONEncoder(json.JSONEncoder):
    """JSONEncoder that supports Home Assistant objects."""

    def default(self, o: Any) -> Any:
        """Convert Home Assistant objects.

        Hand other objects to the original method.
        """
        ...

class ExtendedJSONEncoder(JSONEncoder):
    """JSONEncoder that supports Home Assistant objects and falls back to repr(o)."""

    def default(self, o: Any) -> Any:
        """Convert certain objects.

        Fall back to repr(o).
        """
        ...
