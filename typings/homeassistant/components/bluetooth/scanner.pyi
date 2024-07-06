"""
This type stub file was generated by pyright.
"""

import bleak
from collections.abc import Callable
from typing import Any
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData, AdvertisementDataCallback
from homeassistant.core import HomeAssistant, callback as hass_callback
from homeassistant.exceptions import HomeAssistantError
from .base_scanner import BaseHaScanner
from .models import BluetoothScanningMode, BluetoothServiceInfoBleak

"""The bluetooth integration."""
OriginalBleakScanner = ...
PASSIVE_SCANNER_ARGS = ...
_LOGGER = ...
NEED_RESET_ERRORS = ...
WAIT_FOR_ADAPTER_TO_INIT_ERRORS = ...
ADAPTER_INIT_TIME = ...
START_ATTEMPTS = ...
SCANNING_MODE_TO_BLEAK = ...
SCANNER_WATCHDOG_MULTIPLE = ...

class ScannerStartError(HomeAssistantError):
    """Error to indicate that the scanner failed to start."""

    ...

def create_bleak_scanner(
    detection_callback: AdvertisementDataCallback,
    scanning_mode: BluetoothScanningMode,
    adapter: str | None,
) -> bleak.BleakScanner:
    """Create a Bleak scanner."""
    ...

class HaScanner(BaseHaScanner):
    """Operate and automatically recover a BleakScanner.

    Multiple BleakScanner can be used at the same time
    if there are multiple adapters. This is only useful
    if the adapters are not located physically next to each other.

    Example use cases are usbip, a long extension cable, usb to bluetooth
    over ethernet, usb over ethernet, etc.
    """

    scanner: bleak.BleakScanner
    def __init__(
        self,
        hass: HomeAssistant,
        mode: BluetoothScanningMode,
        adapter: str,
        address: str,
        new_info_callback: Callable[[BluetoothServiceInfoBleak], None],
    ) -> None:
        """Init bluetooth discovery."""
        ...

    @property
    def discovered_devices(self) -> list[BLEDevice]:
        """Return a list of discovered devices."""
        ...

    @property
    def discovered_devices_and_advertisement_data(
        self,
    ) -> dict[str, tuple[BLEDevice, AdvertisementData]]:
        """Return a list of discovered devices and advertisement data."""
        ...

    @hass_callback
    def async_setup(self) -> None:
        """Set up the scanner."""
        ...

    async def async_diagnostics(self) -> dict[str, Any]:
        """Return diagnostic information about the scanner."""
        ...

    async def async_start(self) -> None:
        """Start bluetooth scanner."""
        ...

    async def async_stop(self) -> None:
        """Stop bluetooth scanner."""
        ...
