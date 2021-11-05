import unittest
from datetime import datetime
from typing import Any, Dict

from homeassistant.components.mqtt.sensor import DISCOVERY_SCHEMA
from siobrultech_protocols.gem.packets import BIN48_NET_TIME, Packet

from brultech_serial2mqtt.config import CONFIG_SCHEMA, Config
from brultech_serial2mqtt.device import DeviceManager


class TestDiscovery(unittest.TestCase):
    def setUp(self) -> None:
        self.packet = Packet(
            BIN48_NET_TIME,
            voltage=120.0,
            absolute_watt_seconds=[],
            device_id=12,
            serial_number=3456,
            seconds=0,
            pulse_counts=[],
            temperatures=[],
            polarized_watt_seconds=[],
            currents=[],
            time_stamp=datetime.now(),
        )

    def _get_config(self, config: Dict[str, Any]) -> Config:
        valid_config: Dict[str, Any] = CONFIG_SCHEMA(config)
        return Config(valid_config)

    def test_simple_config(self):
        local_config = self._get_config(
            {
                "device": {
                    "channels": [{"number": 1}],
                    "device_com": "COM1",
                    "name": "gem",
                    "url": "/dev/ttyUSB0",
                },
                "mqtt": {"broker": "localhost"},
            }
        )
        m = DeviceManager(local_config, self.packet)
        for discovery_config in m.home_assistant_discovery_config:
            home_assistant_config = {"platform": "mqtt"}
            home_assistant_config.update(discovery_config.config)
            DISCOVERY_SCHEMA(home_assistant_config)

    def test_main_with_downstream_solar_config(self):
        local_config = self._get_config(
            {
                "device": {
                    "channels": [
                        {"number": 1, "type": "main"},
                        {"number": 2, "type": "solar_downstream_main"},
                    ],
                    "device_com": "COM1",
                    "name": "gem",
                    "url": "/dev/ttyUSB0",
                },
                "mqtt": {"broker": "localhost"},
            }
        )
        m = DeviceManager(local_config, self.packet)
        for discovery_config in m.home_assistant_discovery_config:
            home_assistant_config = {"platform": "mqtt"}
            home_assistant_config.update(discovery_config.config)
            DISCOVERY_SCHEMA(home_assistant_config)
