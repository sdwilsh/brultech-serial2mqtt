"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from functools import lru_cache

"""Typing Helpers for Home Assistant."""
_MM_TO_M = ...
_CM_TO_M = ...
_KM_TO_M = ...
_IN_TO_M = ...
_FOOT_TO_M = ...
_YARD_TO_M = ...
_MILE_TO_M = ...
_NAUTICAL_MILE_TO_M = ...
_HRS_TO_SECS = ...
_DAYS_TO_SECS = ...
_POUND_TO_G = ...
_OUNCE_TO_G = ...
_STONE_TO_G = ...
_STANDARD_GRAVITY = ...
_MERCURY_DENSITY = ...
_L_TO_CUBIC_METER = ...
_ML_TO_CUBIC_METER = ...
_GALLON_TO_CUBIC_METER = ...
_FLUID_OUNCE_TO_CUBIC_METER = ...
_CUBIC_FOOT_TO_CUBIC_METER = ...

class BaseUnitConverter:
    """Define the format of a conversion utility."""

    UNIT_CLASS: str
    NORMALIZED_UNIT: str | None
    VALID_UNITS: set[str | None]
    _UNIT_CONVERSION: dict[str | None, float]
    @classmethod
    def convert(cls, value: float, from_unit: str | None, to_unit: str | None) -> float:
        """Convert one unit of measurement to another."""
        ...

    @classmethod
    @lru_cache
    def converter_factory(
        cls, from_unit: str | None, to_unit: str | None
    ) -> Callable[[float], float]:
        """Return a function to convert one unit of measurement to another."""
        ...

    @classmethod
    @lru_cache
    def converter_factory_allow_none(
        cls, from_unit: str | None, to_unit: str | None
    ) -> Callable[[float | None], float | None]:
        """Return a function to convert one unit of measurement to another which allows None."""
        ...

    @classmethod
    @lru_cache
    def get_unit_ratio(cls, from_unit: str | None, to_unit: str | None) -> float:
        """Get unit ratio between units of measurement."""
        ...

class DataRateConverter(BaseUnitConverter):
    """Utility to convert data rate values."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    _UNIT_CONVERSION: dict[str | None, float] = ...
    VALID_UNITS = ...

class DistanceConverter(BaseUnitConverter):
    """Utility to convert distance values."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    _UNIT_CONVERSION: dict[str | None, float] = ...
    VALID_UNITS = ...

class ElectricCurrentConverter(BaseUnitConverter):
    """Utility to convert electric current values."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    _UNIT_CONVERSION: dict[str | None, float] = ...
    VALID_UNITS = ...

class ElectricPotentialConverter(BaseUnitConverter):
    """Utility to convert electric potential values."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    _UNIT_CONVERSION: dict[str | None, float] = ...
    VALID_UNITS = ...

class EnergyConverter(BaseUnitConverter):
    """Utility to convert energy values."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    _UNIT_CONVERSION: dict[str | None, float] = ...
    VALID_UNITS = ...

class InformationConverter(BaseUnitConverter):
    """Utility to convert information values."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    _UNIT_CONVERSION: dict[str | None, float] = ...
    VALID_UNITS = ...

class MassConverter(BaseUnitConverter):
    """Utility to convert mass values."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    _UNIT_CONVERSION: dict[str | None, float] = ...
    VALID_UNITS = ...

class PowerConverter(BaseUnitConverter):
    """Utility to convert power values."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    _UNIT_CONVERSION: dict[str | None, float] = ...
    VALID_UNITS = ...

class PressureConverter(BaseUnitConverter):
    """Utility to convert pressure values."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    _UNIT_CONVERSION: dict[str | None, float] = ...
    VALID_UNITS = ...

class SpeedConverter(BaseUnitConverter):
    """Utility to convert speed values."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    _UNIT_CONVERSION: dict[str | None, float] = ...
    VALID_UNITS = ...

class TemperatureConverter(BaseUnitConverter):
    """Utility to convert temperature values."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    VALID_UNITS = ...
    _UNIT_CONVERSION = ...
    @classmethod
    @lru_cache(maxsize=8)
    def converter_factory(
        cls, from_unit: str | None, to_unit: str | None
    ) -> Callable[[float], float]:
        """Return a function to convert a temperature from one unit to another."""
        ...

    @classmethod
    @lru_cache(maxsize=8)
    def converter_factory_allow_none(
        cls, from_unit: str | None, to_unit: str | None
    ) -> Callable[[float | None], float | None]:
        """Return a function to convert a temperature from one unit to another which allows None."""
        ...

    @classmethod
    def convert_interval(cls, interval: float, from_unit: str, to_unit: str) -> float:
        """Convert a temperature interval from one unit to another.

        eg. a 10°C interval (10°C to 20°C) will return a 18°F (50°F to 68°F) interval

        For converting a temperature value, please use `convert` as this method
        skips floor adjustment.
        """
        ...

class UnitlessRatioConverter(BaseUnitConverter):
    """Utility to convert unitless ratios."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    _UNIT_CONVERSION: dict[str | None, float] = ...
    VALID_UNITS = ...

class VolumeConverter(BaseUnitConverter):
    """Utility to convert volume values."""

    UNIT_CLASS = ...
    NORMALIZED_UNIT = ...
    _UNIT_CONVERSION: dict[str | None, float] = ...
    VALID_UNITS = ...
