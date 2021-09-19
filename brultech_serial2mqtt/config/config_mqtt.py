import typing
from voluptuous import All, Any, Optional, Required, Schema


SCHEMA = Schema(
    All(
        {
            Required("broker"): str,
            Optional("client_id", default="brultech-serial2mqtt"): Any(str, None),
            Optional("home_assistant", default={}): {
                Optional("enable", default=True): bool,
                Optional("discovery_prefix", default="homeassistant"): str,
            },
            Optional("password", default=None): Any(str, None),
            Optional("port", default=1883): int,
            Optional("topic_prefix", default="brultech-serial2mqtt"): Any(str, None),
            Optional("username", default=None): Any(str, None),
        },
    )
)


class HomeAssistant:
    """Home Assistant integration config."""

    def __init__(self, home_assistant: dict):
        self._enable = home_assistant["enable"]
        self._discovery_prefix = home_assistant["discovery_prefix"]

    @property
    def enable(self) -> bool:
        """Return if integration is enabled."""
        return self._enable

    @property
    def discovery_prefix(self) -> str:
        """Return Home Assistant discovery prefix."""
        return self._discovery_prefix


class MQTTConfig:
    """MQTT config."""

    schema = SCHEMA

    def __init__(self, mqtt: dict):
        self._broker = mqtt["broker"]
        self._client_id = mqtt["client_id"]
        self._home_assistant = HomeAssistant(mqtt["home_assistant"])
        self._password = mqtt["password"]
        self._port = mqtt["port"]
        self._topic_prefix = mqtt["topic_prefix"]
        self._username = mqtt["username"]

    @property
    def broker(self) -> str:
        """Return broker IP or hostname."""
        return self._broker

    @property
    def client_id(self) -> typing.Optional[str]:
        """Return client id."""
        return self._client_id

    @property
    def home_assistant(self) -> HomeAssistant:
        """Return Home Assistant integration config."""
        return self._home_assistant

    @property
    def password(self) -> typing.Optional[str]:
        """Return broker password."""
        return self._password

    @property
    def port(self) -> int:
        """Return broker port."""
        return self._port

    @property
    def topic_prefix(self) -> str:
        """Return topic prefix to use when sending to broker."""
        return self._topic_prefix

    @property
    def username(self) -> typing.Optional[str]:
        """Return broker username."""
        return self._username
