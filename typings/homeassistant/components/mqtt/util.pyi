"""
This type stub file was generated by pyright.
"""

from typing import Any

from homeassistant.helpers import template

"""Utility functions for the MQTT integration."""

def valid_topic(value: Any) -> str:
    """Validate that this is a valid topic name/filter."""
    ...

def valid_subscribe_topic(value: Any) -> str:
    """Validate that we can subscribe using this MQTT topic."""
    ...

def valid_subscribe_topic_template(value: Any) -> template.Template:
    """Validate either a jinja2 template or a valid MQTT subscription topic."""
    ...

def valid_publish_topic(value: Any) -> str:
    """Validate that we can publish using this MQTT topic."""
    ...

_VALID_QOS_SCHEMA = ...
MQTT_WILL_BIRTH_SCHEMA = ...
