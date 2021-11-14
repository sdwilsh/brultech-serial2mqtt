"""
This type stub file was generated by pyright.
"""

from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Final

from aiohttp.web import Application, Request, StreamResponse, middleware
from homeassistant.core import HomeAssistant, callback

"""Ban logic for HTTP component."""
_LOGGER: Final = ...
KEY_BANNED_IPS: Final = ...
KEY_FAILED_LOGIN_ATTEMPTS: Final = ...
KEY_LOGIN_THRESHOLD: Final = ...
NOTIFICATION_ID_BAN: Final = ...
NOTIFICATION_ID_LOGIN: Final = ...
IP_BANS_FILE: Final = ...
ATTR_BANNED_AT: Final = ...
SCHEMA_IP_BAN_ENTRY: Final = ...

@callback
def setup_bans(hass: HomeAssistant, app: Application, login_threshold: int) -> None:
    """Create IP Ban middleware for the app."""
    ...

@middleware
async def ban_middleware(
    request: Request, handler: Callable[[Request], Awaitable[StreamResponse]]
) -> StreamResponse:
    """IP Ban middleware."""
    ...

def log_invalid_auth(
    func: Callable[..., Awaitable[StreamResponse]]
) -> Callable[..., Awaitable[StreamResponse]]:
    """Decorate function to handle invalid auth or failed login attempts."""
    ...

async def process_wrong_login(request: Request) -> None:
    """Process a wrong login attempt.

    Increase failed login attempts counter for remote IP address.
    Add ip ban entry if failed login attempts exceeds threshold.
    """
    ...

async def process_success_login(request: Request) -> None:
    """Process a success login attempt.

    Reset failed login attempts counter for remote IP address.
    No release IP address from banned list function, it can only be done by
    manual modify ip bans config file.
    """
    ...

class IpBan:
    """Represents banned IP address."""

    def __init__(self, ip_ban: str, banned_at: datetime | None = ...) -> None:
        """Initialize IP Ban object."""
        ...

async def async_load_ip_bans_config(hass: HomeAssistant, path: str) -> list[IpBan]:
    """Load list of banned IPs from config file."""
    ...

def update_ip_bans_config(path: str, ip_ban: IpBan) -> None:
    """Update config file with new banned IP address."""
    ...