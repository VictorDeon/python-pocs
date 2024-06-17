import httpx
import logging
import json
from ..client_interface import HttpClientSingletonInterface


class HTTPxClientSingleton(HttpClientSingletonInterface):
    """
    Client HTTP.
    """

    def start_connection(self) -> None:
        """
        Iniciando o poll de conexões.
        """

        self.client = httpx.AsyncClient()

    async def get(self, url: str, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo GET.
        """

        try:
            response = await self.client.get(url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            result = response.json()
        except (httpx.HTTPStatusError, httpx.RequestError) as error:
            logging.error(f"Ocorreu um error na requisição a GET url {url}: {error}")
            result = None
        except json.JSONDecodeError as error:
            logging.error(f"Ocorreu um error ao decodificar o json no GET da url {url}: {error}")
            result = None

        return result

    async def post(self, url: str, data: dict, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo POST.
        """

        try:
            response = await self.client.post(url, json=data, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            result = response.json()
        except (httpx.HTTPStatusError, httpx.RequestError) as error:
            logging.error(f"Ocorreu um error na requisição a POST url {url}: {error}")
            result = None
        except json.JSONDecodeError as error:
            logging.error(f"Ocorreu um error ao decodificar o json no POST da url {url}: {error}")
            result = None

        return result

    async def put(self, url: str, data: dict, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo PUT.
        """

        try:
            response = await self.client.put(url, json=data, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            result = response.json()
        except (httpx.HTTPStatusError, httpx.RequestError) as error:
            logging.error(f"Ocorreu um error na requisição a PUT url {url}: {error}")
            result = None
        except json.JSONDecodeError as error:
            logging.error(f"Ocorreu um error ao decodificar o json no PUT da url {url}: {error}")
            result = None

        return result

    async def patch(self, url: str, data: dict, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo PATCH.
        """

        try:
            response = await self.client.patch(url, json=data, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            result = response.json()
        except (httpx.HTTPStatusError, httpx.RequestError) as error:
            logging.error(f"Ocorreu um error na requisição a PATCH url {url}: {error}")
            result = None
        except json.JSONDecodeError as error:
            logging.error(f"Ocorreu um error ao decodificar o json no PATCH da url {url}: {error}")
            result = None

        return result

    async def delete(self, url: str, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo DELETE.
        """

        try:
            response = await self.client.delete(url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            result = response.json()
        except (httpx.HTTPStatusError, httpx.RequestError) as error:
            logging.error(f"Ocorreu um error na requisição a DELETE url {url}: {error}")
            result = None
        except json.JSONDecodeError as error:
            logging.error(f"Ocorreu um error ao decodificar o json no DELETE da url {url}: {error}")
            result = None

        return result

    async def close_connection(self):
        """
        Fecha a conexão.
        """

        await self.client.aclose()
