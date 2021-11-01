from enum import Enum, unique
from typing import Iterator

from voluptuous import All, Match
from voluptuous import Optional as OptionalField
from voluptuous import Range
from voluptuous import Required as RequiredField
from voluptuous import Schema
from voluptuous.validators import Length

SCHEMA = Schema(
    {
        OptionalField("baud", default=115200): int,
        RequiredField("channels"): All(
            [
                Schema(
                    {
                        OptionalField("name"): All(str, Length(min=1)),
                        OptionalField("net_metered", default=False): bool,
                        RequiredField("number"): All(int, Range(min=1, max=32)),
                    }
                )
            ]
        ),
        RequiredField("device_com"): All(
            str,
            Match(
                r"^(COM1|COM2)$",
            ),
        ),
        RequiredField("name"): All(str, Length(min=1)),
        OptionalField(
            "packet_send_interval_seconds",
            default=5,
        ): All(int, Range(min=5, max=256)),
        RequiredField("url"): str,
    },
)


class ChannelConfig:
    def __init__(self, channel: dict):
        self._name = (
            channel["name"] if "name" in channel else f"channel_{channel['number']}"
        )
        self._net_metered = channel["net_metered"]
        self._number = channel["number"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def net_metered(self) -> bool:
        return self._net_metered

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


@unique
class DeviceCOM(Enum):
    COM1 = "COM1"
    COM2 = "COM2"


class DeviceConfig:
    schema = SCHEMA

    def __init__(self, device: dict):
        self._baud = device["baud"]
        self._channels = ChannelsConfig(device["channels"])
        self._device_com = (
            DeviceCOM.COM1 if device["device_com"] == "COM1" else DeviceCOM.COM2
        )
        self._name: str = device["name"]
        self._packet_send_interval_seconds = device["packet_send_interval_seconds"]
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
    def device_com(self) -> DeviceCOM:
        """Return either COM1"""
        return self._device_com

    @property
    def name(self) -> str:
        return self._name

    @property
    def packet_send_interval_seconds(self) -> int:
        return self._packet_send_interval_seconds

    @property
    def url(self) -> str:
        """Return pySerial url of the serial device to connect to."""
        return self._url
