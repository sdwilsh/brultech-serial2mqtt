"""
This type stub file was generated by pyright.
"""

"""Temperature util functions."""

def fahrenheit_to_celsius(fahrenheit: float, interval: bool = ...) -> float:
    """Convert a temperature in Fahrenheit to Celsius."""
    ...

def kelvin_to_celsius(kelvin: float, interval: bool = ...) -> float:
    """Convert a temperature in Kelvin to Celsius."""
    ...

def celsius_to_fahrenheit(celsius: float, interval: bool = ...) -> float:
    """Convert a temperature in Celsius to Fahrenheit."""
    ...

def celsius_to_kelvin(celsius: float, interval: bool = ...) -> float:
    """Convert a temperature in Celsius to Fahrenheit."""
    ...

def convert(
    temperature: float, from_unit: str, to_unit: str, interval: bool = ...
) -> float:
    """Convert a temperature from one unit to another."""
    ...