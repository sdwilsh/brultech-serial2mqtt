from __future__ import annotations

import asyncio
import logging
import pprint
from asyncio.tasks import Task
from contextlib import AsyncExitStack
from typing import Optional

from aiobrultech_serial import Connection as DeviceConnection
from asyncio_mqtt import Client as MQTTClient
from asyncio_mqtt.client import Will
from asyncio_mqtt.error import MqttError
from siobrultech_protocols.gem.packets import PacketFormatType as DevicePacketFormatType

from brultech_serial2mqtt.config import load_config
from brultech_serial2mqtt.config.config_device import DeviceCOM
from brultech_serial2mqtt.config.config_logging import LoggingConfig
from brultech_serial2mqtt.device import DeviceManager

logger = logging.getLogger(__name__)


class BrultechSerial2MQTT:
    def __init__(self):
        self._config = load_config()

        BrultechSerial2MQTT.setup_logging(self._config.logging)

    @classmethod
    def setup_logging(cls, config: LoggingConfig) -> None:
        """Sets up logging based on the specified logging."""
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(stream_handler)
        logger.setLevel(config.level.value)
        for logger_name, level in config.logs.items():
            l = logging.getLogger(logger_name)
            l.addHandler(stream_handler)
            l.setLevel(level.value)

    async def start(self) -> None:
        """Starts listening to the serial connection and publishes packets to MQTT"""
        async with DeviceConnection(
            port=self._config.device.url, baudrate=self._config.device.baud
        ) as device_connection:

            await self._setup_gem(device_connection)

            packets = device_connection.packets()

            logger.info("Waiting for first packet to finish setup...")
            first_packet = await packets.__anext__()
            device_manager = DeviceManager(self._config, first_packet)

            logger.debug(f"Connecting to MQTT broker at {self._config.mqtt.broker}")
            async with AsyncExitStack() as stack:
                mqtt_client: MQTTClient = await stack.enter_async_context(
                    MQTTClient(
                        client_id=self._config.mqtt.client_id(
                            first_packet.serial_number
                        ),
                        hostname=self._config.mqtt.broker,
                        password=self._config.mqtt.password,
                        port=self._config.mqtt.port,
                        tls_params=self._config.mqtt.tls_params,
                        username=self._config.mqtt.username,
                        will=Will(
                            payload=self._config.mqtt.will_message.payload,
                            qos=self._config.mqtt.will_message.qos,
                            retain=self._config.mqtt.will_message.retain,
                            topic=self._config.mqtt.status_topic(
                                first_packet.serial_number
                            ),
                        ),
                    )
                )
                task = await self._publish_home_assistant_discovery_config(
                    mqtt_client, device_manager
                )
                if not task is None:
                    stack.callback(lambda: task.cancel())

                await self._publish_birth_message(
                    mqtt_client, first_packet.serial_number
                )

                # Set the packet count such that we will send the first packet to Home Assistant.
                packet_count = self._config.mqtt.home_assistant.skip_packets + 1
                async for packet in device_connection.packets():
                    packet_count += 1
                    if packet_count <= self._config.mqtt.home_assistant.skip_packets:
                        logger.debug(
                            "Skipping packet #%d because we are supposed to skip every %d packets",
                            packet_count,
                            self._config.mqtt.home_assistant.skip_packets,
                        )
                        continue
                    else:
                        packet_count = 0
                    try:
                        await device_manager.handle_new_packet(packet, mqtt_client)
                    except MqttError as exc:
                        logger.exception(
                            "MqttError while handling a new packet!",
                            exc_info=exc,
                        )
                        break

    async def _setup_gem(self, connection: DeviceConnection) -> None:
        logger.info("Setting up GEM device...")
        logger.debug("Synchronizing GEM clock with local device")
        await connection.synchronize_time()
        logger.debug("Setting the correct packet format on the GEM device")
        if self._config.device.device_com == DeviceCOM.COM1:
            await connection.set_packet_format(DevicePacketFormatType.BIN48_NET_TIME)
        else:
            await connection.set_secondary_packet_format(
                DevicePacketFormatType.BIN48_NET_TIME
            )
        logger.debug("Setting the packet send interval on the GEM device")
        await connection.set_packet_send_interval(
            self._config.device.send_interval_seconds
        )
        logger.info("Setup of GEM device complete!")

    async def _publish_home_assistant_discovery_config(
        self, mqtt_client: MQTTClient, device_manager: DeviceManager
    ) -> Optional[Task[None]]:
        if not self._config.mqtt.home_assistant.enable:
            logger.info(
                "Home Assistant dicovery configuration is disabled.  Not publishing configuration."
            )
            return None

        async def publish_discovery_config() -> None:
            try:
                for config in device_manager.home_assistant_discovery_configs:
                    topic = config.get_discovery_topic(
                        self._config.mqtt.home_assistant.discovery_prefix
                    )
                    await mqtt_client.publish(
                        topic=topic,
                        payload=config.json_config,
                    )
                    logger.info(
                        f"Published Home Assistant dicovery configuration for a {config.component} identified by {config.object_id} to {topic}"
                    )
                    logger.debug(
                        f"Configuration for {config.component} identified by {config.object_id}:\n{pprint.pformat(config.config)}"
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

        async def subscribe_to_home_assistant_birth() -> None:
            try:
                async with mqtt_client.filtered_messages(
                    self._config.mqtt.home_assistant.birth_message.topic
                ) as messages:  # type: ignore https://github.com/sbtinstruments/asyncio-mqtt/issues/100
                    await mqtt_client.subscribe(
                        self._config.mqtt.home_assistant.birth_message.topic,
                        qos=self._config.mqtt.home_assistant.birth_message.qos,
                    )
                    async for message in messages:  # type: ignore https://github.com/sbtinstruments/asyncio-mqtt/issues/100
                        if (
                            message.payload.decode()
                            == self._config.mqtt.home_assistant.birth_message.payload
                        ):
                            logger.debug(
                                "Home Assistant has re-connected to the mqtt server.  Resending discovery configuration..."
                            )
                            await asyncio.create_task(publish_discovery_config())
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

        await publish_discovery_config()
        return asyncio.create_task(subscribe_to_home_assistant_birth())

    async def _publish_birth_message(
        self, mqtt_client: MQTTClient, device_serial: int
    ) -> None:
        logger.info(
            f"Notifying clients that we are online on {self._config.mqtt.status_topic(device_serial)}"
        )
        await mqtt_client.publish(
            payload=self._config.mqtt.birth_message.payload,
            qos=self._config.mqtt.birth_message.qos,
            retain=self._config.mqtt.birth_message.retain,
            topic=self._config.mqtt.status_topic(device_serial),
        )
