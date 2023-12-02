"""
This type stub file was generated by pyright.
"""

from aiohttp.web import Application
from homeassistant.core import callback

"""Middleware that helps with the control of headers in our responses."""

@callback
def setup_headers(app: Application, use_x_frame_options: bool) -> None:
    """Create headers middleware for the app."""
    ...
