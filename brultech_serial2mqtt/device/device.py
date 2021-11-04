from siobrultech_protocols.gem.packets import Packet

from brultech_serial2mqtt.config.config_mqtt import MQTTConfig


def get_device_state_topic(packet: Packet, mqtt_config: MQTTConfig) -> str:
    return f"{mqtt_config.topic_prefix}/gem_{packet.serial_number}/state"
