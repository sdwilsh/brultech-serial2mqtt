from voluptuous import Optional, Required, Schema

SCHEMA = Schema(
    {
        Optional("baud", default=115200): int,
        Required("url"): str,
    },
)


class DeviceConfig:
    schema = SCHEMA

    def __init__(self, device: dict):
        self._baud = device["baud"]
        self._url = device["url"]

    @property
    def baud(self) -> int:
        """Return baud rate."""
        return self._baud

    @property
    def url(self) -> str:
        """Return pySerial url of the serial device to connect to."""
        return self._url
