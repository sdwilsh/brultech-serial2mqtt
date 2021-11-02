import logging
import os
import shutil
import tempfile
import unittest
from typing import Dict, Union

import yaml

from brultech_serial2mqtt import BrultechSerial2MQTT
from brultech_serial2mqtt.config import load_config
from brultech_serial2mqtt.const import CONFIG_PATH
from tests.test_config import DATA_DIR


class TestLoggingSetup(unittest.TestCase):
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
        self._resetLogger(logging.getLogger("brultech_serial2mqtt"))

    def _setLoggingConfig(
        self, logging_config: Dict[str, Union[str, Dict[str, str]]]
    ) -> None:
        path = os.path.join(self.root.name, CONFIG_PATH)
        with open(path, "r") as config_file:
            config = yaml.load(config_file, Loader=yaml.SafeLoader)
        config["logging"] = logging_config
        with open(path, "w") as config_file:
            yaml.dump(config, config_file)

    def _resetLogger(self, logger: logging.Logger) -> None:
        for h in logger.handlers:
            logger.removeHandler(h)
        logger.setLevel(logging.NOTSET)

    def test_core_logging(self):
        logger = logging.getLogger("brultech_serial2mqtt")
        self.assertNotEqual(logger.level, logging.ERROR)
        self.assertNotIn(logging.StreamHandler, [l.__class__ for l in logger.handlers])

        self._setLoggingConfig({"level": "error"})
        config = load_config(self.root.name).logging
        BrultechSerial2MQTT.setup_logging(config)

        logger = logging.getLogger("brultech_serial2mqtt")
        self.assertEqual(logger.level, logging.ERROR)
        self.assertIn(logging.StreamHandler, [l.__class__ for l in logger.handlers])

    def test_additional_logging(self):
        logger = logging.getLogger("siobrultech_protocols")
        self.assertNotEqual(logger.level, logging.INFO)
        self.assertNotIn(logging.StreamHandler, [l.__class__ for l in logger.handlers])

        self._setLoggingConfig({"logs": {"siobrultech_protocols": "info"}})
        config = load_config(self.root.name).logging
        BrultechSerial2MQTT.setup_logging(config)

        logger = logging.getLogger("siobrultech_protocols")
        self.addCleanup(self._resetLogger, logger)
        self.assertEqual(logger.level, logging.INFO)
        self.assertIn(logging.StreamHandler, [l.__class__ for l in logger.handlers])
