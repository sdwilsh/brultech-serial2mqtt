import asyncio
from typing import List

from asyncio_mqtt import Client as MQTTClient
from siobrultech_protocols.gem.packets import Packet

from brultech_serial2mqtt.config import Config
from brultech_serial2mqtt.device.device import DeviceSensorMixin
from brultech_serial2mqtt.device.mqtt import HomeAssistantDiscoveryConfig


class Channel(DeviceSensorMixin):
    def __init__(self, config: Config, channel_num: int, previous_packet: Packet):
        super().__init__(config.mqtt)
        self._channel_config = config.device.channels[channel_num]
        self._last_packet = previous_packet
        self._mqtt_config = config.mqtt
        self._unique_id = (
            f"{config.device.name}_{config.device.channels[channel_num].name}"
        )

    async def handle_packet(self, new_packet: Packet, mqtt_client: MQTTClient) -> None:
        await asyncio.gather(self._handle_packet_for_energy(new_packet, mqtt_client))
        self._last_packet = new_packet

    async def _handle_packet_for_energy(
        self, new_packet: Packet, mqtt_client: MQTTClient
    ) -> None:
        reset_time = None
        # Absolute watt-seconds always goes up!  However, polarized watt-seconds does
        # not.  Ideally, we'd send a serial command `RSTC` with the channel number to
        # reset both when we detect this regardless of net metering.  This is rare, so
        # it is left as a future improvement. See:
        # https://www.brultech.com/community/viewtopic.php?f=29&t=599&p=2566
        if (
            not self._channel_config.net_metered
            and self._last_packet.absolute_watt_seconds
            > new_packet.absolute_watt_seconds
        ):
            reset_time = self._last_packet.absolute_watt_seconds

        if reset_time is not None:
            await mqtt_client.publish(
                self._get_last_reset_topic(new_packet),
                payload={self._last_packet.time_stamp.isoformat()},
                qos=1,
                retain=True,
            )

    @property
    def state_data(self) -> dict:
        state = {
            "absolute_watt_seconds": self._last_packet.absolute_watt_seconds[
                self._channel_config.number
            ],
        }
        if self._channel_config.net_metered:
            pws = self._last_packet.polarized_watt_seconds
            assert pws is not None
            state.update(
                {
                    "net_watt_seconds": pws[self._channel_config.number],
                }
            )
        return {self._channel_config.name: state}

    def _sensor_specific_home_assistant_discovery_config(
        self,
    ) -> List[HomeAssistantDiscoveryConfig]:
        return [
            # Future improvements: Current, Power
            HomeAssistantDiscoveryConfig(
                component="sensor",
                object_id=self._unique_id,
                config={
                    "device_class": "energy",
                    "last_reset_value_template": f"as_timestamp(value_json)",
                    "qos": 1,
                    "state_class": (
                        "total"
                        if self._channel_config.net_metered
                        else "total_increasing"
                    ),
                    "unique_id": self._unique_id,
                    "unit_of_measurement": "Ws",
                    "value_template": (
                        f"value_json.{self._channel_config.name}.net_watt_seconds"
                        if self._channel_config.net_metered
                        else f"value_json.{self._channel_config.name}.absolute_watt_seconds"
                    ),
                },
            ),
        ]

    def _get_last_reset_topic(self, packet: Packet) -> str:
        return f"{super()._get_last_reset_topic(packet)}/{self._channel_config.name}"


class ChannelsManager:
    def __init__(self, config: Config, previous_packet: Packet):
        self.channels = [
            Channel(config, c_conf.number, previous_packet)
            for c_conf in config.device.channels
        ]
        self._previous_packet = previous_packet

    def home_assistant_discovery_config(
        self,
    ) -> List[HomeAssistantDiscoveryConfig]:
        """The sensor(s) for Home Assistant MQTT Discovery."""
        configs = []
        for c in self.channels:
            configs.extend(c.home_assistant_discovery_config(self._previous_packet))
        return configs
