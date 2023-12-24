import pytest

from datetime import datetime, timedelta
from typing import Any, AsyncGenerator, Dict, Generator
from unittest.mock import AsyncMock

from siobrultech_protocols.gem.packets import BIN48_NET_TIME, Packet
from brultech_serial2mqtt.config import CONFIG_SCHEMA, Config
from brultech_serial2mqtt.device import DeviceManager


@pytest.fixture()
async def device_manager(
    local_config: Config,
) -> AsyncGenerator[DeviceManager, None]:
    ts = datetime.now()
    first_packet = Packet(
        BIN48_NET_TIME,
        voltage=120.0,
        # In Wh, this is [0, 0, 0, ...]
        absolute_watt_seconds=[0 for _ in range(1, 32)],
        device_id=12,
        serial_number=3456,
        seconds=0,
        pulse_counts=[],
        temperatures=[],
        # In Wh, this is [0, 0, 0, ...]
        polarized_watt_seconds=[0 for _ in range(1, 32)],
        currents=[0 for _ in range(1, 32)],
        time_stamp=ts,
    )

    device_manager = DeviceManager(local_config, first_packet)
    await device_manager.handle_new_packet(
        # A Packet with increased values 10 seconds later.
        Packet(
            BIN48_NET_TIME,
            voltage=120.0,
            # In Wh, this is [1, 2, 3, ...]
            absolute_watt_seconds=[i * 3600 for i in range(1, 32)],
            device_id=12,
            serial_number=3456,
            seconds=10,
            pulse_counts=[],
            temperatures=[],
            # In Wh, this is [0, 1, 2, ...]
            polarized_watt_seconds=[(i - 1) * 3600 for i in range(1, 32)],
            currents=[i / 10 for i in range(1, 32)],
            time_stamp=ts + timedelta(seconds=10),
        ),
        AsyncMock(),
    )
    yield device_manager


@pytest.fixture()
def local_config(
    config: Dict[str, Any],
) -> Generator[Config, None, None]:
    valid_config: Dict[str, Any] = CONFIG_SCHEMA(config)
    yield Config(valid_config)
