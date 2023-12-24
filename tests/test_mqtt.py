import pytest

from typing import cast, Generator
from unittest.mock import ANY, call, patch, Mock

from brultech_serial2mqtt import mqtt
from brultech_serial2mqtt.config import Config, MQTTConfig
from brultech_serial2mqtt.device import DeviceManager


@pytest.fixture()
def mqtt_config(local_config: Config) -> Generator[MQTTConfig, None, None]:
    yield local_config.mqtt


@pytest.mark.parametrize(
    "config",
    [
        {
            "device": {
                "channels": [{"number": 1}],
                "device_com": "COM1",
                "name": "gem",
            },
            "mqtt": {
                "broker": "localhost",
                "home_assistant": {
                    "enable": False,
                },
            },
        },
    ],
)
async def test_manage_home_assistant_lifecyle_disabled(
    mqtt_config: MQTTConfig, device_manager: DeviceManager
) -> None:
    with patch("brultech_serial2mqtt.mqtt.Client", autospec=True):
        client = mqtt.get_client(mqtt_config, 42)
        task = await mqtt.manage_home_assistant_lifecycle(
            mqtt_config, client, device_manager
        )
        assert task is None


@pytest.mark.parametrize(
    "config",
    [
        {
            "device": {
                "channels": [{"number": 1}],
                "device_com": "COM1",
                "name": "gem",
            },
            "mqtt": {
                "broker": "localhost",
            },
        },
    ],
)
async def test_manage_home_assistant_lifecyle_enabled(
    mqtt_config: MQTTConfig, device_manager: DeviceManager
) -> None:
    with patch("brultech_serial2mqtt.mqtt.Client", autospec=True):
        client = mqtt.get_client(mqtt_config, 42)
        task = await mqtt.manage_home_assistant_lifecycle(
            mqtt_config, client, device_manager
        )
        assert task is not None
        await task
        mock_client = cast(Mock, client)
        mock_client.publish.assert_has_calls(
            [
                call(
                    topic="homeassistant/sensor/gem_3456_channel_1_energy/config",
                    payload=ANY,
                ),
                call(
                    topic="homeassistant/sensor/gem_3456_channel_1_current/config",
                    payload=ANY,
                ),
                call(
                    topic="homeassistant/sensor/gem_3456_channel_1_power/config",
                    payload=ANY,
                ),
                call(topic="homeassistant/sensor/gem_3456_voltage/config", payload=ANY),
            ],
            any_order=True,
        )
        assert mock_client.publish.call_count == 4
        mock_client.subscribe.assert_called_once_with("homeassistant/status", qos=0)
