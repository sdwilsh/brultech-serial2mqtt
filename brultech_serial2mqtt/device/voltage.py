from typing import Any, Dict, Set

from siobrultech_protocols.gem.packets import Packet

from brultech_serial2mqtt.config import Config
from brultech_serial2mqtt.device.mqtt import HomeAssistantDiscoveryConfig
from brultech_serial2mqtt.device.sensor import SensorMixin


class Voltage(SensorMixin):
    def __init__(self, config: Config, previous_packet: Packet):
        super().__init__(config.device.name, config.mqtt)
        self._last_packet = previous_packet
        self._unique_id = f"gem_{previous_packet.serial_number}_voltage"
        self._name = f"{config.device.name} Voltage"

    async def handle_new_packet(self, packet: Packet) -> None:
        self._last_packet = packet

    @property
    def state_data(self) -> Dict[str, Any]:
        return {"voltage": self._last_packet.voltage}

    @property
    def _sensor_specific_home_assistant_discovery_config(
        self,
    ) -> Set[HomeAssistantDiscoveryConfig]:
        return {
            HomeAssistantDiscoveryConfig(
                component="sensor",
                config={
                    "device_class": "voltage",
                    "name": f"{self._name} Voltage",
                    "qos": 1,
                    "state_class": "measurement",
                    "unique_id": self._unique_id,
                    "unit_of_measurement": "V",
                    "value_template": (f"{{{{ value_json.voltage }}}}"),
                },
            ),
        }
