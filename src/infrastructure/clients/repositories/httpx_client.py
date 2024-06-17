from typing import Any
from httpx import AsyncClient
from ..http_interface import HttpClientInterface


class HTTPxClient(HttpClientInterface):
    async def get(self, url: str, params: dict[str, Any] = None) -> dict[str, Any]:
        async with AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
