import json
import aiohttp
from aiohttp.web import HTTPError
from src.engines.logger import ProjectLoggerSingleton


class AIOHTTPClient:
    """
    Client HTTP aio.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.client: aiohttp.ClientSession = None

    async def __aenter__(self) -> "AIOHTTPClient":
        """
        Iniciando o poll de conexões.
        """

        self.client = aiohttp.ClientSession()
        self.logger = ProjectLoggerSingleton.get_logger()
        return self

    async def get(self, url: str, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo GET.
        """

        try:
            async with self.client.get(url, params=params, headers=headers, timeout=timeout) as response:
                response.raise_for_status()
                result = await response.json()
        except HTTPError as error:
            self.logger.error(f"Ocorreu um error na requisição a GET url {url}: {error}")
            result = None
        except json.JSONDecodeError as error:
            self.logger.error(f"Ocorreu um error ao decodificar o json no GET da url {url}: {error}")
            result = None

        return result

    async def post(self, url: str, data: dict, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo POST.
        """

        try:
            async with self.client.post(url, json=data, params=params, headers=headers, timeout=timeout) as response:
                response.raise_for_status()
                result = await response.json()
        except HTTPError as error:
            self.logger.error(f"Ocorreu um error na requisição a POST url {url}: {error}")
            result = None
        except json.JSONDecodeError as error:
            self.logger.error(f"Ocorreu um error ao decodificar o json no POST da url {url}: {error}")
            result = None

        return result

    async def put(self, url: str, data: dict, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo PUT.
        """

        try:
            async with self.client.put(url, json=data, params=params, headers=headers, timeout=timeout) as response:
                response.raise_for_status()
                result = await response.json()
        except HTTPError as error:
            self.logger.error(f"Ocorreu um error na requisição a PUT url {url}: {error}")
            result = None
        except json.JSONDecodeError as error:
            self.logger.error(f"Ocorreu um error ao decodificar o json no PUT da url {url}: {error}")
            result = None

        return result

    async def patch(self, url: str, data: dict, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo PATCH.
        """

        try:
            async with self.client.patch(url, json=data, params=params, headers=headers, timeout=timeout) as response:
                response.raise_for_status()
                result = await response.json()
        except HTTPError as error:
            self.logger.error(f"Ocorreu um error na requisição a PATCH url {url}: {error}")
            result = None
        except json.JSONDecodeError as error:
            self.logger.error(f"Ocorreu um error ao decodificar o json no PATCH da url {url}: {error}")
            result = None

        return result

    async def delete(self, url: str, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo DELETE.
        """

        try:
            async with self.client.delete(url, params=params, headers=headers, timeout=timeout) as response:
                response.raise_for_status()
                result = await response.json()
        except HTTPError as error:
            self.logger.error(f"Ocorreu um error na requisição a DELETE url {url}: {error}")
            result = None
        except json.JSONDecodeError as error:
            self.logger.error(f"Ocorreu um error ao decodificar o json no DELETE da url {url}: {error}")
            result = None

        return result

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Fecha a conexão.
        """

        await self.client.close()
