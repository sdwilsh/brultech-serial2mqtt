import functools
import logging
import pytest
from brultech_serial2mqtt.device.channel import ChannelsManager
from brultech_serial2mqtt.config import Config
from siobrultech_protocols.gem import packets

LOGGER_NAME: str = "brultech_serial2mqtt.device.channel"

packet_maker = functools.partial(
    packets.Packet,
    packet_format=packets.BIN32_ABS,
    voltage=120.0,
    absolute_watt_seconds=[0] * packets.BIN32_NET.num_channels,
    device_id=123456,
    serial_number=123456,
    seconds=0,
    pulse_counts=[0] * packets.GEMPacketFormat.NUM_PULSE_COUNTERS,
    temperatures=list([0.0] * packets.GEMPacketFormat.NUM_TEMPERATURE_SENSORS),
    aux=None,
)


@pytest.mark.parametrize(
    "config",
    [
        {
            "device": {
                "channels": [{"number": 32}],
                "device_com": "COM1",
                "name": "gem",
            },
            "mqtt": {"broker": "localhost"},
        },
    ],
)
def test_skip_configured_channel_not_in_packet(
    caplog: pytest.LogCaptureFixture,
    local_config: Config,
):
    with caplog.at_level(logging.ERROR, LOGGER_NAME):
        manager = ChannelsManager(
            local_config, packet_maker(packet_format=packets.ECM_1240)
        )
        assert len(manager.channels) == 0
        assert caplog.record_tuples == [
            (
                LOGGER_NAME,
                logging.ERROR,
                "Exception while setting up channel 32; skipping!",
            )
        ]
