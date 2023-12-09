import asyncio
import functools
import logging
from enum import Enum, unique
from typing import Any, Coroutine, Dict, List, Literal, Set, Tuple

from siobrultech_protocols.gem.packets import Packet

from brultech_serial2mqtt.config import Config
from brultech_serial2mqtt.config.config_device import ChannelConfig, ChannelType
from brultech_serial2mqtt.device.mqtt import HomeAssistantDiscoveryConfig
from brultech_serial2mqtt.device.sensor import SensorMixin


logger = logging.getLogger(__name__)


class ConfigException(Exception):
    def __init__(self, message: str, config: ChannelConfig):
        super().__init__(f"{message} channel_config={config}")


class Channel(SensorMixin):
    def __init__(self, config: Config, channel_num: int, previous_packet: Packet):
        super().__init__(config.device.name, config.mqtt)
        self._average_power = 0.0
        self._channel_config = config.device.channels[channel_num]
        self._last_packet = previous_packet
        self._mqtt_config = config.mqtt
        self._unique_id_base = (
            f"gem_{previous_packet.serial_number}_channel_{channel_num}"
        )
        self._name_root = config.device.channels[channel_num].name

        if channel_num > previous_packet.num_channels:
            raise ConfigException(
                "Channel configured but not available in packet!", self._channel_config
            )

    async def handle_new_packet(self, packet: Packet) -> None:
        self._average_power = self._last_packet.get_average_power(
            self._channel_index,
            packet,
        )
        self._last_packet = packet

    @property
    def _channel_index(self) -> int:
        # Channel numbers are 1-based, but list index is 0-based
        return self._channel_config.number - 1

    @property
    def config(self) -> ChannelConfig:
        return self._channel_config

    @property
    def state_data(self) -> Dict[str, Any]:
        state: Dict[str, Any] = {
            "absolute_watt_seconds": self._last_packet.absolute_watt_seconds[
                self._channel_index
            ],
            "power": self._average_power,
        }

        if self._last_packet.currents is not None:
            state.update({"current": self._last_packet.currents[self._channel_index]})

        if self._channel_config.polarized:
            assert self._last_packet.polarized_watt_seconds is not None
            state.update(
                {
                    "polarized_watt_seconds": self._last_packet.polarized_watt_seconds[
                        self._channel_index
                    ],
                }
            )

        return {f"channel_{self._channel_config.number}": state}

    @property
    def _sensor_specific_home_assistant_discovery_configs(
        self,
    ) -> Set[HomeAssistantDiscoveryConfig]:
        entities: Set[HomeAssistantDiscoveryConfig] = {
            HomeAssistantDiscoveryConfig(
                component="sensor",
                config={
                    "enabled_by_default": self.config.home_assistant,
                    "device_class": "power",
                    "name": f"{self._name_root} Power",
                    "qos": 1,
                    "state_class": "measurement",
                    "unique_id": f"{self._unique_id_base}_power",
                    "unit_of_measurement": "W",
                    "value_template": (
                        f"{{{{ value_json.channel_{self._channel_config.number}.power }}}}"
                    ),
                },
            ),
        }
        if self._channel_config.polarized:
            entities.add(
                HomeAssistantDiscoveryConfig(
                    component="sensor",
                    config={
                        "enabled_by_default": self.config.home_assistant,
                        "device_class": "energy",
                        "name": f"{self._name_root} Absolute Energy",
                        "qos": 1,
                        "state_class": "total_increasing",
                        "unique_id": f"{self._unique_id_base}_absolute_energy",
                        "unit_of_measurement": "Wh",
                        "value_template": (
                            f"{{{{ (value_json.channel_{self._channel_config.number}.absolute_watt_seconds / 3600) | round }}}}"
                        ),
                    },
                ),
            )
            entities.add(
                HomeAssistantDiscoveryConfig(
                    component="sensor",
                    config={
                        "enabled_by_default": self.config.home_assistant,
                        "device_class": "energy",
                        "name": f"{self._name_root} Polarized Energy",
                        "qos": 1,
                        "state_class": "total_increasing",
                        "unique_id": f"{self._unique_id_base}_polarized_energy",
                        "unit_of_measurement": "Wh",
                        "value_template": (
                            f"{{{{ (value_json.channel_{self._channel_config.number}.polarized_watt_seconds / 3600) | round }}}}"
                        ),
                    },
                ),
            )
        else:
            entities.add(
                HomeAssistantDiscoveryConfig(
                    component="sensor",
                    config={
                        "enabled_by_default": self.config.home_assistant,
                        "device_class": "energy",
                        "name": f"{self._name_root} Energy",
                        "qos": 1,
                        "state_class": "total_increasing",
                        "unique_id": f"{self._unique_id_base}_energy",
                        "unit_of_measurement": "Wh",
                        "value_template": (
                            f"{{{{ (value_json.channel_{self._channel_config.number}.absolute_watt_seconds / 3600) | round }}}}"
                        ),
                    },
                ),
            )

        if self._last_packet.currents is not None:
            entities.add(
                HomeAssistantDiscoveryConfig(
                    component="sensor",
                    config={
                        "enabled_by_default": self.config.home_assistant,
                        "device_class": "current",
                        "name": f"{self._name_root} Current",
                        "qos": 1,
                        "state_class": "measurement",
                        "unique_id": f"{self._unique_id_base}_current",
                        "unit_of_measurement": "A",
                        "value_template": f"{{{{ value_json.channel_{self._channel_config.number}.current }}}}",
                    },
                ),
            )
        return entities


@unique
class ChannelValueType(Enum):
    ABSOLUTE = "absolute"
    POLARIZED = "polarized"


class AggregatedEnergyChannel(SensorMixin):
    def __init__(
        self,
        config: Config,
        name_root: str,
        unique_id_root: str,
        channel_combination: List[Tuple[Literal["+", "-"], Set[int], ChannelValueType]],
        reference_packet: Packet,
    ):
        super().__init__(config.device.name, config.mqtt)
        self._name_root = name_root
        self._unique_id_root = f"gem_{reference_packet.serial_number}_{unique_id_root}"
        self._channel_combination = channel_combination
        self._total_channels = functools.reduce(
            lambda v, t: v + len(t[1]), channel_combination, 0
        )

    async def handle_new_packet(self, packet: Packet) -> None:
        pass

    @property
    def state_data(self) -> Dict[str, Any]:
        raise Exception("not implemented; should use real channel data to compute!")

    @property
    def _sensor_specific_home_assistant_discovery_configs(
        self,
    ) -> Set[HomeAssistantDiscoveryConfig]:
        entities: Set[HomeAssistantDiscoveryConfig] = set()
        if self._total_channels == 0:
            return entities

        entities.add(
            HomeAssistantDiscoveryConfig(
                component="sensor",
                config={
                    "device_class": "energy",
                    "name": f"{self._name_root} Energy",
                    "qos": 1,
                    "state_class": "total_increasing",
                    "unique_id": f"{self._unique_id_root}_energy",
                    "unit_of_measurement": "Wh",
                    "value_template": f"{self._energy_value_template}",
                },
            ),
        )

        return entities

    @property
    def _energy_value_template(self) -> str:
        parts = "0 "
        for operator, channel_numbers, type in self._channel_combination:
            for channel_number in channel_numbers:
                field = "absolute" if type == ChannelValueType.ABSOLUTE else "polarized"
                parts += f" {operator} value_json.channel_{channel_number}.{field}_watt_seconds"

        return f"{{{{ (({parts}) / 3600) | round }}}}"


class ChannelsManager:
    def __init__(self, config: Config, previous_packet: Packet):
        self._channels: Set[Channel] = set()
        for c_conf in config.device.channels:
            try:
                self._channels.add(Channel(config, c_conf.number, previous_packet))
            except ConfigException:
                logger.exception(
                    f"Exception while setting up channel {c_conf.number}; skipping!"
                )

        self._previous_packet = previous_packet
        self._aggregate_channels = self._get_aggregate_channels(config)

    async def handle_new_packet(self, packet: Packet) -> None:
        updates: List[Coroutine[None, None, None]] = []
        for c in self._channels:
            updates.append(c.handle_new_packet(packet))
        await asyncio.gather(*updates)
        self._previous_packet = packet

    @property
    def channels(self) -> Set[Channel]:
        return self._channels

    @property
    def state_data(self) -> Dict[str, Dict[str, Any]]:
        states: Dict[str, Dict[str, Any]] = {}
        for c in self._channels:
            states.update(c.state_data)
        return states

    @property
    def home_assistant_discovery_configs(
        self,
    ) -> Set[HomeAssistantDiscoveryConfig]:
        """The sensor(s) for Home Assistant MQTT Discovery."""
        configs: Set[HomeAssistantDiscoveryConfig] = set()
        for channel in self._channels:
            for config in channel.home_assistant_discovery_configs(
                self._previous_packet
            ):
                configs.add(config)

        for channel in self._aggregate_channels:
            for config in channel.home_assistant_discovery_configs(
                self._previous_packet
            ):
                configs.add(config)

        return configs

    def _get_aggregate_channels(self, config: Config) -> Set[AggregatedEnergyChannel]:
        channels_by_type: Dict[ChannelType, Set[Channel]] = {}
        for t in ChannelType:
            channels_by_type[t] = set()
        for c in self._channels:
            channels_by_type[c.config.type].add(c)

        main = {c.config.number for c in channels_by_type[ChannelType.MAIN]}
        solar_downstream = {
            c.config.number for c in channels_by_type[ChannelType.SOLAR_DOWNSTREAM_MAIN]
        }
        solar_upstream = {
            c.config.number for c in channels_by_type[ChannelType.SOLAR_UPSTREAM_MAIN]
        }

        channels: Set[AggregatedEnergyChannel] = set()

        # Solar Production
        channels.add(
            AggregatedEnergyChannel(
                config=config,
                name_root="Solar Production",
                unique_id_root="solar_production",
                channel_combination=[
                    ("+", solar_downstream, ChannelValueType.POLARIZED),
                    ("+", solar_upstream, ChannelValueType.POLARIZED),
                ],
                reference_packet=self._previous_packet,
            )
        )

        # Grid Consumption
        channels.add(
            AggregatedEnergyChannel(
                config=config,
                name_root="Grid Consumption",
                unique_id_root="grid_consumed",
                channel_combination=[
                    ("+", main, ChannelValueType.ABSOLUTE),  # to/from utility
                    ("-", main, ChannelValueType.POLARIZED),  # to utility
                    (
                        "+",
                        solar_upstream,
                        ChannelValueType.ABSOLUTE,
                    ),  # to/from utility
                    (
                        "-",
                        solar_upstream,
                        ChannelValueType.POLARIZED,
                    ),  # to utility
                ],
                reference_packet=self._previous_packet,
            )
        )

        # Return to Grid
        channels.add(
            AggregatedEnergyChannel(
                config=config,
                name_root="Return to Grid",
                unique_id_root="grid_returned",
                channel_combination=[
                    ("+", main, ChannelValueType.POLARIZED),
                    (
                        "+",
                        solar_upstream,
                        ChannelValueType.POLARIZED,
                    ),
                ],
                reference_packet=self._previous_packet,
            )
        )

        return channels
