import asyncio
import logging
import pytest
import subprocess

from asyncio import TaskGroup
from contextlib import asynccontextmanager
from typing import AsyncGenerator, cast, Generator, Set
from unittest.mock import ANY, call, patch, Mock

from aiomqtt import Client
from aiomqtt.client import Message
from brultech_serial2mqtt import mqtt
from brultech_serial2mqtt.config import Config, MQTTConfig
from brultech_serial2mqtt.device import DeviceManager
from pytest import FixtureRequest
from siobrultech_protocols.gem.packets import Packet

logger = logging.getLogger(__name__)


@pytest.fixture()
def home_assistant_client(
    mqtt_config: MQTTConfig,
    request: FixtureRequest,
) -> Generator[Client, None, None]:
    yield Client(
        client_id=request.function.__name__[:23],
        hostname=mqtt_config.broker,
        port=mqtt_config.port,
    )


@pytest.fixture()
def mosquitto_image() -> Generator[str, None, None]:
    # Build the image for tests.
    docker_output = subprocess.run(
        [
            "docker",
            "build",
            "-q",
            "tests/docker",
            "-f",
            "tests/docker/Docker.eclipse-mosquitto",
        ],
        capture_output=True,
        check=True,
        text=True,
    )
    sha = docker_output.stdout.strip()
    yield sha

    # Cleanup the Image
    subprocess.run(
        [
            "docker",
            "image",
            "rm",
            sha,
        ],
    )


@pytest.fixture()
def mqtt_config(local_config: Config) -> Generator[MQTTConfig, None, None]:
    yield local_config.mqtt


@pytest.fixture
def mqtt_server(
    mosquitto_image: str,
    mqtt_config: MQTTConfig,
) -> Generator[str, None, None]:
    # Start the container
    port = str(mqtt_config.port)
    docker_output = subprocess.run(
        [
            "docker",
            "run",
            "--detach",
            "--rm",
            "--publish",
            f"1883:{port}",
            mosquitto_image,
        ],
        capture_output=True,
        check=True,
        text=True,
    )
    container_id = docker_output.stdout.strip()

    # Wait for the container to be healthy
    while True:
        docker_output = subprocess.run(
            [
                "docker",
                "inspect",
                "-f",
                "{{.State.Health.Status}}",
                container_id,
            ],
            capture_output=True,
            check=True,
            text=True,
        )
        if docker_output.stdout.strip() == "healthy":
            break
    yield container_id

    # Log any container output for debugging.
    docker_output = subprocess.run(
        [
            "docker",
            "logs",
            container_id,
        ],
        capture_output=True,
        text=True,
    )
    logger.debug(docker_output.stdout.strip())

    # Cleanup the container
    subprocess.run(
        [
            "docker",
            "stop",
            container_id,
        ],
    )


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
    mqtt_config: MQTTConfig,
    device_manager: DeviceManager,
    packet_generator: Generator[Packet, None, None],
) -> None:
    with patch("brultech_serial2mqtt.mqtt.Client", autospec=True):
        client = mqtt.get_client(mqtt_config, 42)
        async with TaskGroup() as task_group:
            await mqtt.manage_home_assistant_lifecycle(
                task_group,
                mqtt_config,
                client,
                device_manager,
                lambda: next(packet_generator),
            )
        mock_client = cast(Mock, client)
        mock_client.publish.assert_not_called()


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
    mqtt_config: MQTTConfig,
    device_manager: DeviceManager,
    packet_generator: Generator[Packet, None, None],
) -> None:
    with patch("brultech_serial2mqtt.mqtt.Client", autospec=True):
        client = mqtt.get_client(mqtt_config, 42)
        async with TaskGroup() as task_group:
            await mqtt.manage_home_assistant_lifecycle(
                task_group,
                mqtt_config,
                client,
                device_manager,
                lambda: next(packet_generator),
            )
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
    mqtt_config: MQTTConfig,
    device_manager: DeviceManager,
    packet_generator: Generator[Packet, None, None],
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
        async with TaskGroup() as task_group:
            await mqtt.manage_home_assistant_lifecycle(
                task_group,
                mqtt_config,
                client,
                device_manager,
                lambda: next(packet_generator),
            )
            mock_client = cast(Mock, client)
            mock_client.publish.reset_mock()
            assert mock_client.publish.call_count == 0
            mock_client.messages.side_effect = _messages

        # Exiting the task group means the subscribe happened!
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
                call(
                    payload=ANY,
                    qos=mqtt_config.qos,
                    topic=mqtt_config.state_topic(device_manager.serial_number),
                ),
            ],
            any_order=True,
        )
        assert mock_client.publish.call_count == 6


@pytest.mark.enable_socket
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
                "broker": "127.0.0.1",
            },
        },
    ],
)
async def test_integration_manage_home_assistant_birth_message_sends_discovery(
    home_assistant_client: Client,
    mqtt_config: MQTTConfig,
    mqtt_server: None,
    device_manager: DeviceManager,
    packet_generator: Generator[Packet, None, None],
) -> None:
    EXPECTED_TOPICS = {
        f"{mqtt_config.home_assistant.discovery_prefix}/sensor/gem_3456_channel_1_energy/config",
        f"{mqtt_config.home_assistant.discovery_prefix}/sensor/gem_3456_channel_1_current/config",
        f"{mqtt_config.home_assistant.discovery_prefix}/sensor/gem_3456_channel_1_power/config",
        f"{mqtt_config.home_assistant.discovery_prefix}/sensor/gem_3456_voltage/config",
    }

    seen_topics: Set[str] = set()
    async with TaskGroup() as task_group:
        async with home_assistant_client as hass_client:
            async with mqtt.get_client(mqtt_config, 42) as test_client:
                # Setup Lifecycle
                lifecycle_task = await mqtt.manage_home_assistant_lifecycle(
                    task_group,
                    mqtt_config,
                    test_client,
                    device_manager,
                    lambda: next(packet_generator),
                )
                assert lifecycle_task is not None

                async def _waitForDiscoveryMessages() -> None:
                    async with hass_client.messages() as received_messages:
                        async for message in received_messages:
                            logger.debug(
                                f"Home Asssistant client has received topic `{
                                    message.topic.value}`",
                            )
                            if message.topic.matches(
                                mqtt_config.home_assistant.birth_message.topic
                            ):
                                continue
                            seen_topics.add(message.topic.value)
                            if len(seen_topics) == len(EXPECTED_TOPICS):
                                lifecycle_task.cancel()
                                return

                # Subscribe to discovery prefix messages.
                await hass_client.subscribe(
                    mqtt_config.home_assistant.discovery_prefix + "/#"
                )

                # Birth Home Assitant
                await hass_client.publish(
                    mqtt_config.home_assistant.birth_message.topic,
                    payload=mqtt_config.home_assistant.birth_message.payload,
                )

                await asyncio.wait_for(_waitForDiscoveryMessages(), timeout=60.0)

    for topic in seen_topics:
        assert topic in EXPECTED_TOPICS
