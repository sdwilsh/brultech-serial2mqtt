"""
This type stub file was generated by pyright.
"""

from enum import StrEnum
from typing import Final
from homeassistant.util.unit_conversion import BaseUnitConverter

"""Constants for sensor."""
DOMAIN: Final = ...
CONF_STATE_CLASS: Final = ...
ATTR_LAST_RESET: Final = ...
ATTR_STATE_CLASS: Final = ...
ATTR_OPTIONS: Final = ...

class SensorDeviceClass(StrEnum):
    """Device class for sensors."""

    DATE = ...
    ENUM = ...
    TIMESTAMP = ...
    APPARENT_POWER = ...
    AQI = ...
    ATMOSPHERIC_PRESSURE = ...
    BATTERY = ...
    CO = ...
    CO2 = ...
    CURRENT = ...
    DATA_RATE = ...
    DATA_SIZE = ...
    DISTANCE = ...
    DURATION = ...
    ENERGY = ...
    ENERGY_STORAGE = ...
    FREQUENCY = ...
    GAS = ...
    HUMIDITY = ...
    ILLUMINANCE = ...
    IRRADIANCE = ...
    MOISTURE = ...
    MONETARY = ...
    NITROGEN_DIOXIDE = ...
    NITROGEN_MONOXIDE = ...
    NITROUS_OXIDE = ...
    OZONE = ...
    PH = ...
    PM1 = ...
    PM10 = ...
    PM25 = ...
    POWER_FACTOR = ...
    POWER = ...
    PRECIPITATION = ...
    PRECIPITATION_INTENSITY = ...
    PRESSURE = ...
    REACTIVE_POWER = ...
    SIGNAL_STRENGTH = ...
    SOUND_PRESSURE = ...
    SPEED = ...
    SULPHUR_DIOXIDE = ...
    TEMPERATURE = ...
    VOLATILE_ORGANIC_COMPOUNDS = ...
    VOLATILE_ORGANIC_COMPOUNDS_PARTS = ...
    VOLTAGE = ...
    VOLUME = ...
    VOLUME_STORAGE = ...
    WATER = ...
    WEIGHT = ...
    WIND_SPEED = ...

NON_NUMERIC_DEVICE_CLASSES = ...
DEVICE_CLASSES_SCHEMA: Final = ...
DEVICE_CLASSES: Final[list[str]] = ...

class SensorStateClass(StrEnum):
    """State class for sensors."""

    MEASUREMENT = ...
    TOTAL = ...
    TOTAL_INCREASING = ...

STATE_CLASSES_SCHEMA: Final = ...
STATE_CLASS_MEASUREMENT: Final = ...
STATE_CLASS_TOTAL: Final = ...
STATE_CLASS_TOTAL_INCREASING: Final = ...
STATE_CLASSES: Final[list[str]] = ...
UNIT_CONVERTERS: dict[SensorDeviceClass | str | None, type[BaseUnitConverter]] = ...
DEVICE_CLASS_UNITS: dict[SensorDeviceClass, set[type[StrEnum] | str | None]] = ...
DEVICE_CLASS_STATE_CLASSES: dict[SensorDeviceClass, set[SensorStateClass]] = ...
