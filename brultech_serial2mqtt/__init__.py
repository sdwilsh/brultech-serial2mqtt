from __future__ import annotations

import logging
from contextlib import AsyncExitStack
from datetime import timedelta
from typing import Optional

from aiobrultech_serial import Connection as DeviceConnection
from aiomqtt import Client as MqttClient
from siobrultech_protocols.gem.packets import (
    Packet as DevicePacket,
    PacketFormatType as DevicePacketFormatType,
)

from brultech_serial2mqtt.config import load_config
from brultech_serial2mqtt.config.config_device import DeviceCOM, DeviceType
from brultech_serial2mqtt.config.config_logging import LoggingConfig
from brultech_serial2mqtt.device import DeviceManager
from brultech_serial2mqtt import mqtt

logger = logging.getLogger(__name__)


class BrultechSerial2MQTT:
    _most_recent_packet: Optional[DevicePacket] = None

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
            sub_logger = logging.getLogger(logger_name)
            sub_logger.addHandler(stream_handler)
            sub_logger.setLevel(level.value)

    async def start(self) -> None:
        """Starts listening to the serial connection and publishes packets to MQTT"""
        async with DeviceConnection(
            api_type=self._config.device.type,
            baudrate=self._config.device.baud,
            packet_delay_clear_time=timedelta(
                seconds=self._config.device.packet_delay_clear_seconds
            ),
            port=self._config.device.url,
        ) as device_connection:
            await self._setup_device(device_connection)

            packets = device_connection.packets()

            logger.info("Waiting for first packet to finish setup...")
            first_packet = await packets.__anext__()
            logger.debug(f"Received new packet:\n{first_packet}")
            device_manager = DeviceManager(self._config, first_packet)

            logger.debug(f"Connecting to MQTT broker at {self._config.mqtt.broker}")
            async with AsyncExitStack() as stack:
                mqtt_client: MqttClient = await stack.enter_async_context(
                    mqtt.get_client(self._config.mqtt, first_packet.serial_number)
                )
                task = await mqtt.manage_home_assistant_lifecycle(
                    self._config.mqtt,
                    mqtt_client,
                    device_manager,
                    lambda: self.most_recent_packet or first_packet,
                )
                if task is not None:
                    stack.callback(lambda: task.cancel())

                await mqtt.publish_birth_message(
                    self._config.mqtt, mqtt_client, first_packet.serial_number
                )

                # Set the packet count such that we will send the first packet to Home Assistant.
                packet_count = self._config.mqtt.home_assistant.skip_packets + 1
                async for packet in device_connection.packets():
                    logger.debug(f"Received new packet:\n{packet}")
                    self._most_recent_packet = packet
                    packet_count += 1
                    if packet_count <= self._config.mqtt.home_assistant.skip_packets:
                        logger.debug(
                            "Skipping packet #%d because we are supposed to skip every %d packets",
                            packet_count,
                            self._config.mqtt.home_assistant.skip_packets,
                        )
                        continue

                    if not await mqtt.publish_packet(
                        mqtt_client, device_manager, packet
                    ):
                        break

                    # Reset the packet_count now that we have published.
                    packet_count = 0

    @property
    def most_recent_packet(self) -> Optional[DevicePacket]:
        return self._most_recent_packet

    async def _setup_device(self, connection: DeviceConnection) -> None:
        logger.info(f"Setting up {self._config.device.type.name} device...")

        if self._config.device.type == DeviceType.GEM:
            logger.debug("Synchronizing device clock with machine")
            await connection.synchronize_time()
            logger.debug("Setting the correct packet format on the device")
            if self._config.device.device_com == DeviceCOM.COM1:
                await connection.set_packet_format(
                    DevicePacketFormatType.BIN48_NET_TIME
                )
            else:
                await connection.set_secondary_packet_format(
                    DevicePacketFormatType.BIN48_NET_TIME
                )

        logger.debug("Setting the packet send interval on the device")
        await connection.set_packet_send_interval(
            self._config.device.send_interval_seconds
        )

        logger.info(f"Setup of {self._config.device.type.name} device complete!")
