from typing import Any


class HttpClientInterface:
    async def get(self, url: str, params: dict[str, Any] = None) -> dict[str, Any]:
        pass
