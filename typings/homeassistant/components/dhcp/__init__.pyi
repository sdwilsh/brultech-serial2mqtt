"""
This type stub file was generated by pyright.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Final, TYPE_CHECKING
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import BaseServiceInfo
from homeassistant.helpers.typing import ConfigType
from homeassistant.loader import DHCPMatcher

"""The dhcp integration."""
if TYPE_CHECKING: ...
CONFIG_SCHEMA = ...
FILTER = ...
REQUESTED_ADDR = ...
MESSAGE_TYPE = ...
HOSTNAME: Final = ...
MAC_ADDRESS: Final = ...
IP_ADDRESS: Final = ...
REGISTERED_DEVICES: Final = ...
DHCP_REQUEST = ...
SCAN_INTERVAL = ...
_LOGGER = ...

@dataclass(slots=True)
class DhcpServiceInfo(BaseServiceInfo):
    """Prepared info from dhcp entries."""

    ip: str
    hostname: str
    macaddress: str
    ...

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the dhcp component."""
    ...

class WatcherBase(ABC):
    """Base class for dhcp and device tracker watching."""
    def __init__(
        self,
        hass: HomeAssistant,
        address_data: dict[str, dict[str, str]],
        integration_matchers: list[DHCPMatcher],
    ) -> None:
        """Initialize class."""
        ...

    @abstractmethod
    async def async_stop(self) -> None:
        """Stop the watcher."""
        ...

    @abstractmethod
    async def async_start(self) -> None:
        """Start the watcher."""
        ...

    def process_client(self, ip_address: str, hostname: str, mac_address: str) -> None:
        """Process a client."""
        ...

    @callback
    def async_process_client(
        self, ip_address: str, hostname: str, mac_address: str
    ) -> None:
        """Process a client."""
        ...

class NetworkWatcher(WatcherBase):
    """Class to query ptr records routers."""
    def __init__(
        self,
        hass: HomeAssistant,
        address_data: dict[str, dict[str, str]],
        integration_matchers: list[DHCPMatcher],
    ) -> None:
        """Initialize class."""
        ...

    async def async_stop(self) -> None:
        """Stop scanning for new devices on the network."""
        ...

    async def async_start(self) -> None:
        """Start scanning for new devices on the network."""
        ...

    @callback
    def async_start_discover(self, *_: Any) -> None:
        """Start a new discovery task if one is not running."""
        ...

    async def async_discover(self) -> None:
        """Process discovery."""
        ...

class DeviceTrackerWatcher(WatcherBase):
    """Class to watch dhcp data from routers."""
    def __init__(
        self,
        hass: HomeAssistant,
        address_data: dict[str, dict[str, str]],
        integration_matchers: list[DHCPMatcher],
    ) -> None:
        """Initialize class."""
        ...

    async def async_stop(self) -> None:
        """Stop watching for new device trackers."""
        ...

    async def async_start(self) -> None:
        """Stop watching for new device trackers."""
        ...

class DeviceTrackerRegisteredWatcher(WatcherBase):
    """Class to watch data from device tracker registrations."""
    def __init__(
        self,
        hass: HomeAssistant,
        address_data: dict[str, dict[str, str]],
        integration_matchers: list[DHCPMatcher],
    ) -> None:
        """Initialize class."""
        ...

    async def async_stop(self) -> None:
        """Stop watching for device tracker registrations."""
        ...

    async def async_start(self) -> None:
        """Stop watching for device tracker registrations."""
        ...

class DHCPWatcher(WatcherBase):
    """Class to watch dhcp requests."""
    def __init__(
        self,
        hass: HomeAssistant,
        address_data: dict[str, dict[str, str]],
        integration_matchers: list[DHCPMatcher],
    ) -> None:
        """Initialize class."""
        ...

    async def async_stop(self) -> None:
        """Stop watching for new device trackers."""
        ...

    async def async_start(self) -> None:
        """Start watching for dhcp packets."""
        ...
