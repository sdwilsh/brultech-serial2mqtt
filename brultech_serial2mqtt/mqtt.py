import asyncio
import logging
import pprint

from asyncio.tasks import Task
from typing import Awaitable, Callable, Optional

from aiomqtt import Client
from aiomqtt.error import MqttError
from brultech_serial2mqtt.config import MQTTConfig
from brultech_serial2mqtt.device import DeviceManager

logger = logging.getLogger(__name__)


async def manage_home_assistant_lifecycle(
    config: MQTTConfig, mqtt_client: Client, device_manager: DeviceManager
) -> Optional[Task[None]]:
    if not config.home_assistant.enable:
        logger.info(
            "Home Assistant dicovery configuration is disabled.  Not publishing configuration."
        )
        return None

    async def _on_birth() -> None:
        logger.debug(
            "Home Assistant has re-connected to the mqtt server.  Resending discovery configuration..."
        )
        await asyncio.create_task(
            publish_home_assistant_discovery_config(config, mqtt_client, device_manager)
        )

    await publish_home_assistant_discovery_config(config, mqtt_client, device_manager)
    return asyncio.create_task(
        subscribe_to_home_assistant_birth(config, mqtt_client, _on_birth)
    )


async def publish_birth_message(
    config: MQTTConfig, mqtt_client: Client, device_serial: int
) -> None:
    logger.info(
        f"Notifying clients that we are online on {config.status_topic(device_serial)}"
    )
    await mqtt_client.publish(
        payload=config.birth_message.payload,
        qos=config.birth_message.qos,
        retain=config.birth_message.retain,
        topic=config.status_topic(device_serial),
    )


async def publish_home_assistant_discovery_config(
    config: MQTTConfig, mqtt_client: Client, device_manager: DeviceManager
) -> None:
    try:
        for discovery_config in device_manager.home_assistant_discovery_configs:
            topic = discovery_config.get_discovery_topic(
                config.home_assistant.discovery_prefix
            )
            await mqtt_client.publish(
                topic=topic,
                payload=discovery_config.json_config,
            )
            logger.info(
                f"Published Home Assistant dicovery configuration for a {discovery_config.component} identified by {discovery_config.object_id} to {topic}"
            )
            logger.debug(
                f"Configuration for {discovery_config.component} identified by {discovery_config.object_id}:\n{pprint.pformat(discovery_config.config)}"
            )
    except asyncio.CancelledError:
        pass
    except MqttError as exc:
        logger.debug(
            "MqttError while attempting to publish Home Assistant dicovery configuration!",
            exc_info=exc,
        )
    except Exception as exc:
        logger.exception(
            "Exception caught while attempting to publish Home Assistant discovery configuration!",
            exc_info=exc,
        )


async def subscribe_to_home_assistant_birth(
    config: MQTTConfig, mqtt_client: Client, on_birth: Callable[[], Awaitable[None]]
) -> None:
    try:
        async with mqtt_client.messages() as messages:
            await mqtt_client.subscribe(
                config.home_assistant.birth_message.topic,
                qos=config.home_assistant.birth_message.qos,
            )
            async for message in messages:
                if (
                    message.topic.matches(config.home_assistant.birth_message.topic)
                    and message.payload == config.home_assistant.birth_message.payload
                ):
                    await on_birth()
    except asyncio.CancelledError:
        pass
    except MqttError as exc:
        logger.debug(
            "MqttError while listenting/publishing for Home Assistant birth!",
            exc_info=exc,
        )
    except Exception as exc:
        logger.exception(
            "Exception caught while listenting/publishing for Home Assistant birth!",
            exc_info=exc,
        )
