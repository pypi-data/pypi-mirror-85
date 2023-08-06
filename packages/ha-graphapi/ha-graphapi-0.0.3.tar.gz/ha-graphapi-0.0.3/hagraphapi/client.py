"""
Microsoft Graph API Client
"""
import logging
from typing import Any

from aiohttp import hdrs
from aiohttp.client import ClientResponse
from ms_cv import CorrelationVector

from .provider.presence import PresenceProvider
from .auth.manager import AuthenticationManager

log = logging.getLogger("microsoft.graph.api")


class Session:
    def __init__(self, auth_mgr: AuthenticationManager):
        self._auth_mgr = auth_mgr
        self._cv = CorrelationVector()

    async def request(
        self,
        method: str,
        url: str,
        include_auth: bool = True,
        include_cv: bool = True,
        **kwargs: Any,
    ) -> ClientResponse:
        """Proxy Request and add Auth/CV headers."""
        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", None)
        data = kwargs.pop("data", None)

        # Extra, user supplied values
        extra_headers = kwargs.pop("extra_headers", None)
        extra_params = kwargs.pop("extra_params", None)
        extra_data = kwargs.pop("extra_data", None)

        if include_auth:
            # Ensure tokens valid
            await self._auth_mgr.refresh_tokens()
            # Set auth header
            headers[
                hdrs.AUTHORIZATION
            ] = self._auth_mgr.xsts_token.authorization_header_value

        if include_cv:
            headers["MS-CV"] = self._cv.increment()

        # Extend with optionally supplied values
        if extra_headers:
            headers.update(extra_headers)
        if extra_params:
            # query parameters
            params = params or {}
            params.update(extra_params)
        if extra_data:
            # form encoded post data
            data = data or {}
            data.update(extra_data)

        return await self._auth_mgr.session.request(
            method, url, **kwargs, headers=headers, params=params, data=data
        )

    async def get(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_GET, url, **kwargs)

    async def options(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_OPTIONS, url, **kwargs)

    async def head(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_HEAD, url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_POST, url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_PUT, url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_PATCH, url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_DELETE, url, **kwargs)


class GraphApiClient:
    def __init__(
        self,
        auth_mgr: AuthenticationManager,
    ):
        self._auth_mgr = auth_mgr
        self.session = Session(auth_mgr)

        self.presence = PresenceProvider(self)
