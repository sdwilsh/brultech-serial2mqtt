import asyncio
import json
import logging
import pprint
from typing import Any, Dict, Set

from asyncio_mqtt import Client as MQTTClient
from siobrultech_protocols.gem.packets import Packet

from brultech_serial2mqtt.config import Config
from brultech_serial2mqtt.device.channel import ChannelsManager
from brultech_serial2mqtt.device.mqtt import (
    HomeAssistantDiscoveryConfig,
    get_device_state_topic,
)
from brultech_serial2mqtt.device.voltage import Voltage

logger = logging.getLogger(__name__)


class DeviceManager:
    def __init__(self, config: Config, previous_packet: Packet):
        self._channels_manager = ChannelsManager(config, previous_packet)
        self._mqtt_config = config.mqtt
        self._previous_packet = previous_packet
        self._voltage = Voltage(config, previous_packet)

    async def handle_new_packet(self, packet: Packet, mqtt_client: MQTTClient) -> None:
        await asyncio.gather(
            self._voltage.handle_new_packet(packet),
            self._channels_manager.handle_new_packet(packet),
        )
        self._previous_packet = packet

        try:
            await self._publish_packet(packet, mqtt_client)
        except Exception as exc:
            logger.exception(
                "Exception caught while attempting to publish a packet!",
                exc,
            )

    async def _publish_packet(
        self,
        packet: Packet,
        mqtt_client: MQTTClient,
    ) -> None:
        state: Dict[str, Any] = {}
        state.update(self.state_data)
        json_state = json.dumps(state, indent=2)
        topic = get_device_state_topic(packet, self._mqtt_config)
        await mqtt_client.publish(
            topic=topic,
            payload=json_state,
            qos=self._mqtt_config.qos,
        )
        logger.debug(f"Published packet data to {topic}:\n{pprint.pformat(state)}")

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
        configs: Set[HomeAssistantDiscoveryConfig] = set()
        for c in self._voltage.home_assistant_discovery_configs(self._previous_packet):
            configs.add(c)
        for c in self._channels_manager.home_assistant_discovery_configs:
            configs.add(c)
        return configs
