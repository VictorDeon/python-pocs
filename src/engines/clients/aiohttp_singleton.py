import json
import aiohttp
import time
import os
from aiohttp.web import HTTPError
from fastapi.exceptions import HTTPException
from src.engines.logger import ProjectLoggerSingleton


class AIOHTTPSingleton:
    """
    Client HTTP aio Singleton.
    """

    __instance = None
    cache_connection_pool_expire = int(os.environ.get("HTTP_KEEP_ALIVE_EXPIRE", 120))

    def __init__(self) -> None:
        """
        Construtor.
        """

        if self.__instance:
            raise HTTPException(status_code=500, detail="Não se pode instânciar uma classe singleton.")

        self.logger = ProjectLoggerSingleton.get_logger()
        self.logger.info("Abrindo a pool de conexões")
        self.connection_pool_started = time.time()
        self.client: aiohttp.ClientSession = aiohttp.ClientSession()

    @classmethod
    async def get_instance(cls) -> "AIOHTTPSingleton":
        """
        Realiza a conexão do singleton e retorna sua instância.
        """

        if not cls.__instance:
            cls.__instance = AIOHTTPSingleton()

        connection_pool_time = time.time() - cls.__instance.connection_pool_started
        cls.__instance.logger.info(f"Ja se passaram {connection_pool_time:.2f} ms no pool de conexões.")
        if connection_pool_time >= cls.cache_connection_pool_expire:
            await cls.__instance.client.close()
            cls.__instance = None
            cls.__instance = AIOHTTPSingleton()

        return cls.__instance

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
