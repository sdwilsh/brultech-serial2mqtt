from typing import Any, Dict, Generator, Union

import pytest
from homeassistant.components.mqtt.sensor import DISCOVERY_SCHEMA
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template
from brultech_serial2mqtt.device import DeviceManager


DiscoveryConfig = Dict[str, Any]
DiscoveryConfigByUniqueId = Dict[str, DiscoveryConfig]


@pytest.fixture()
def discovery_configs(
    device_manager: DeviceManager
) -> Generator[DiscoveryConfigByUniqueId, None, None]:
    discovery_configs_by_unique_id: DiscoveryConfigByUniqueId = {}
    for discovery_config in device_manager.home_assistant_discovery_configs:
        home_assistant_config = {"platform": "mqtt"}
        home_assistant_config.update(discovery_config.config)
        parsed_discover_config: Dict[str, Any] = DISCOVERY_SCHEMA(home_assistant_config)
        discovery_configs_by_unique_id[
            parsed_discover_config["unique_id"]
        ] = parsed_discover_config
    yield discovery_configs_by_unique_id


@pytest.fixture()
def parsed_values(
    device_manager: DeviceManager,
    discovery_configs: DiscoveryConfigByUniqueId,
    hass: HomeAssistant,
) -> Generator[Dict[str, Union[int, float]], None, None]:
    values_by_unique_id: Dict[str, Union[int, float]] = {}
    for unique_id, discovery_config in discovery_configs.items():
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


@pytest.mark.parametrize(
    "config",
    [
        {
            "device": {
                "channels": [{"number": 1}],
                "device_com": "COM1",
                "name": "gem",
            },
            "mqtt": {"broker": "localhost"},
        },
    ],
)
def test_simple_config(
    discovery_configs: DiscoveryConfigByUniqueId, parsed_values: Dict[str, Any]
):
    assert discovery_configs == {
        "gem_3456_channel_1_current": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.CURRENT,
            "enabled_by_default": True,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 1 Current",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.MEASUREMENT,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_1_current",
            "unit_of_measurement": "A",
            "value_template": Template("{{ value_json.channel_1.current }}"),
        },
        "gem_3456_channel_1_energy": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.ENERGY,
            "enabled_by_default": True,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 1 Energy",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_1_energy",
            "unit_of_measurement": "Wh",
            "value_template": Template(
                "{{ (value_json.channel_1.absolute_watt_seconds / 3600) | round }}"
            ),
        },
        "gem_3456_channel_1_power": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.POWER,
            "enabled_by_default": True,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 1 Power",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.MEASUREMENT,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_1_power",
            "unit_of_measurement": "W",
            "value_template": Template("{{ value_json.channel_1.power }}"),
        },
        "gem_3456_voltage": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech Research Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.VOLTAGE,
            "enabled_by_default": True,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Voltage",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.MEASUREMENT,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_voltage",
            "unit_of_measurement": "V",
            "value_template": Template("{{ value_json.voltage }}"),
        },
    }
    assertParsedValues(
        parsed_values,
        {
            "gem_3456_channel_1_current": 0.1,
            "gem_3456_channel_1_energy": 1,
            "gem_3456_channel_1_power": 360,
            "gem_3456_voltage": 120.0,
        },
    )


@pytest.mark.parametrize(
    "config",
    [
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
        },
    ],
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


@pytest.mark.parametrize(
    "config",
    [
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
        },
    ],
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


@pytest.mark.parametrize(
    "config",
    [
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
        },
    ],
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


@pytest.mark.parametrize(
    "config",
    [
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
        },
    ],
)
def test_solar_production_upstream_and_downstream_config(
    discovery_configs: DiscoveryConfigByUniqueId, parsed_values: Dict[str, Any]
):
    assert discovery_configs == {
        "gem_3456_channel_1_absolute_energy": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech " "Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.ENERGY,
            "enabled_by_default": False,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 1 Absolute Energy",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_1_absolute_energy",
            "unit_of_measurement": "Wh",
            "value_template": Template(
                "{{ (value_json.channel_1.absolute_watt_seconds / 3600) | round }}"
            ),
        },
        "gem_3456_channel_1_current": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.CURRENT,
            "enabled_by_default": False,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 1 Current",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.MEASUREMENT,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_1_current",
            "unit_of_measurement": "A",
            "value_template": Template("{{ value_json.channel_1.current }}"),
        },
        "gem_3456_channel_1_polarized_energy": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech " "Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.ENERGY,
            "enabled_by_default": False,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 1 Polarized Energy",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_1_polarized_energy",
            "unit_of_measurement": "Wh",
            "value_template": Template(
                "{{ (value_json.channel_1.polarized_watt_seconds / 3600) | round }}"
            ),
        },
        "gem_3456_channel_1_power": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.POWER,
            "enabled_by_default": False,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 1 Power",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.MEASUREMENT,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_1_power",
            "unit_of_measurement": "W",
            "value_template": Template("{{ value_json.channel_1.power }}"),
        },
        "gem_3456_channel_2_absolute_energy": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech " "Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.ENERGY,
            "enabled_by_default": False,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 2 Absolute Energy",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_2_absolute_energy",
            "unit_of_measurement": "Wh",
            "value_template": Template(
                "{{ (value_json.channel_2.absolute_watt_seconds / 3600) | round }}"
            ),
        },
        "gem_3456_channel_2_current": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.CURRENT,
            "enabled_by_default": False,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 2 Current",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.MEASUREMENT,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_2_current",
            "unit_of_measurement": "A",
            "value_template": Template("{{ value_json.channel_2.current }}"),
        },
        "gem_3456_channel_2_polarized_energy": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech " "Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.ENERGY,
            "enabled_by_default": False,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 2 Polarized Energy",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_2_polarized_energy",
            "unit_of_measurement": "Wh",
            "value_template": Template(
                "{{ (value_json.channel_2.polarized_watt_seconds / 3600) | round }}"
            ),
        },
        "gem_3456_channel_2_power": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.POWER,
            "enabled_by_default": False,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 2 Power",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.MEASUREMENT,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_2_power",
            "unit_of_measurement": "W",
            "value_template": Template("{{ value_json.channel_2.power }}"),
        },
        "gem_3456_channel_3_absolute_energy": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech " "Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.ENERGY,
            "enabled_by_default": False,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 3 Absolute Energy",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_3_absolute_energy",
            "unit_of_measurement": "Wh",
            "value_template": Template(
                "{{ (value_json.channel_3.absolute_watt_seconds / 3600) | round }}"
            ),
        },
        "gem_3456_channel_3_current": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.CURRENT,
            "enabled_by_default": False,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 3 Current",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.MEASUREMENT,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_3_current",
            "unit_of_measurement": "A",
            "value_template": Template("{{ value_json.channel_3.current }}"),
        },
        "gem_3456_channel_3_polarized_energy": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech " "Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.ENERGY,
            "enabled_by_default": False,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 3 Polarized Energy",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_3_polarized_energy",
            "unit_of_measurement": "Wh",
            "value_template": Template(
                "{{ (value_json.channel_3.polarized_watt_seconds / 3600) | round }}"
            ),
        },
        "gem_3456_channel_3_power": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.POWER,
            "enabled_by_default": False,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Channel 3 Power",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.MEASUREMENT,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_channel_3_power",
            "unit_of_measurement": "W",
            "value_template": Template("{{ value_json.channel_3.power }}"),
        },
        "gem_3456_grid_consumed_energy": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech " "Research Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.ENERGY,
            "enabled_by_default": True,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Grid Consumption Energy",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_grid_consumed_energy",
            "unit_of_measurement": "Wh",
            "value_template": Template(
                "{{ ((0  + value_json.channel_1.absolute_watt_seconds - value_json.channel_1.polarized_watt_seconds + value_json.channel_2.absolute_watt_seconds - value_json.channel_2.polarized_watt_seconds) / 3600) | round }}"
            ),
        },
        "gem_3456_grid_returned_energy": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech " "Research Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.ENERGY,
            "enabled_by_default": True,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Return to Grid Energy",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_grid_returned_energy",
            "unit_of_measurement": "Wh",
            "value_template": Template(
                "{{ ((0  + value_json.channel_1.polarized_watt_seconds + value_json.channel_2.polarized_watt_seconds) / 3600) | round }}"
            ),
        },
        "gem_3456_solar_production_energy": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech " "Research " "Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.ENERGY,
            "enabled_by_default": True,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Solar Production Energy",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_solar_production_energy",
            "unit_of_measurement": "Wh",
            "value_template": Template(
                "{{ ((0  + value_json.channel_3.polarized_watt_seconds + value_json.channel_2.polarized_watt_seconds) / 3600) | round }}"
            ),
        },
        "gem_3456_voltage": {
            "availability": [
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
                {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "brultech-serial2mqtt-3456/status",
                },
            ],
            "availability_mode": "latest",
            "device": {
                "connections": [],
                "identifiers": [
                    "brultech-serial2mqtt,serial-3456",
                    "brultech-serial2mqtt,device_id-12",
                ],
                "manufacturer": "Brultech Research Inc.",
                "model": "GreenEye Monitor",
                "name": "gem",
            },
            "device_class": SensorDeviceClass.VOLTAGE,
            "enabled_by_default": True,
            "encoding": "utf-8",
            "force_update": False,
            "name": "Voltage",
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 1,
            "state_class": SensorStateClass.MEASUREMENT,
            "state_topic": "brultech-serial2mqtt-3456/state",
            "unique_id": "gem_3456_voltage",
            "unit_of_measurement": "V",
            "value_template": Template("{{ value_json.voltage }}"),
        },
    }
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
