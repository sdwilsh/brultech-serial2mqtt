import abc
from typing import Any, Dict, Set

from siobrultech_protocols.gem.packets import Packet

from brultech_serial2mqtt.config.config_mqtt import MQTTConfig
from brultech_serial2mqtt.const import HOME_ASSISTANT_DOMAIN
from brultech_serial2mqtt.device.mqtt import HomeAssistantDiscoveryConfig


class SensorMixin:
    def __init__(self, device_name: str, mqtt_config: MQTTConfig):
        self._device_name = device_name
        self._mqtt_config = mqtt_config

    def home_assistant_discovery_configs(
        self, packet: Packet
    ) -> Set[HomeAssistantDiscoveryConfig]:
        """The sensor(s) for Home Assistant MQTT Discovery."""
        common = {
            "availability": [
                {
                    "payload_available": self._mqtt_config.birth_message.payload,
                    "topic": self._mqtt_config.birth_message.topic(
                        packet.serial_number
                    ),
                },
                {
                    "payload_not_available": self._mqtt_config.will_message.payload,
                    "topic": self._mqtt_config.will_message.topic(packet.serial_number),
                },
            ],
            "device": {
                "identifiers": [
                    ",".join((HOME_ASSISTANT_DOMAIN, f"serial-{packet.serial_number}")),
                    ",".join((HOME_ASSISTANT_DOMAIN, f"device_id-{packet.device_id}")),
                ],
                "manufacturer": "Brultech Research Inc.",
                "model": "GreenEye Monitor",
                "name": self._device_name,
            },
            "state_topic": self._mqtt_config.state_topic(packet.serial_number),
        }
        configs: Set[HomeAssistantDiscoveryConfig] = set()
        for config in self._sensor_specific_home_assistant_discovery_configs:
            config.apply_common_config(common)
            configs.add(config)
        return configs

    @abc.abstractmethod
    async def handle_new_packet(self, packet: Packet) -> None:
        pass

    @property
    @abc.abstractmethod
    def state_data(self) -> Dict[str, Any]:
        pass

    @property
    @abc.abstractmethod
    def _sensor_specific_home_assistant_discovery_configs(
        self,
    ) -> Set[HomeAssistantDiscoveryConfig]:
        pass
