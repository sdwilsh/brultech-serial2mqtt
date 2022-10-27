import os
import shutil
import ssl
import tempfile
import unittest
from typing import Any, Dict, List, Union

import yaml
from asyncio_mqtt import TLSParameters as MqttTlsParams
from voluptuous.error import MultipleInvalid

from brultech_serial2mqtt.config import load_config
from brultech_serial2mqtt.config.config_device import ChannelType, DeviceCOM
from brultech_serial2mqtt.config.config_logging import LogLevel
from brultech_serial2mqtt.const import CONFIG_PATH

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "configs")


class TestSimpleConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tempfile.TemporaryDirectory(prefix=__class__.__name__)
        config_dir = os.path.join(self.root.name, os.path.dirname(CONFIG_PATH))
        os.mkdir(config_dir)
        shutil.copyfile(
            os.path.join(DATA_DIR, "simple_config.yml"),
            os.path.join(self.root.name, CONFIG_PATH),
        )

    def tearDown(self) -> None:
        self.root.cleanup()

    def test_load(self):
        config = load_config(self.root.name)

        self.assertEqual(config.device.baud, 115200)
        self.assertEqual(len(config.device.channels), 1)
        self.assertTrue(config.device.channels[1].home_assistant)
        self.assertEqual(config.device.channels[1].name, "Channel 1")
        self.assertEqual(config.device.channels[1].number, 1)
        self.assertEqual(config.device.channels[1].type, ChannelType.NORMAL)
        self.assertEqual(config.device.device_com, DeviceCOM.COM1)
        self.assertEqual(config.device.name, "gem")
        self.assertEqual(config.device.send_interval_seconds, 8)
        self.assertEqual(config.device.url, "/dev/ttyUSB0")

        self.assertEqual(config.logging.level, LogLevel.INFO)
        self.assertEqual(config.mqtt.broker, "localhost")
        self.assertEqual(config.mqtt.client_id(123), "brultech-serial2mqtt-123")
        self.assertEqual(config.mqtt.port, 1883)
        self.assertIsNone(config.mqtt.password)
        self.assertEqual(config.mqtt.qos, 0)
        self.assertEqual(config.mqtt.state_topic(123), "brultech-serial2mqtt-123/state")
        self.assertEqual(
            config.mqtt.status_topic(123), "brultech-serial2mqtt-123/status"
        )
        self.assertEqual(config.mqtt.topic_prefix(123), "brultech-serial2mqtt-123")
        self.assertIsNone(config.mqtt.username)
        self.assertEqual(config.mqtt.usetls, False)
        self.assertEqual(config.mqtt.birth_message.payload, "online")
        self.assertEqual(config.mqtt.birth_message.qos, 0)
        self.assertTrue(config.mqtt.birth_message.retain)
        self.assertEqual(config.mqtt.will_message.payload, "offline")
        self.assertEqual(config.mqtt.will_message.qos, 0)
        self.assertTrue(config.mqtt.will_message.retain)

        self.assertEqual(config.mqtt.home_assistant.birth_message.payload, "online")
        self.assertEqual(config.mqtt.home_assistant.birth_message.qos, 0)
        self.assertEqual(
            config.mqtt.home_assistant.birth_message.topic, "homeassistant/status"
        )
        self.assertEqual(config.mqtt.home_assistant.discovery_prefix, "homeassistant")
        self.assertTrue(config.mqtt.home_assistant.enable)
        self.assertEqual(config.mqtt.home_assistant.skip_packets, 37)


class TestChannelConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tempfile.TemporaryDirectory(prefix=__class__.__name__)
        config_dir = os.path.join(self.root.name, os.path.dirname(CONFIG_PATH))
        os.mkdir(config_dir)
        shutil.copyfile(
            os.path.join(DATA_DIR, "simple_config.yml"),
            os.path.join(self.root.name, CONFIG_PATH),
        )

    def tearDown(self) -> None:
        self.root.cleanup()

    def _setChannelConfig(self, channels_config: List[Dict[str, Any]]) -> None:
        path = os.path.join(self.root.name, CONFIG_PATH)
        with open(path, "r") as config_file:
            config = yaml.load(config_file, Loader=yaml.SafeLoader)
        config["device"]["channels"] = channels_config
        with open(path, "w") as config_file:
            yaml.dump(config, config_file)

    def test_polarized_main(self):
        self._setChannelConfig(
            [
                {"number": 1, "type": "main"},
                {"number": 2, "type": "solar_downstream_main"},
            ]
        )
        config = load_config(self.root.name).device.channels
        self.assertFalse(config[1].home_assistant)
        self.assertTrue(config[1].polarized)
        self.assertFalse(config[2].home_assistant)
        self.assertTrue(config[2].polarized)

    def test_unpolarized_main(self):
        self._setChannelConfig([{"number": 1, "type": "main"}])
        config = load_config(self.root.name).device.channels
        self.assertFalse(config[1].home_assistant)
        self.assertFalse(config[1].polarized)


class TestLoggingConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tempfile.TemporaryDirectory(prefix=__class__.__name__)
        config_dir = os.path.join(self.root.name, os.path.dirname(CONFIG_PATH))
        os.mkdir(config_dir)
        shutil.copyfile(
            os.path.join(DATA_DIR, "simple_config.yml"),
            os.path.join(self.root.name, CONFIG_PATH),
        )

    def tearDown(self) -> None:
        self.root.cleanup()

    def _setLoggingConfig(
        self, logging_config: Dict[str, Union[str, Dict[str, str]]]
    ) -> None:
        path = os.path.join(self.root.name, CONFIG_PATH)
        with open(path, "r") as config_file:
            config = yaml.load(config_file, Loader=yaml.SafeLoader)
        config["logging"] = logging_config
        with open(path, "w") as config_file:
            yaml.dump(config, config_file)

    def test_valid_level(self):
        for level in LogLevel:
            self._setLoggingConfig({"level": level.name})
            config = load_config(self.root.name)
            self.assertEqual(config.logging.level, level)

    def test_invalid_level(self):
        self._setLoggingConfig({"level": "notareallevel"})
        with self.assertRaises(MultipleInvalid):
            load_config(self.root.name)

    def test_additional_logging(self):
        self._setLoggingConfig({"logs": {"siobrultech_protocols": "info"}})
        config = load_config(self.root.name).logging
        self.assertDictEqual(config.logs, {"siobrultech_protocols": LogLevel.INFO})


class TestTlsConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tempfile.TemporaryDirectory(prefix=__class__.__name__)
        config_dir = os.path.join(self.root.name, os.path.dirname(CONFIG_PATH))
        os.mkdir(config_dir)
        shutil.copyfile(
            os.path.join(DATA_DIR, "simple_config.yml"),
            os.path.join(self.root.name, CONFIG_PATH),
        )

    def tearDown(self) -> None:
        self.root.cleanup()

    def _setTlsConfig(self, usetls: bool, tls_options: Dict[str, Any] = {}) -> None:
        path = os.path.join(self.root.name, CONFIG_PATH)
        with open(path, "r") as config_file:
            config = yaml.load(config_file, Loader=yaml.SafeLoader)
        config["mqtt"]["usetls"] = usetls
        config["mqtt"]["tls_options"] = tls_options
        with open(path, "w") as config_file:
            yaml.dump(config, config_file)

    def test_no_tls(self):
        self._setTlsConfig(False, {"tls_version": "tls1.1"})
        config = load_config(self.root.name).mqtt
        self.assertFalse(config.usetls)
        self.assertIsNone(config.tls_params)

    def test_default_tls(self):
        self._setTlsConfig(True)
        config = load_config(self.root.name).mqtt
        self.assertTrue(config.usetls)
        self.assertIsInstance(config.tls_params, MqttTlsParams)

    def test_tls_v11(self):
        self._setTlsConfig(True, {"tls_version": "tls1.1"})
        config = load_config(self.root.name).mqtt
        self.assertIsInstance(config.tls_params, MqttTlsParams)
        self.assertEqual(config.tls_params.tls_version, ssl.PROTOCOL_TLSv1_1)  # type: ignore
