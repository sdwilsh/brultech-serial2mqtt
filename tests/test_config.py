import os
import shutil
import tempfile
import unittest

from brultech_serial2mqtt.config import load_config
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
        self.assertEqual(config.device.channels[1].name, "channel_1")
        self.assertFalse(config.device.channels[1].net_metered)
        self.assertEqual(config.device.channels[1].number, 1)
        self.assertEqual(config.device.url, "/dev/ttyUSB0")

        self.assertEqual(config.mqtt.broker, "localhost")
        self.assertEqual(config.mqtt.client_id, "brultech-serial2mqtt")
        self.assertEqual(config.mqtt.port, 1883)
        self.assertIsNone(config.mqtt.password)
        self.assertEqual(config.mqtt.topic_prefix, "brultech-serial2mqtt")
        self.assertIsNone(config.mqtt.username)

        self.assertTrue(config.mqtt.home_assistant.enable)
        self.assertEqual(config.mqtt.home_assistant.discovery_prefix, "homeassistant")
