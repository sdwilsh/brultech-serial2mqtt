import asyncio
from typing import Any, Coroutine, Dict, List

from siobrultech_protocols.gem.packets import Packet

from brultech_serial2mqtt.config import Config
from brultech_serial2mqtt.device.device import DeviceSensorMixin
from brultech_serial2mqtt.device.mqtt import HomeAssistantDiscoveryConfig


class Channel(DeviceSensorMixin):
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

        if self._last_packet.polarized_watt_seconds is not None:
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
    ) -> List[HomeAssistantDiscoveryConfig]:
        # Future improvements: Power
        entities = [
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
                        f"{{{{ (value_json.channel_{self._channel_config.number}.absolute_watt_seconds / 60) | round }}}}"
                    ),
                },
            ),
        ]
        if self._channel_config.polarized:
            entities.append(
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
                            f"{{{{ (value_json.channel_{self._channel_config.number}.polarized_watt_seconds / 60) | round }}}}"
                        ),
                    },
                )
            )
        if self._last_packet.currents is not None:
            entities.append(
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


class ChannelsManager:
    def __init__(self, config: Config, previous_packet: Packet):
        self._channels = {
            Channel(config, c_conf.number, previous_packet)
            for c_conf in config.device.channels
        }
        self._previous_packet = previous_packet

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
    ) -> List[HomeAssistantDiscoveryConfig]:
        """The sensor(s) for Home Assistant MQTT Discovery."""
        configs = []
        for c in self._channels:
            configs.extend(c.home_assistant_discovery_config(self._previous_packet))
        return configs
