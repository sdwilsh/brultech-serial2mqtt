from copy import deepcopy
from typing import Any, Dict


class HomeAssistantDiscoveryConfig:
    """
    Helper object to manage the discovery config.  See
    https://www.home-assistant.io/docs/mqtt/discovery/
    """

    def __init__(self, component: str, object_id: str, config: Dict[str, Any]) -> None:
        self._component = component
        self._object_id = object_id
        self._config = config

    @property
    def component(self) -> str:
        return self._component

    @property
    def object_id(self) -> str:
        return self._object_id

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

    def apply_common_config(self, common_config: Dict[str, Any]):
        """
        Applies the given common configuration, allowing the current
        configuration to override any part of it.
        """
        new_config = deepcopy(common_config)
        new_config.update(self._config)
        self._config = new_config
