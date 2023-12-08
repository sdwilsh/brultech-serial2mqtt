from __future__ import annotations

from enum import Enum, unique
from typing import Any, Dict, Iterator, List

import voluptuous as vol
import voluptuous.validators as validators
from siobrultech_protocols.gem.const import PACKET_DELAY_CLEAR_TIME_DEFAULT
from siobrultech_protocols.gem.protocol import (
    ApiType as DeviceType,
    API_RESPONSE_WAIT_TIME,
)
from voluptuous.error import Invalid


@unique
class ChannelType(Enum):
    NORMAL = 1
    MAIN = 2
    SOLAR_DOWNSTREAM_MAIN = 3
    SOLAR_UPSTREAM_MAIN = 4

    @classmethod
    def fromValue(cls, value: str) -> ChannelType:
        for t in cls:
            if value.upper() == t.name:
                return t
        raise Invalid(
            f"Must be a valid channel type ({', '.join([t.name for t in cls])})"
        )


SCHEMA = vol.Schema(
    {
        vol.Optional("baud", default=115200): int,
        vol.Required("channels"): validators.All(
            [
                vol.Schema(
                    {
                        vol.Optional("home_assistant"): validators.All(bool, None),
                        vol.Optional("name"): validators.All(
                            str, validators.Length(min=1)
                        ),
                        vol.Required("number"): validators.All(
                            int, validators.Range(min=1, max=32)
                        ),
                        vol.Optional("type", default="normal"): ChannelType.fromValue,
                    }
                )
            ]
        ),
        vol.Required("device_com"): validators.All(
            str,
            validators.Match(
                r"^(COM1|COM2)$",
            ),
        ),
        vol.Required("name"): validators.All(str, validators.Length(min=1)),
        vol.Optional(
            "packet_delay_clear_seconds",
            default=PACKET_DELAY_CLEAR_TIME_DEFAULT.seconds,
        ): validators.All(
            int, validators.Range(min=1, max=15 - API_RESPONSE_WAIT_TIME.seconds)
        ),
        vol.Optional(
            "send_interval_seconds",
            default=8,
        ): validators.All(int, validators.Range(min=5, max=256)),
        vol.Optional("type", default="GEM"): validators.All(
            str, validators.Match(r"^(ECM|GEM)$")
        ),
        vol.Optional("url", default="/dev/ttyUSB0"): str,
    },
)


class ChannelConfig:
    def __init__(self, channel_config: Dict[str, Any], polarized: bool):
        self._name = (
            channel_config["name"]
            if "name" in channel_config
            else f"Channel {channel_config['number']}"
        )
        self._number = channel_config["number"]
        self._polarized = polarized
        self._type = channel_config["type"]
        self._home_assistant = (
            channel_config["home_assistant"]
            if "home_assistant" in channel_config and channel_config["home_assistant"]
            else self._type == ChannelType.NORMAL
        )

    @property
    def home_assistant(self) -> bool:
        """Indicates if this should be enabled by default in Home Assistant"""
        return self._home_assistant

    @property
    def name(self) -> str:
        return self._name

    @property
    def number(self) -> int:
        return self._number

    @property
    def polarized(self) -> bool:
        return self._polarized

    @property
    def type(self) -> ChannelType:
        return self._type


class ChannelsConfig:
    def __init__(self, channels_config: List[Dict[str, Any]]):
        polarized_channels = ChannelsConfig._get_polarized_channels(channels_config)
        self._channels: dict[int, ChannelConfig] = {
            c["number"]: ChannelConfig(c, c["number"] in polarized_channels)
            for c in channels_config
        }

    def __getitem__(self, key: int) -> ChannelConfig:
        assert key in self._channels
        return self._channels[key]

    def __len__(self) -> int:
        return len(self._channels)

    def __iter__(self) -> Iterator[ChannelConfig]:
        return iter(self._channels.values())

    @staticmethod
    def _get_polarized_channels(channels_config: List[Dict[str, Any]]) -> List[int]:
        polarized_channels: List[int] = []

        # Any MAIN should be polarized if there is a solar channel downstream of it.
        include_main = False
        if ChannelType.SOLAR_DOWNSTREAM_MAIN in [c["type"] for c in channels_config]:
            include_main = True

        for c in channels_config:
            if include_main and c["type"] == ChannelType.MAIN:
                polarized_channels.append(c["number"])

            # Any solar channel should be polarized.
            if (
                c["type"] == ChannelType.SOLAR_DOWNSTREAM_MAIN
                or c["type"] == ChannelType.SOLAR_UPSTREAM_MAIN
            ):
                polarized_channels.append(c["number"])

        return polarized_channels


@unique
class DeviceCOM(Enum):
    COM1 = "COM1"
    COM2 = "COM2"


class DeviceConfig:
    schema = SCHEMA

    def __init__(self, device_config: Dict[str, Any]):
        self._baud = device_config["baud"]
        self._channels = ChannelsConfig(device_config["channels"])
        self._device_com = (
            DeviceCOM.COM1 if device_config["device_com"] == "COM1" else DeviceCOM.COM2
        )
        self._name: str = device_config["name"]
        self._packet_delay_clear_seconds = device_config["packet_delay_clear_seconds"]
        self._send_interval_seconds = device_config["send_interval_seconds"]
        self._type = DeviceType[device_config["type"]]
        self._url = device_config["url"]

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
    def packet_delay_clear_seconds(self) -> int:
        return self._packet_delay_clear_seconds

    @property
    def send_interval_seconds(self) -> int:
        return self._send_interval_seconds

    @property
    def type(self) -> DeviceType:
        return self._type

    @property
    def url(self) -> str:
        """Return pySerial url of the serial device to connect to."""
        return self._url
