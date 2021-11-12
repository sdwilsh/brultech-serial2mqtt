![Lint](https://github.com/sdwilsh/brultech-serial2mqtt/workflows/Lint/badge.svg)
![Test](https://github.com/sdwilsh/brultech-serial2mqtt/workflows/Test/badge.svg)

# What is brultech-serial2mqtt?

This library talks to devices from [Brultech Research](https://www.brultech.com/)
over their serial port, using
[siobrultech-protocols](https://github.com/sdwilsh/siobrultech-protocols) to
decode the data, and then sends the data to an MQTT server.

# Configuration Options

## Device

| Name                 | Type | Default      | Supported Options                                                       | Description                                                         |
| -------------------- | ---- | ------------ | ----------------------------------------------------------------------- | ------------------------------------------------------------------- |
| channels             | list | **required** | See [channels config](#channels)                                        | Channels to monitor and send to MQTT.                               |
| device_com           | str  | **required** | Either `COM1` or `COM2`                                                 | Which COM port on the device this serial connection is attached to. |
| name                 | str  | **required** | Any string                                                              | The name of the device to be used in Home Assistant Discovery       |
| url                  | str  | **required** | Any [pyserial URL](https://pythonhosted.org/pyserial/url_handlers.html) | The local connection to the device (i.e. `/dev/ttyUSB0`).           |
| baud                 | int  | 115200       | Any int                                                                 | The baud rate to communicate with the attached device with.         |
| packet_send_interval | int  | 8            | 5-256                                                                   | The frequency in which to have the device send packets.             |

### Channels

| Name                      | Type | Default                    | Supported Options                  | Description                                                                    |
| ------------------------- | ---- | -------------------------- | ---------------------------------- | ------------------------------------------------------------------------------ |
| number                    | int  | **required**               | 1-32                               | The channel number in the device.                                              |
| enabled_in_home_assistant | bool | True if `type` is `normal` | Any bool                           | If the entity for this channel should be enabled by default in Home Assistant. |
| name                      | str  | Channel {`number`}         | Any str                            | The name of the entity in Home Assistant                                       |
| type                      | str  | normal                     | See [channel types](#channel-type) | The type of channel to support net-metering and aggregation.                   |

#### Channel Type

##### `normal`

Power flows through one direction in this channel.

##### `main`

Power may flow through in both directions (depending on other channels like solar existing), and represents power coming in and going out from an electricity provider.

##### `solar_downstream_main`

Power flows in two directions from/to a solar inverter, with a `main` channel between it and the electricity provider.

##### `solar_upstream_main`

Power flows in two directions from/to a solar inverter, without a `main` channel between it and the electricity provider.

## MQTT

| Name           | Type | Default              | Supported Options                     | Description                                                           |
| -------------- | ---- | -------------------- | ------------------------------------- | --------------------------------------------------------------------- |
| broker         | str  | **required**         | Any str                               | The MQTT broker to connect to.                                        |
| birth_message  | dict | `{}`                 | See [birth message](#birth-message)   | The birth message to send when we connect to the MQTT broker.         |
| client_id      | str  | brultech-serial2mqtt | Any str                               | The client ID to use when connecting to the MQTT broker.              |
| home_assistant | dict | `{}`                 | See [home assistant](#home-assistant) | Configuration on how Home Assitant communicates with the MQTT broker. |
| password       | str  | None                 | Any str                               | The password to use to connect to the MQTT broker.                    |
| port           | int  | 1883                 | The port to connect to the broker on. |
| qos            | int  | 0                    | 0-2                                   | The qos to use for messages sent to the MQTT broker.                  |
| topic_prefix   | str  | brultech-serial2mqtt | Any str                               | The root topic to publish status messages on.                         |
| username       | str  | None                 | Any str                               | The username to connect to use to connect to the MQTT broker.         |
| will_message   | dict | `{}`                 | See [will message](#will-message)     | The will message to send when we disconnect from the MQTT broker.     |

### Birth Message

| Name    | Type | Default              | Supported Options | Description                                        |
| ------- | ---- | -------------------- | ----------------- | -------------------------------------------------- |
| payload | str  | online               | Any str           | The payload to use when sending the birth message. |
| qos     | int  | 0                    | 0-2               | The qos to use for the birth message.              |
| retain  | bool | True                 | Any bool          | If the retain flag is set on the birth message.    |
| topic   | str  | brultech-serial2mqtt | Any str           | The topic to use when sending the birth message.   |

### Home Assistant

| Name             | Type | Default       | Supported Options                                  | Description                                                                              |
| ---------------- | ---- | ------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| enable           | bool | True          | Any bool                                           | If the Home Assistant discovery configuration should be sent or not.                     |
| discovery_prefix | str  | homeassistant | Any str                                            | The topic prefix Home Assistant is configured to listen to for discovery configurations. |
| birth_message    | dict | `{}`          | See [birth message](#home-assistant-birth-message) | The birth message configuration of Home Assistant.                                       |

#### Home Assistant Birth Message

| Name    | Type | Default              | Supported Options | Description                                                                     |
| ------- | ---- | -------------------- | ----------------- | ------------------------------------------------------------------------------- |
| payload | str  | online               | Any str           | The payload Home Assistant is configured to use when sending the birth message. |
| qos     | int  | 0                    | 0-2               | The qos Home Assistant is configured to use for the birth message.              |
| topic   | str  | homeassistant/status | Any str           | The topic Home Assistant is configured to use when sending the birth message.   |

### Will Message

| Name    | Type | Default              | Supported Options | Description                                       |
| ------- | ---- | -------------------- | ----------------- | ------------------------------------------------- |
| payload | str  | online               | Any str           | The payload to use when sending the will message. |
| qos     | int  | 0                    | 0-2               | The qos to use for the will message.              |
| retain  | bool | True                 | Any bool          | If the retain flag is set on the will message.    |
| topic   | str  | brultech-serial2mqtt | Any str           | The topic to use when sending the will message.   |

## Logging

| Name  | Type | Default | Supported Options                                  | Description                                                               |
| ----- | ---- | ------- | -------------------------------------------------- | ------------------------------------------------------------------------- |
| level | str  | info    | `critical`, `error`, `warning`, `info`, or `debug` | The logging level the application should print messages to stdout with.   |
| logs  | dict | `{}`    | Any dict of levels                                 | A dict of Python named-logs and the level in which to log them to stdout. |

# Development

## Setup

```
python3.10 -m venv .venv
source .venv/bin/activate

# Install Requirements
pip install -r requirements.txt

# Install Dev Requirements
pip install -r requirements-dev.txt

# One-Time Install of Commit Hooks
pre-commit install
```

## Testing

Tests are run with `pytest`.
