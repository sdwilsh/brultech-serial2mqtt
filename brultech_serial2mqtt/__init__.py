import logging

from aiobrultech_serial import Connection as DeviceConnection
from asyncio_mqtt import Client as MQTTClient
from siobrultech_protocols.gem.packets import Packet as DevicePacket
from siobrultech_protocols.gem.packets import PacketFormatType as DevicePacketFormatType

from brultech_serial2mqtt.config import load_config
from brultech_serial2mqtt.config.config_device import DeviceCOM

logger = logging.getLogger(__name__)


class BrultechSerial2MQTT:
    def __init__(self):
        self.config = load_config()

    async def start(self) -> None:
        """Starts listening to the serial connection and publishes packets to MQTT"""
        async with DeviceConnection(
            port=self.config.device.url, baudrate=self.config.device.baud
        ) as device_connection:

            await self._setup_gem(device_connection)

            async with MQTTClient(
                hostname=self.config.mqtt.broker,
                port=self.config.mqtt.port,
                username=self.config.mqtt.username,
                password=self.config.mqtt.password,
                client_id=self.config.mqtt.client_id,
            ) as mqtt_client:
                async for packet in device_connection.packets():
                    try:
                        await self._publish_packet(packet, mqtt_client)
                    except Exception as exc:
                        logger.exception(
                            "Exception caught while attempting to publish a packet!",
                            exc,
                        )

    async def _setup_gem(self, connection: DeviceConnection) -> None:
        await connection.synchronize_time()
        if self.config.device.device_com == DeviceCOM.COM1:
            await connection.set_packet_format(DevicePacketFormatType.BIN48_NET_TIME)
        else:
            await connection.set_secondary_packet_format(
                DevicePacketFormatType.BIN48_NET_TIME
            )
        await connection.set_packet_send_interval(
            self.config.device.packet_send_interval_seconds
        )

    async def _publish_packet(
        self, packet: DevicePacket, mqtt_client: MQTTClient
    ) -> None:
        pass
