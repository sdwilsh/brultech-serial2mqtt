"""
This type stub file was generated by pyright.
"""

import aiohttp
from typing import NamedTuple

"""Module with location helpers.

detect_location_info and elevation are mocked by default during tests.
"""
WHOAMI_URL = ...
WHOAMI_URL_DEV = ...
AXIS_A = ...
FLATTENING = ...
AXIS_B = ...
MILES_PER_KILOMETER = ...
MAX_ITERATIONS = ...
CONVERGENCE_THRESHOLD = ...

class LocationInfo(NamedTuple):
    """Tuple with location information."""

    ip: str
    country_code: str
    currency: str
    region_code: str
    region_name: str
    city: str
    zip_code: str
    time_zone: str
    latitude: float
    longitude: float
    use_metric: bool
    ...

async def async_detect_location_info(
    session: aiohttp.ClientSession,
) -> LocationInfo | None:
    """Detect location information."""
    ...

def distance(
    lat1: float | None, lon1: float | None, lat2: float, lon2: float
) -> float | None:
    """Calculate the distance in meters between two points.

    Async friendly.
    """
    ...

def vincenty(
    point1: tuple[float, float], point2: tuple[float, float], miles: bool = ...
) -> float | None:
    """Vincenty formula (inverse method) to calculate the distance.

    Result in kilometers or miles between two points on the surface of a
    spheroid.

    Async friendly.
    """
    ...
