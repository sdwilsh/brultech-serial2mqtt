import ssl
from typing import Any, Dict, Optional

from jinja2 import Template
from voluptuous import All
from voluptuous import Any as AnyValid
from voluptuous import Optional as OptionalField
from voluptuous import Range
from voluptuous import Required as RequiredField
from voluptuous import Schema

from brultech_serial2mqtt.config.typing import EmptyConfigDict

SCHEMA = Schema(
    {
        OptionalField("birth_message", default=EmptyConfigDict): {
            OptionalField("payload", default="online"): str,
            OptionalField("qos", default=0): All(
                int,
                Range(min=0, max=2),
            ),
            OptionalField("retain", default=True): bool,
        },
        RequiredField("broker"): str,
        OptionalField(
            "client_id", default="brultech-serial2mqtt-{{ device_serial }}"
        ): AnyValid(str, None),
        OptionalField("home_assistant", default=EmptyConfigDict): {
            OptionalField("enable", default=True): bool,
            OptionalField("birth_message", default=EmptyConfigDict): {
                OptionalField("topic", default="homeassistant/status"): str,
                OptionalField("payload", default="online"): str,
                OptionalField("qos", default=0): All(
                    int,
                    Range(min=0, max=2),
                ),
            },
            OptionalField("discovery_prefix", default="homeassistant"): str,
            OptionalField("skip_packets", default=37): All(int, Range(min=0)),
        },
        OptionalField("password", default=None): AnyValid(str, None),
        OptionalField("port", default=1883): int,
        OptionalField("qos", default=0): All(
            int,
            Range(min=0, max=2),
        ),
        OptionalField("tls_options", default=EmptyConfigDict): {
            OptionalField("ca_certs", default=None): AnyValid(str, None),
            OptionalField("cert_reqs", default=True): bool,
            OptionalField("certfile", default=None): AnyValid(str, None),
            OptionalField("ciphers", default=None): AnyValid(str, None),
            OptionalField("keyfile", default=None): AnyValid(str, None),
            OptionalField("keyfile_password", default=None): AnyValid(str, None),
            OptionalField("tls_version", default="tls1.2"): AnyValid(
                "tls1", "tls1.1", "tls1.2", None
            ),
        },
        OptionalField(
            "topic_prefix", default="brultech-serial2mqtt-{{ device_serial }}"
        ): AnyValid(str, None),
        OptionalField("username", default=None): AnyValid(str, None),
        OptionalField("usetls", default=False): bool,
        OptionalField("will_message", default=EmptyConfigDict): {
            OptionalField("payload", default="offline"): str,
            OptionalField("qos", default=0): All(
                int,
                Range(min=0, max=2),
            ),
            OptionalField("retain", default=True): bool,
        },
    },
)


class BirthWillConfigMixin:
    def __init__(self, birth_will_config: Dict[str, Any]):
        self._payload: str = birth_will_config["payload"]
        self._qos: int = birth_will_config["qos"]

    @property
    def payload(self) -> str:
        return self._payload

    @property
    def qos(self) -> int:
        return self._qos


class HomeAssistantBirthMessage(BirthWillConfigMixin):
    """Home Assistant birth message config."""

    def __init__(self, birth_config: Dict[str, Any]):
        super().__init__(birth_config)
        self._topic: str = birth_config["topic"]

    @property
    def topic(self) -> str:
        return self._topic


class HomeAssistant:
    """Home Assistant integration config."""

    def __init__(self, home_assistant_config: Dict[str, Any]):
        self._birth_message = HomeAssistantBirthMessage(
            home_assistant_config["birth_message"]
        )
        self._discovery_prefix = home_assistant_config["discovery_prefix"]
        self._enable = home_assistant_config["enable"]
        self._skip_packets = home_assistant_config["skip_packets"]

    @property
    def birth_message(self) -> HomeAssistantBirthMessage:
        return self._birth_message

    @property
    def discovery_prefix(self) -> str:
        """Return Home Assistant discovery prefix."""
        return self._discovery_prefix

    @property
    def enable(self) -> bool:
        """Return if integration is enabled."""
        return self._enable

    @property
    def skip_packets(self) -> int:
        """Return the number of packets to skip before updating Home Assistant."""
        return self._skip_packets


class MQTTBirthWillMessageConfig(BirthWillConfigMixin):
    """MQTT birth/will message sending configuration."""

    def __init__(
        self,
        birth_will_config: Dict[str, Any],
    ):
        super().__init__(birth_will_config)
        self._retain: bool = birth_will_config["retain"]

    @property
    def retain(self) -> bool:
        return self._retain


class TlsConfig:
    """TLS Param options."""

    def __init__(self, tls_config: Dict[str, Any]):
        self._ca_certs = tls_config["ca_certs"]
        self._cert_reqs = tls_config["cert_reqs"]
        self._certfile = tls_config["certfile"]
        self._ciphers = tls_config["ciphers"]
        self._keyfile = tls_config["keyfile"]
        self._keyfile_password = tls_config["keyfile_password"]
        self._tls_version = tls_config["tls_version"]

    @property
    def ca_certs(self) -> str:
        return self._ca_certs

    @property
    def cert_reqs(self):
        if not self._cert_reqs:
            return ssl.CERT_NONE
        else:
            return ssl.CERT_REQUIRED

    @property
    def certfile(self) -> str:
        return self._certfile

    @property
    def ciphers(self) -> str:
        return self._ciphers

    @property
    def keyfile(self) -> str:
        return self._keyfile

    @property
    def keyfile_password(self) -> str:
        return self._keyfile_password

    @property
    def tls_version(self):
        if self._tls_version == "tls1":
            return ssl.PROTOCOL_TLSv1
        elif self._tls_version == "tls1.1":
            return ssl.PROTOCOL_TLSv1_1
        elif self._tls_version == "tls1.2":
            return ssl.PROTOCOL_TLSv1_2
        else:
            # Let paho-mqtt handle (defaults to ssl.PROTOCOL_TLS)
            return None


class MQTTConfig:
    """MQTT config."""

    schema = SCHEMA

    def __init__(self, mqtt_config: Dict[str, Any]):
        self._birth_message = MQTTBirthWillMessageConfig(mqtt_config["birth_message"])
        self._broker = mqtt_config["broker"]
        self._client_id = mqtt_config["client_id"]
        self._home_assistant = HomeAssistant(mqtt_config["home_assistant"])
        self._password = mqtt_config["password"]
        self._port = mqtt_config["port"]
        self._qos = mqtt_config["qos"]
        self._tls_options = TlsConfig(mqtt_config["tls_options"])
        self._topic_prefix = mqtt_config["topic_prefix"]
        self._username = mqtt_config["username"]
        self._usetls = mqtt_config["usetls"]
        self._will_message = MQTTBirthWillMessageConfig(mqtt_config["will_message"])

    @property
    def birth_message(self) -> MQTTBirthWillMessageConfig:
        return self._birth_message

    @property
    def broker(self) -> str:
        """Return broker IP or hostname."""
        return self._broker

    def client_id(self, device_serial: int) -> str:
        """Return client id."""
        return Template(self._client_id).render(device_serial=device_serial)

    @property
    def home_assistant(self) -> HomeAssistant:
        """Return Home Assistant integration config."""
        return self._home_assistant

    @property
    def password(self) -> Optional[str]:
        """Return broker password."""
        return self._password

    @property
    def port(self) -> int:
        """Return broker port."""
        return self._port

    @property
    def qos(self) -> int:
        """Return qos to use for messages."""
        return self._qos

    @property
    def tls_options(self) -> TlsConfig:
        """Return TLS options"""
        return self._tls_options

    def state_topic(self, device_serial: int) -> str:
        """Return the topic used to convey device state."""
        return f"{self.topic_prefix(device_serial)}/state"

    def status_topic(self, device_serial: int) -> str:
        """Return the topic used to convey service status (via birth and will)."""
        return f"{self.topic_prefix(device_serial)}/status"

    def topic_prefix(self, device_serial: int) -> str:
        """Return topic prefix to use when sending to broker."""
        return Template(self._topic_prefix).render(device_serial=device_serial)

    @property
    def username(self) -> Optional[str]:
        """Return broker username."""
        return self._username

    @property
    def usetls(self) -> bool:
        return self._usetls

    @property
    def will_message(self) -> MQTTBirthWillMessageConfig:
        return self._will_message
