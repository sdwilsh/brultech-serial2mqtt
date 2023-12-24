import pytest

from typing import Any, AsyncGenerator, Dict, Generator
from unittest.mock import AsyncMock

from brultech_serial2mqtt.config import CONFIG_SCHEMA, Config
from brultech_serial2mqtt.device import DeviceManager
from tests import packets
from siobrultech_protocols.gem.packets import Packet


@pytest.fixture()
def packet_generator() -> Generator[Generator[Packet, None, None], None, None]:
    yield packets.packet_generator()


@pytest.fixture()
async def device_manager(
    local_config: Config,
    packet_generator: Generator[Packet, None, None],
) -> AsyncGenerator[DeviceManager, None]:
    first_packet = next(packet_generator)

    device_manager = DeviceManager(local_config, first_packet)
    await device_manager.handle_new_packet(
        next(packet_generator),
        AsyncMock(),
    )
    yield device_manager


@pytest.fixture()
def local_config(
    config: Dict[str, Any],
) -> Generator[Config, None, None]:
    valid_config: Dict[str, Any] = CONFIG_SCHEMA(config)
    yield Config(valid_config)
