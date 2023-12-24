from datetime import datetime, timedelta
from typing import Generator
from siobrultech_protocols.gem.packets import BIN48_NET_TIME, Packet


def packet_generator(seconds_to_increment: int = 10) -> Generator[Packet, None, None]:
    ts = datetime.now()
    packet = Packet(
        BIN48_NET_TIME,
        voltage=120.0,
        # In Wh, this is [1, 2, 3, ...]
        absolute_watt_seconds=[i * 3600 for i in range(1, 32)],
        device_id=12,
        serial_number=3456,
        seconds=0,
        pulse_counts=[],
        temperatures=[],
        # In Wh, this is always one less than the absolute watt seconds
        polarized_watt_seconds=[i * 3600 - 3600 for i in range(1, 32)],
        currents=[i / seconds_to_increment for i in range(1, 32)],
        time_stamp=ts,
    )
    yield packet

    while True:
        packet = Packet(
            BIN48_NET_TIME,
            voltage=120.0,
            # In Wh, this increments by one for each new packet.
            absolute_watt_seconds=[v + 3600 for v in packet.absolute_watt_seconds],
            device_id=packet.device_id,
            serial_number=packet.serial_number,
            seconds=seconds_to_increment,
            pulse_counts=[],
            temperatures=[],
            # In Wh, this is always one less than the absolute watt seconds
            polarized_watt_seconds=[v - 3600 for v in packet.absolute_watt_seconds],
            currents=[
                round(v + 1 / seconds_to_increment, 1) for v in packet.currents or []
            ],
            time_stamp=ts + timedelta(seconds=seconds_to_increment),
        )
        yield packet
