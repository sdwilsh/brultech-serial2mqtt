import json
from copy import deepcopy
from typing import Any, Dict


class HomeAssistantDiscoveryConfig:
    """
    Helper object to manage the discovery config.  See
    https://www.home-assistant.io/docs/mqtt/discovery/
    """

    def __init__(self, component: str, config: Dict[str, Any]) -> None:
        assert "unique_id" in config
        self._component = component
        self._object_id = config["unique_id"]
        self._config = config

    @property
    def component(self) -> str:
        return self._component

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

    @property
    def json_config(self) -> str:
        """Returns pretty-printed JSON to send via MQTT."""
        return json.dumps(self.config, indent=2)

    @property
    def object_id(self) -> str:
        return self._object_id

    def apply_common_config(self, common_config: Dict[str, Any]):
        """
        Applies the given common configuration, allowing the current
        configuration to override any part of it.
        """
        new_config = deepcopy(common_config)
        new_config.update(self._config)
        self._config = new_config

    def get_discovery_topic(self, prefix: str) -> str:
        return f"{prefix}/{self.component}/{self.object_id}/config"
