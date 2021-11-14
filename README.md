![Lint](https://github.com/sdwilsh/brultech-serial2mqtt/workflows/Lint/badge.svg)
![Test](https://github.com/sdwilsh/brultech-serial2mqtt/workflows/Test/badge.svg)

# What is brultech-serial2mqtt?

This image talks to devices from [Brultech Research](https://www.brultech.com/)
over their serial port, using
[siobrultech-protocols](https://github.com/sdwilsh/siobrultech-protocols) to
decode the data, and then sends the data to an MQTT server.

This image works will with Home Assistant, and will automatically create sesnors
if [MQTT Discovery](https://www.home-assistant.io/docs/mqtt/discovery/) is
enabled. Additionally, it creates named senors to easily integrate into the
native [Energy Management](https://www.home-assistant.io/docs/energy/).

# Table of Contents

- [Getting Started](#getting-started)
  - [Minimum Configuration](#minimum-configuration)
  - [Docker Compose](#docker-compose)
- [Supported Architectures](#supported-architectures)
- [Configuration Options](#configuration-options)
  - [Device](#device)
  - [Channels](#channels)
  - [MQTT](#mqtt)
  - [Logging](#logging)
- [Contributing](#contributing)

# Getting Started

## Minimum Configuration

Below is an example of the the minimum amount of configuration needed. See
[Configuration Options](#configuration-options) for more details and additional
options.

```yaml
---
device:
  channels:
    - number: 1
  device_com: "COM1"
  name: "House Energy Monitor"
mqtt:
  broker: "mqtt.mybroker.com"
```

## Docker Compose

```yaml
---
services:
  brultech:
    container_name: "serial2mqtt"
    image: "ghcr.io/sdwilsh/brultech-serial2mqtt:main"
    volumes:
      - "/etc/localtime:/etc/localtime:ro"
      - "<config path>:/config:ro"
    devices:
      - "/dev/serial/by-id/usb-XXXXX:/dev/ttyUSB0"
```

# Supported Architectures

All published images support multiple architectures. The images are currently published with support for the folowing:

- linux/amd64
- linux/arm/v7
- linux/arm64

The available images are:

| Image                                     | Description                               |
| ----------------------------------------- | ----------------------------------------- |
| ghcr.io/sdwilsh/brultech-serial2mqtt:main | Bleeding edge tracking the `main` branch. |

# Configuration Options

The configuration file supports `!secret` strings, [as documented for Home Assistant](https://www.home-assistant.io/docs/configuration/secrets/).

## Device

| Name       | Type | Supported Options                | Description                                                         |
| ---------- | ---- | -------------------------------- | ------------------------------------------------------------------- |
| channels   | list | See [channels config](#channels) | Channels to monitor and send to MQTT.                               |
| device_com | str  | Either `COM1` or `COM2`          | Which COM port on the device this serial connection is attached to. |
| name       | str  | Any string                       | The name of the device to be used in Home Assistant Discovery.      |

<details>
<summary>Optional Device Configuration Options</summary>

| Name                  | Type | Default      | Supported Options                                                       | Description                                             |
| --------------------- | ---- | ------------ | ----------------------------------------------------------------------- | ------------------------------------------------------- |
| baud                  | int  | 115200       | Any int                                                                 | The baud rate to communicate with the attached device.  |
| send_interval_seconds | int  | 8            | 5-256                                                                   | The frequency in which to have the device send packets. |
| url                   | str  | /dev/ttyUSB0 | Any [pyserial URL](https://pythonhosted.org/pyserial/url_handlers.html) | The local connection to the device.                     |

</details>

### Channels

| Name   | Type | Supported Options | Description                       |
| ------ | ---- | ----------------- | --------------------------------- |
| number | int  | 1-32              | The channel number in the device. |

<details>
<summary>Optional Channel Configuration Options</summary>

| Name           | Type | Default                    | Supported Options                  | Description                                                                    |
| -------------- | ---- | -------------------------- | ---------------------------------- | ------------------------------------------------------------------------------ |
| home_assistant | bool | True if `type` is `normal` | Any bool                           | If the entity for this channel should be enabled by default in Home Assistant. |
| name           | str  | Channel {`number`}         | Any str                            | The name of the entity in Home Assistant.                                      |
| type           | str  | normal                     | See [channel types](#channel-type) | The type of channel to support net-metering and aggregation.                   |

#### Channel Type

| Channel Type          | Description                                                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| normal                | Power flows through one direction in this channel.                                                                                                                      |
| main                  | Power may flow through in both directions (depending on other channels like solar existing), and represents power coming in and going out from an electricity provider. |
| solar_downstream_main | Power flows in two directions from/to a solar inverter, with a `main` channel between it and the electricity provider.                                                  |
| solar_upstream_main   | Power flows in two directions from/to a solar inverter, without a `main` channel between it and the electricity provider.                                               |

</details>

## MQTT

| Name   | Type | Supported Options | Description                    |
| ------ | ---- | ----------------- | ------------------------------ |
| broker | str  | Any str           | The MQTT broker to connect to. |

<details>
<summary>Optional MQTT Configuration Options</summary>

| Name           | Type                | Default                       | Supported Options                     | Description                                                                                                   |
| -------------- | ------------------- | ----------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| birth_message  | dict                | `{}`                          | See [birth message](#birth-message)   | The birth message to send when we connect to the MQTT broker.                                                 |
| client_id      | Jinja2 template str | brultech-serial2mqtt-{serial} | Any Jinja2 template str               | The client ID to use when connecting to the MQTT broker. `device_serial` is available to use in the template. |
| home_assistant | dict                | `{}`                          | See [home assistant](#home-assistant) | Configuration on how Home Assistant communicates with the MQTT broker.                                        |
| password       | str                 | None                          | Any str                               | The password to use to connect to the MQTT broker.                                                            |
| port           | int                 | 1883                          | Any int                               | The port to connect to the broker on.                                                                         |
| qos            | int                 | 0                             | 0-2                                   | The qos to use for messages sent to the MQTT broker.                                                          |
| topic_prefix   | Jina2 template str  | brultech-serial2mqtt-{serial} | Any Jinja2 template str               | The root topic to publish status messages on. `device_serial` is available to use in the template.            |
| username       | str                 | None                          | Any str                               | The username to connect to use to connect to the MQTT broker.                                                 |
| will_message   | dict                | `{}`                          | See [will message](#will-message)     | The will message to send when we disconnect from the MQTT broker.                                             |

### Birth Message

The birth message is sent under the topic prefix configured in the [MQTT](#mqtt) config, `/status`.

| Name    | Type | Default | Supported Options | Description                                        |
| ------- | ---- | ------- | ----------------- | -------------------------------------------------- |
| payload | str  | online  | Any str           | The payload to use when sending the birth message. |
| qos     | int  | 0       | 0-2               | The qos to use for the birth message.              |
| retain  | bool | True    | Any bool          | If the retain flag is set on the birth message.    |

### Home Assistant

| Name             | Type | Default       | Supported Options                                  | Description                                                                                                                                 |
| ---------------- | ---- | ------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| enable           | bool | True          | Any bool                                           | If the Home Assistant discovery configuration should be sent or not.                                                                        |
| discovery_prefix | str  | homeassistant | Any str                                            | The topic prefix Home Assistant is configured to listen to for discovery configurations.                                                    |
| birth_message    | dict | `{}`          | See [birth message](#home-assistant-birth-message) | The birth message configuration of Home Assistant. See [Home Assistant documentation](https://www.home-assistant.io/docs/mqtt/birth_will/). |

#### Home Assistant Birth Message

| Name    | Type | Default              | Supported Options | Description                                                                     |
| ------- | ---- | -------------------- | ----------------- | ------------------------------------------------------------------------------- |
| payload | str  | online               | Any str           | The payload Home Assistant is configured to use when sending the birth message. |
| qos     | int  | 0                    | 0-2               | The qos Home Assistant is configured to use for the birth message.              |
| topic   | str  | homeassistant/status | Any str           | The topic Home Assistant is configured to use when sending the birth message.   |

### Will Message

The well message is sent under the topic prefix configured in the [MQTT](#mqtt) config, `/status`.

| Name    | Type | Default | Supported Options | Description                                       |
| ------- | ---- | ------- | ----------------- | ------------------------------------------------- |
| payload | str  | online  | Any str           | The payload to use when sending the will message. |
| qos     | int  | 0       | 0-2               | The qos to use for the will message.              |
| retain  | bool | True    | Any bool          | If the retain flag is set on the will message.    |

</details>

## Logging

<details>
<summary>Optional Logging Configuration Options</summary>

| Name  | Type | Default | Supported Options                                  | Description                                                               |
| ----- | ---- | ------- | -------------------------------------------------- | ------------------------------------------------------------------------- |
| level | str  | info    | `critical`, `error`, `warning`, `info`, or `debug` | The logging level the application should print messages to stdout with.   |
| logs  | dict | `{}`    | Any dict of levels                                 | A dict of Python named-logs and the level in which to log them to stdout. |

</details>

# Contributing

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
