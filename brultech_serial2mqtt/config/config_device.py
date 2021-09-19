from typing import Iterator

from voluptuous import All, Optional, Range, Required, Schema
from voluptuous.validators import Length

SCHEMA = Schema(
    {
        Optional("baud", default=115200): int,
        Required("channels"): All(
            [
                Schema(
                    {
                        Optional("name"): All(str, Length(min=1)),
                        Required("number"): All(int, Range(min=1, max=32)),
                    }
                )
            ]
        ),
        Required("url"): str,
    },
)


class ChannelConfig:
    def __init__(self, channel: dict):
        self._name = (
            channel["name"] if "name" in channel else f"channel_{channel['number']}"
        )
        self._number = channel["number"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def number(self) -> int:
        return self._number


class ChannelsConfig:
    def __init__(self, channels: dict):
        self._channels: dict[int, ChannelConfig] = {
            c["number"]: ChannelConfig(c) for c in channels
        }

    def __getitem__(self, key: int) -> ChannelConfig:
        assert key in self._channels
        return self._channels[key]

    def __len__(self) -> int:
        return len(self._channels)

    def __iter__(self) -> Iterator[ChannelConfig]:
        return iter(self._channels.values())


class DeviceConfig:
    schema = SCHEMA

    def __init__(self, device: dict):
        self._baud = device["baud"]
        self._channels = ChannelsConfig(device["channels"])
        self._url = device["url"]

    @property
    def baud(self) -> int:
        """Return baud rate."""
        return self._baud

    @property
    def channels(self) -> ChannelsConfig:
        """Return the monitored channel configurations."""
        return self._channels

    @property
    def url(self) -> str:
        """Return pySerial url of the serial device to connect to."""
        return self._url
