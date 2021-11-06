import asyncio
from typing import Any, Dict, Set

from siobrultech_protocols.gem.packets import Packet

from brultech_serial2mqtt.config import Config
from brultech_serial2mqtt.device.channel import ChannelsManager
from brultech_serial2mqtt.device.mqtt import HomeAssistantDiscoveryConfig
from brultech_serial2mqtt.device.voltage import Voltage


class DeviceManager:
    def __init__(self, config: Config, previous_packet: Packet):
        self._voltage = Voltage(config, previous_packet)
        self._channels_manager = ChannelsManager(config, previous_packet)
        self._previous_packet = previous_packet

    async def handle_new_packet(self, packet: Packet) -> None:
        await asyncio.gather(
            self._voltage.handle_new_packet(packet),
            self._channels_manager.handle_new_packet(packet),
        )
        self._previous_packet = packet

    @property
    def state_data(self) -> Dict[str, Dict[str, Any]]:
        states = self._voltage.state_data
        states.update(self._channels_manager.state_data)
        return states

    @property
    def home_assistant_discovery_configs(
        self,
    ) -> Set[HomeAssistantDiscoveryConfig]:
        """The sensor(s) for Home Assistant MQTT Discovery."""
        configs = set()
        for c in self._voltage.home_assistant_discovery_configs(self._previous_packet):
            configs.add(c)
        for c in self._channels_manager.home_assistant_discovery_configs:
            configs.add(c)
        return configs
