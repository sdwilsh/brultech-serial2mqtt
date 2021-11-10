"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from json import JSONEncoder

from homeassistant.core import HomeAssistant, callback
from homeassistant.loader import bind_hass

"""Helper to help store data."""
STORAGE_DIR = ...
_LOGGER = ...
STORAGE_SEMAPHORE = ...

@bind_hass
async def async_migrator(
    hass, old_path, store, *, old_conf_load_func=..., old_conf_migrate_func=...
):  # -> None:
    """Migrate old data to a store and then load data.

    async def old_conf_migrate_func(old_data)
    """
    ...

@bind_hass
class Store:
    """Class to help storing data."""

    def __init__(
        self,
        hass: HomeAssistant,
        version: int,
        key: str,
        private: bool = ...,
        *,
        encoder: type[JSONEncoder] | None = ...
    ) -> None:
        """Initialize storage class."""
        ...
    @property
    def path(self):  # -> str:
        """Return the config path."""
        ...
    async def async_load(self) -> dict | list | None:
        """Load data.

        If the expected version does not match the given version, the migrate
        function will be invoked with await migrate_func(version, config).

        Will ensure that when a call comes in while another one is in progress,
        the second call will wait and return the result of the first call.
        """
        ...
    async def async_save(self, data: dict | list) -> None:
        """Save data."""
        ...
    @callback
    def async_delay_save(
        self, data_func: Callable[[], dict], delay: float = ...
    ) -> None:
        """Save data with an optional delay."""
        ...
    async def async_remove(self) -> None:
        """Remove all data."""
        ...
