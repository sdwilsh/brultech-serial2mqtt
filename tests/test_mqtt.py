import pytest

from contextlib import asynccontextmanager
from typing import AsyncGenerator, cast, Generator
from unittest.mock import ANY, call, patch, Mock

from aiomqtt.client import Message
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
async def test_manage_home_assistant_lifecyle_birth_message_sends_discovery(
    mqtt_config: MQTTConfig, device_manager: DeviceManager
) -> None:
    BIRTH_MESSAGE = Message(
        topic=mqtt_config.home_assistant.birth_message.topic,
        payload=mqtt_config.home_assistant.birth_message.payload,
        qos=mqtt_config.home_assistant.birth_message.qos,
        retain=False,
        mid=42,
        properties=None,
    )

    async def _only_birth_message() -> AsyncGenerator[Message, None]:
        yield BIRTH_MESSAGE

    @asynccontextmanager
    async def _messages():
        yield _only_birth_message()

    with patch("brultech_serial2mqtt.mqtt.Client", autospec=True):
        client = mqtt.get_client(mqtt_config, 42)
        task = await mqtt.manage_home_assistant_lifecycle(
            mqtt_config, client, device_manager
        )
        assert task is not None
        mock_client = cast(Mock, client)
        mock_client.publish.reset_mock()
        assert mock_client.publish.call_count == 0
        mock_client.messages.side_effect = _messages

        await task  # This subscribes and reads messages!
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
                call(
                    payload=mqtt_config.birth_message.payload,
                    qos=mqtt_config.birth_message.qos,
                    retain=mqtt_config.birth_message.retain,
                    topic=mqtt_config.status_topic(device_manager.serial_number),
                ),
            ],
            any_order=True,
        )
        assert mock_client.publish.call_count == 5
