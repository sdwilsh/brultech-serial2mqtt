import asyncio
import logging
import pprint

from aiomqtt import Client as MQTTClient
from aiomqtt.error import MqttError
from brultech_serial2mqtt.config import MQTTConfig
from brultech_serial2mqtt.device import DeviceManager

logger = logging.getLogger(__name__)


async def publish_birth_message(
    config: MQTTConfig, mqtt_client: MQTTClient, device_serial: int
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
    config: MQTTConfig, mqtt_client: MQTTClient, device_manager: DeviceManager
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
