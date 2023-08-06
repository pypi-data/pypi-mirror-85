"""
Presence
Get user presence for authenticated user or a specified user by ID
"""
from typing import List

from ..baseprovider import BaseProvider
from .models import PresenceResponse


class PresenceProvider(BaseProvider):
    BASE_URL = "https://graph.microsoft.com/beta"
    SEPARATOR = ","

    async def get_presence(self, **kwargs) -> PresenceResponse:
        """
        Get presence info for the current user
        Returns:
            :class:`PresenceResponse`: Presence Response
        """
        url = self.BASE_URL + "/me/presence"
        resp = await self.client.session.get(
            url, headers=self.HEADERS_PRESENCE, **kwargs
        )
        resp.raise_for_status()
        return PresenceResponse.parse_raw(await resp.text())

    async def get_presence_by_id(self, target_id: str, **kwargs) -> PresenceResponse:
        """
        Get Userpresence by xuid
        Args:
            target_xuid: XUID to get presence for
        Returns:
            :class:`PresenceResponse`: Presence Response
        """
        # https://graph.microsoft.com/beta/users/{user-id}/presence
        url = self.BASE_URL + f"/users/{target_id}/presence"
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_PRESENCE, **kwargs
        )
        resp.raise_for_status()
        return PresenceResponse.parse_raw(await resp.text())
