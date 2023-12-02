from datetime import datetime, timedelta
from typing import Any, AsyncGenerator, Dict, Generator, Union
from unittest.mock import MagicMock

import pytest
from homeassistant.components.mqtt.sensor import DISCOVERY_SCHEMA
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template
from siobrultech_protocols.gem.packets import BIN48_NET_TIME, Packet

from brultech_serial2mqtt.config import Config
from brultech_serial2mqtt.device import DeviceManager


@pytest.fixture(autouse=True)
def auto_hass(hass: HomeAssistant) -> Generator[HomeAssistant, None, None]:
    yield hass


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
        MagicMock(),
    )
    yield device_manager


@pytest.fixture()
def parsed_values(
    device_manager: DeviceManager, hass: HomeAssistant
) -> Generator[Dict[str, Union[int, float]], None, None]:
    discovery_configs_by_unique_id: Dict[str, Dict[str, Any]] = {}
    for discovery_config in device_manager.home_assistant_discovery_configs:
        home_assistant_config = {"platform": "mqtt"}
        home_assistant_config.update(discovery_config.config)
        parsed_discover_config: Dict[str, Any] = DISCOVERY_SCHEMA(home_assistant_config)
        discovery_configs_by_unique_id[
            parsed_discover_config["unique_id"]
        ] = parsed_discover_config

    values_by_unique_id: Dict[str, Union[int, float]] = {}
    for unique_id, discovery_config in discovery_configs_by_unique_id.items():
        t = Template(
            discovery_config["value_template"].template,
            hass,
        )
        num: Union[int, float] = t.async_render(
            {"entity_id": unique_id, "value_json": device_manager.state_data},
            limited=True,
        )
        values_by_unique_id[unique_id] = num
    yield values_by_unique_id


def assertParsedValues(parsed: Dict[str, Any], expected: Dict[str, Any]) -> None:
    for entity, expected_value in expected.items():
        assert entity in parsed, f"Expected entity '{entity}' in parsed data."
        assert (
            parsed[entity] == expected_value
        ), f"Expected entity '{entity}' to have value {expected_value}, but got {parsed[entity]}"

    for entity in parsed.keys():
        assert entity in expected, f"Unexpected entity '{entity}' in parsed data."


@pytest.mark.local_config(
    {
        "device": {
            "channels": [{"number": 1}],
            "device_com": "COM1",
            "name": "gem",
        },
        "mqtt": {"broker": "localhost"},
    }
)
def test_simple_config(parsed_values: Dict[str, Any]):
    assertParsedValues(
        parsed_values,
        {
            "gem_3456_channel_1_current": 0.1,
            "gem_3456_channel_1_energy": 1,
            "gem_3456_channel_1_power": 360,
            "gem_3456_voltage": 120.0,
        },
    )


@pytest.mark.local_config(
    {
        "device": {
            "channels": [
                {"number": 1, "type": "main"},
                {"number": 2, "type": "solar_downstream_main"},
            ],
            "device_com": "COM1",
            "name": "gem",
        },
        "mqtt": {"broker": "localhost"},
    }
)
def test_main_with_downstream_soloar_config(parsed_values: Dict[str, Any]):
    assertParsedValues(
        parsed_values,
        {
            "gem_3456_channel_1_absolute_energy": 1,  # To/from grid, through main
            "gem_3456_channel_1_current": 0.1,
            "gem_3456_channel_1_polarized_energy": 0,  # To grid, through main
            "gem_3456_channel_1_power": 360,
            "gem_3456_channel_2_absolute_energy": 2,  # To/from solar
            "gem_3456_channel_2_current": 0.2,
            "gem_3456_channel_2_polarized_energy": 1,  # From solar
            "gem_3456_channel_2_power": 0,
            "gem_3456_solar_production_energy": 1,
            "gem_3456_grid_returned_energy": 0,
            "gem_3456_grid_consumed_energy": 1,
            "gem_3456_voltage": 120.0,
        },
    )


@pytest.mark.local_config(
    {
        "device": {
            "channels": [
                # Absolute: 1 Wh, Polarized 0 Wh
                {"number": 1, "type": "solar_upstream_main"},
                # Absolute: 2 Wh, Polarized 1 Wh
                {"number": 2, "type": "solar_upstream_main"},
            ],
            "device_com": "COM1",
            "name": "gem",
        },
        "mqtt": {"broker": "localhost"},
    }
)
def test_solar_production_only_upstream_config(parsed_values: Dict[str, Any]):
    assertParsedValues(
        parsed_values,
        {
            "gem_3456_channel_1_absolute_energy": 1,
            "gem_3456_channel_1_current": 0.1,
            "gem_3456_channel_1_polarized_energy": 0,
            "gem_3456_channel_1_power": 360,
            "gem_3456_channel_2_absolute_energy": 2,
            "gem_3456_channel_2_current": 0.2,
            "gem_3456_channel_2_polarized_energy": 1,
            "gem_3456_channel_2_power": 0,
            "gem_3456_solar_production_energy": 1,
            "gem_3456_grid_returned_energy": 1,
            "gem_3456_grid_consumed_energy": 2,
            "gem_3456_voltage": 120.0,
        },
    )


@pytest.mark.local_config(
    {
        "device": {
            "channels": [
                {"number": 1, "type": "solar_downstream_main"},
                {"number": 2, "type": "solar_downstream_main"},
            ],
            "device_com": "COM1",
            "name": "gem",
        },
        "mqtt": {"broker": "localhost"},
    }
)
def test_solar_production_only_downstream_config(parsed_values: Dict[str, Any]):
    assertParsedValues(
        parsed_values,
        {
            "gem_3456_channel_1_absolute_energy": 1,
            "gem_3456_channel_1_current": 0.1,
            "gem_3456_channel_1_polarized_energy": 0,
            "gem_3456_channel_1_power": 360,
            "gem_3456_channel_2_absolute_energy": 2,
            "gem_3456_channel_2_current": 0.2,
            "gem_3456_channel_2_polarized_energy": 1,
            "gem_3456_channel_2_power": 0,
            "gem_3456_solar_production_energy": 1,
            "gem_3456_voltage": 120.0,
        },
    )


@pytest.mark.local_config(
    {
        "device": {
            "channels": [
                # Absolute: 1 Wh, Polarized 0 Wh
                {"number": 1, "type": "main"},
                # Absolute: 2 Wh, Polarized 1 Wh
                {"number": 2, "type": "solar_upstream_main"},
                # Absolute: 3 Wh, Polarized 2 Wh
                {"number": 3, "type": "solar_downstream_main"},
            ],
            "device_com": "COM1",
            "name": "gem",
        },
        "mqtt": {"broker": "localhost"},
    }
)
def test_solar_production_upstream_and_downstream_config(parsed_values: Dict[str, Any]):
    assertParsedValues(
        parsed_values,
        {
            "gem_3456_channel_1_absolute_energy": 1,
            "gem_3456_channel_1_current": 0.1,
            "gem_3456_channel_1_polarized_energy": 0,
            "gem_3456_channel_1_power": 360,
            "gem_3456_channel_2_absolute_energy": 2,
            "gem_3456_channel_2_current": 0.2,
            "gem_3456_channel_2_polarized_energy": 1,
            "gem_3456_channel_2_power": 0,
            "gem_3456_channel_3_absolute_energy": 3,
            "gem_3456_channel_3_current": 0.3,
            "gem_3456_channel_3_polarized_energy": 2,
            "gem_3456_channel_3_power": -360,
            "gem_3456_solar_production_energy": 3,
            "gem_3456_grid_returned_energy": 1,
            "gem_3456_grid_consumed_energy": 2,
            "gem_3456_voltage": 120.0,
        },
    )
