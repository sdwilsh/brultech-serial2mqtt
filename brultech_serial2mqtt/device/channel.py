import asyncio
from typing import Any, Coroutine, Dict, List, Set

from siobrultech_protocols.gem.packets import Packet

from brultech_serial2mqtt.config import Config
from brultech_serial2mqtt.config.config_device import ChannelConfig, ChannelType
from brultech_serial2mqtt.device.mqtt import HomeAssistantDiscoveryConfig
from brultech_serial2mqtt.device.sensor import SensorMixin


class Channel(SensorMixin):
    def __init__(self, config: Config, channel_num: int, previous_packet: Packet):
        super().__init__(config.device.name, config.mqtt)
        self._channel_config = config.device.channels[channel_num]
        self._last_packet = previous_packet
        self._mqtt_config = config.mqtt
        self._unique_id_base = (
            f"gem_{previous_packet.serial_number}_channel_{channel_num}"
        )
        self._name = f"{config.device.name} {config.device.channels[channel_num].name}"

    async def handle_new_packet(self, packet: Packet) -> None:
        self._last_packet = packet

    @property
    def config(self) -> ChannelConfig:
        return self._channel_config

    @property
    def state_data(self) -> Dict[str, Any]:
        # Channel numbers are 1-based, but list index is 0-based
        channel_index = self._channel_config.number - 1
        state: Dict[str, Any] = {
            "absolute_watt_seconds": self._last_packet.absolute_watt_seconds[
                channel_index
            ],
        }

        if self._last_packet.currents is not None:
            state.update({"current": self._last_packet.currents[channel_index]})

        if self._channel_config.polarized:
            assert self._last_packet.polarized_watt_seconds is not None
            state.update(
                {
                    "polarized_watt_seconds": self._last_packet.polarized_watt_seconds[
                        channel_index
                    ],
                }
            )

        return {f"channel_{self._channel_config.number}": state}

    @property
    def _sensor_specific_home_assistant_discovery_config(
        self,
    ) -> Set[HomeAssistantDiscoveryConfig]:
        # Future improvements: Power
        entities = set()
        if self._channel_config.polarized:
            entities.add(
                HomeAssistantDiscoveryConfig(
                    component="sensor",
                    config={
                        "device_class": "energy",
                        "name": f"{self._name} Absolute Energy",
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
                        "device_class": "energy",
                        "name": f"{self._name} Polarized Energy",
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
                        "device_class": "energy",
                        "name": f"{self._name} Energy",
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
                        "device_class": "current",
                        "name": f"{self._name} Current",
                        "qos": 1,
                        "state_class": "measurement",
                        "unique_id": f"{self._unique_id_base}_current",
                        "unit_of_measurement": "A",
                        "value_template": f"{{{{ value_json.channel_{self._channel_config.number}.current }}}}",
                    },
                ),
            )
        return entities


class AggregatedEnergyChannel(SensorMixin):
    def __init__(
        self,
        config: Config,
        name: str,
        unique_id: str,
        value_template: str,
        reference_packet: Packet,
    ):
        super().__init__(config.device.name, config.mqtt)
        self._name = f"{config.device.name} {name}"
        self._unique_id = f"gem_{reference_packet.serial_number}_{unique_id}"
        self._value_template = value_template

    async def handle_new_packet(self, packet: Packet) -> None:
        pass

    @property
    def state_data(self) -> Dict[str, Any]:
        raise Exception("not implemented; should use real channel data to compute!")

    @property
    def _sensor_specific_home_assistant_discovery_config(
        self,
    ) -> Set[HomeAssistantDiscoveryConfig]:
        return {
            HomeAssistantDiscoveryConfig(
                component="sensor",
                config={
                    "device_class": "energy",
                    "name": f"{self._name}",
                    "qos": 1,
                    "state_class": "total_increasing",
                    "unique_id": f"{self._unique_id}",
                    "unit_of_measurement": "Wh",
                    "value_template": f"{self._value_template}",
                },
            ),
        }


class ChannelsManager:
    def __init__(self, config: Config, previous_packet: Packet):
        self._channels = {
            Channel(config, c_conf.number, previous_packet)
            for c_conf in config.device.channels
        }
        self._previous_packet = previous_packet
        self._aggregate_channels = self._get_aggregate_channels(config)

    async def handle_new_packet(self, packet: Packet) -> None:
        updates: List[Coroutine[None, None, None]] = []
        for c in self._channels:
            updates.append(c.handle_new_packet(packet))
        await asyncio.gather(*updates)
        self._previous_packet = packet

    @property
    def state_data(self) -> Dict[str, Dict[str, Any]]:
        states = {}
        for c in self._channels:
            states.update(c.state_data)
        return states

    @property
    def home_assistant_discovery_config(
        self,
    ) -> Set[HomeAssistantDiscoveryConfig]:
        """The sensor(s) for Home Assistant MQTT Discovery."""
        configs = set()
        for channel in self._channels:
            for config in channel.home_assistant_discovery_config(
                self._previous_packet
            ):
                configs.add(config)

        for channel in self._aggregate_channels:
            for config in channel.home_assistant_discovery_config(
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

        main_absolute = " + ".join(
            [
                f"value_json.channel_{c.config.number}.absolute_watt_seconds"
                for c in channels_by_type[ChannelType.MAIN]
            ]
        )
        main_polarized = " + ".join(
            [
                f"value_json.channel_{c.config.number}.polarized_watt_seconds"
                for c in channels_by_type[ChannelType.MAIN]
            ]
        )
        solar_downstream_polarized = " + ".join(
            [
                f"value_json.channel_{c.config.number}.polarized_watt_seconds"
                for c in channels_by_type[ChannelType.SOLAR_DOWNSTREAM_MAIN]
            ]
        )

        channels = set()
        if (
            len(channels_by_type[ChannelType.MAIN]) > 0
            and len(channels_by_type[ChannelType.SOLAR_DOWNSTREAM_MAIN]) > 0
            and len(channels_by_type[ChannelType.SOLAR_UPSTREAM_MAIN]) == 0
        ):
            # Grid consumption of main power looks like this:
            # main_absolute + solar_polarized - main_polarized
            channels.add(
                AggregatedEnergyChannel(
                    config=config,
                    name="Grid Consumption",
                    unique_id="grid_consumed_energy",
                    value_template=f"{{{{ ((({main_absolute}) + ({solar_downstream_polarized}) - ({main_polarized})) / 3600) | round }}}}",
                    reference_packet=self._previous_packet,
                )
            )
            # Return to grid looks like this:
            # main_absolute - main_polarized
            channels.add(
                AggregatedEnergyChannel(
                    config=config,
                    name="Return to Grid",
                    unique_id="grid_returned_energy",
                    value_template=f"{{{{ ((({main_absolute}) - ({main_polarized})) / 3600) | round }}}}",
                    reference_packet=self._previous_packet,
                )
            )

        return channels
