"""
This type stub file was generated by pyright.
"""

from datetime import datetime, timedelta
from typing import NamedTuple

import attr

from . import permissions as perm_mdl

"""
This type stub file was generated by pyright.
"""
TOKEN_TYPE_NORMAL = ...
TOKEN_TYPE_SYSTEM = ...
TOKEN_TYPE_LONG_LIVED_ACCESS_TOKEN = ...

@attr.s(slots=True)
class Group:
    """A group."""

    name: str | None = ...
    policy: perm_mdl.PolicyType = ...
    id: str = ...
    system_generated: bool = ...

@attr.s(slots=True)
class User:
    """A user."""

    name: str | None = ...
    perm_lookup: perm_mdl.PermissionLookup = ...
    id: str = ...
    is_owner: bool = ...
    is_active: bool = ...
    system_generated: bool = ...
    groups: list[Group] = ...
    credentials: list[Credentials] = ...
    refresh_tokens: dict[str, RefreshToken] = ...
    _permissions: perm_mdl.PolicyPermissions | None = ...
    @property
    def permissions(self) -> perm_mdl.AbstractPermissions:
        """Return permissions object for user."""
        ...
    @property
    def is_admin(self) -> bool:
        """Return if user is part of the admin group."""
        ...
    def invalidate_permission_cache(self) -> None:
        """Invalidate permission cache."""
        ...

@attr.s(slots=True)
class RefreshToken:
    """RefreshToken for a user to grant new access tokens."""

    user: User = ...
    client_id: str | None = ...
    access_token_expiration: timedelta = ...
    client_name: str | None = ...
    client_icon: str | None = ...
    token_type: str = ...
    id: str = ...
    created_at: datetime = ...
    token: str = ...
    jwt_key: str = ...
    last_used_at: datetime | None = ...
    last_used_ip: str | None = ...
    credential: Credentials | None = ...
    version: str | None = ...

@attr.s(slots=True)
class Credentials:
    """Credentials for a user on an auth provider."""

    auth_provider_type: str = ...
    auth_provider_id: str | None = ...
    data: dict = ...
    id: str = ...
    is_new: bool = ...

class UserMeta(NamedTuple):
    """User metadata."""

    name: str | None
    is_active: bool
    ...
