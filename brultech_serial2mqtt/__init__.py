from __future__ import annotations

import asyncio
import logging
import pprint
from typing import Optional

from aiobrultech_serial import Connection as DeviceConnection
from asyncio_mqtt import Client as MQTTClient
from siobrultech_protocols.gem.packets import Packet as DevicePacket
from siobrultech_protocols.gem.packets import PacketFormatType as DevicePacketFormatType

from brultech_serial2mqtt.config import load_config
from brultech_serial2mqtt.config.config_device import DeviceCOM
from brultech_serial2mqtt.device.channel import ChannelsManager

logger = logging.getLogger(__name__)


class BrultechSerial2MQTT:
    def __init__(self):
        self._config = load_config()
        self._first_packet: asyncio.Future[DevicePacket] = asyncio.Future()
        self._last_packet: Optional[DevicePacket] = None

        logger.setLevel(self._config.logging.level.value)

    async def start(self) -> None:
        """Starts listening to the serial connection and publishes packets to MQTT"""
        async with DeviceConnection(
            port=self._config.device.url, baudrate=self._config.device.baud
        ) as device_connection:

            await self._setup_gem(device_connection)

            async with MQTTClient(
                hostname=self._config.mqtt.broker,
                port=self._config.mqtt.port,
                username=self._config.mqtt.username,
                password=self._config.mqtt.password,
                client_id=self._config.mqtt.client_id,
            ) as mqtt_client:
                async for packet in device_connection.packets():
                    await self._handle_packet(packet, mqtt_client)

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
            self._config.device.packet_send_interval_seconds
        )
        logger.info("Setup of GEM device complete!")

    async def _publish_home_assistant_discovery_config(
        self, mqtt_client: MQTTClient
    ) -> None:
        if not self._config.mqtt.home_assistant.enable:
            logger.info(
                "Home Assistant dicovery configuration is disabled.  Not publishing configuration."
            )
            return

        async def publish_discovery_config() -> None:
            logger.debug(
                "Waiting for first packet to publish Home Assistant dicovery configuration..."
            )
            packet = await self._first_packet
            configs = ChannelsManager(
                self._config, packet
            ).home_assistant_discovery_config()
            try:
                for config in configs:
                    await mqtt_client.publish(
                        topic=f"{self._config.mqtt.home_assistant.discovery_prefix}/{config.component}/{config.object_id}/config",
                        payload=config.config,
                    )
                    logger.info(
                        f"Published Home Assistant dicovery configuration for a {config.component} identified by {config.object_id}"
                    )
                    logger.debug(
                        f"Configuration for {config.component} identified by {config.object_id}:\n{pprint.pformat(config.config)}"
                    )
            except Exception as exc:
                logger.exception(
                    "Exception caught while attempting to publish Home Assistant discovery configuration!",
                    exc,
                )

        asyncio.create_task(publish_discovery_config())

    async def _handle_packet(
        self, packet: DevicePacket, mqtt_client: MQTTClient
    ) -> None:
        if not self._first_packet.done():
            self._first_packet.set_result(packet)
            self._last_packet = packet
            return

        try:
            await self._publish_packet(packet, mqtt_client)
        except Exception as exc:
            logger.exception(
                "Exception caught while attempting to publish a packet!",
                exc,
            )
        self._last_packet = packet

    async def _publish_packet(
        self, packet: DevicePacket, mqtt_client: MQTTClient
    ) -> None:
        pass
