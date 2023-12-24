import logging

from aiomqtt import Client as MQTTClient
from brultech_serial2mqtt.config import MQTTConfig

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
