import abc
from typing import Any, Dict, List

from siobrultech_protocols.gem.packets import Packet

from brultech_serial2mqtt.config.config_mqtt import MQTTConfig
from brultech_serial2mqtt.const import HOME_ASSISTANT_DOMAIN
from brultech_serial2mqtt.device.mqtt import HomeAssistantDiscoveryConfig


def get_device_state_topic(packet: Packet, mqtt_config: MQTTConfig) -> str:
    return f"{mqtt_config.topic_prefix}/gem_{packet.serial_number}/state"


class DeviceSensorMixin:
    def __init__(self, device_name: str, mqtt_config: MQTTConfig):
        self._device_name = device_name
        self._mqtt_config = mqtt_config

    def home_assistant_discovery_config(
        self, packet: Packet
    ) -> List[HomeAssistantDiscoveryConfig]:
        """The sensor(s) for Home Assistant MQTT Discovery."""
        common = {
            "device": {
                "identifiers": [
                    ",".join((HOME_ASSISTANT_DOMAIN, f"serial-{packet.serial_number}")),
                    ",".join((HOME_ASSISTANT_DOMAIN, f"device_id-{packet.device_id}")),
                ],
                "manufacturer": "Brultech Research Inc.",
                "model": "GreenEye Monitor",
                "name": self._device_name,
            },
            "state_topic": get_device_state_topic(packet, self._mqtt_config),
        }
        configs = []
        for config in self._sensor_specific_home_assistant_discovery_config:
            config.apply_common_config(common)
            configs.append(config)
        return configs

    @property
    @abc.abstractmethod
    def state_data(self) -> Dict[str, Any]:
        pass

    @property
    @abc.abstractmethod
    def _sensor_specific_home_assistant_discovery_config(
        self,
    ) -> List[HomeAssistantDiscoveryConfig]:
        pass
