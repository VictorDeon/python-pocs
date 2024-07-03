import logging
import json
import os
import httpx
from fastapi.exceptions import HTTPException


class HTTPxSingleton:
    """
    Client HTTP Singleton.
    """

    __instance = None

    def __init__(self) -> None:
        """
        Construtor.
        """

        if self.__instance:
            raise HTTPException(status_code=500, detail="Não se pode instânciar uma classe singleton.")

        self.client: httpx.AsyncClient = httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=int(os.environ.get("HTTP_MAX_CONNECTIONS", 100)),
                max_keepalive_connections=int(os.environ.get("HTTP_MAX_KEEP_ALIVE_CONNECTONS", 20)),
                keepalive_expiry=int(os.environ.get("HTTP_KEEP_ALIVE_EXPIRE", 600))
            )
        )

    @classmethod
    def connect(cls) -> "HTTPxClient":
        """
        Realiza a conexão do singleton.
        """

        if not cls.__instance:
            cls.__instance = HTTPxClient()

        return cls.__instance

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
