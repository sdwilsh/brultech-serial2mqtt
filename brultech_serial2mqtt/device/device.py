import abc
from copy import deepcopy
from typing import List

from siobrultech_protocols.gem.packets import Packet

from brultech_serial2mqtt.config.config_mqtt import MQTTConfig
from brultech_serial2mqtt.const import HOME_ASSISTANT_DOMAIN


class DeviceSensorMixin:
    def __init__(self, mqtt_config: MQTTConfig):
        self._mqtt_config = mqtt_config

    def _get_unique_id_from_packet(self, packet: Packet) -> str:
        return f"gem_{packet.device_id}"

    def _get_last_reset_topic(self, packet: Packet) -> str:
        return f"{self._mqtt_config.topic_prefix}/{self._get_unique_id_from_packet(packet)}/last_reset"

    def _get_state_topic(self, packet: Packet) -> str:
        return f"{self._mqtt_config.topic_prefix}/{self._get_unique_id_from_packet(packet)}/state"

    async def home_assistant_discovery_config(self, packet: Packet) -> List[dict]:
        """The sensor(s) for Home Assistant MQTT Discovery."""
        common = {
            "device": {
                "identifiers": [
                    (HOME_ASSISTANT_DOMAIN, f"serial-{packet.serial_number}"),
                    (HOME_ASSISTANT_DOMAIN, f"device_id-{packet.device_id}"),
                ],
                "manufacturer": "Brultech Research Inc.",
                "model": "GreenEye Monitor",
            },
            "last_reset_topic": self._get_last_reset_topic(packet),
            "state_topic": self._get_state_topic(packet),
        }
        configs = []
        for config in self._sensor_specific_home_assistant_discovery_config():
            sensor_config = deepcopy(common)
            sensor_config.update(config)
        return configs

    @abc.abstractmethod
    def state_data(self) -> dict:
        pass

    @abc.abstractmethod
    def _sensor_specific_home_assistant_discovery_config(self) -> List[dict]:
        pass
