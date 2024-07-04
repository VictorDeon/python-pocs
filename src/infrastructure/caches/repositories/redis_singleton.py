import os
import json
import logging
from typing import Any, Union
from fastapi import HTTPException
from redis.asyncio import Redis
from redis.exceptions import ConnectionError
from src.domains.utils.formatters import JsonFormatter


class RedisSingleton:
    """
    Modulo de cache do redis como singleton.
    """

    __instance = None

    def __init__(self) -> None:
        """
        Construtor.
        """

        if self.__instance:
            raise HTTPException(status_code=500, detail="Não se pode instânciar uma classe singleton.")

        self.cache = Redis(
            host=os.environ.get("CACHE_HOST"),
            port=os.environ.get("CACHE_PORT"),
            decode_responses=True,
            socket_keepalive=True,
            max_connections=int(os.environ.get("CACHE_MAX_CONNECTIONS", 20))
        )

    @classmethod
    def get_instance(cls) -> "RedisSingleton":
        """
        Realiza a conexão do singleton e retorna sua instância.
        """

        if not cls.__instance:
            cls.__instance = RedisSingleton()

        return cls.__instance

    async def set(self, key: str, value: Any, exp: int = 86400) -> bool:
        """
        Configura o cache com expiração de 1 dia.
        """

        success = True
        try:
            await self.cache.setex(key, exp, json.dumps(value, cls=JsonFormatter, ensure_ascii=False))
        except ConnectionError as error:
            logging.error(f"Conexão com o redis falhou: {error}")
            success = False

        return success

    async def is_cached(self, key: str) -> bool:
        """
        Verifica se a chave existe no cache.
        """

        success = True
        try:
            number = await self.cache.exists(key)
            if number <= 0:
                success = False
        except ConnectionError as error:
            logging.error(f"Conexão com o redis falhou: {error}")
            success = False

        return success

    async def get(self, key: str) -> Union[dict, list]:
        """
        Pega o cache pela chave.
        """

        result = None
        if await self.is_cached(key):
            try:
                result = json.loads(await self.cache.get(key))
            except ConnectionError as error:
                logging.error(f"Conexão com o redis falhou: {error}")
            except (TypeError, json.JSONDecodeError) as error:
                logging.error(f"Ocorreu um error ao puxar os dados do cache: {error}")

        return result

    async def clean(self) -> None:
        """
        Limpa todo o cache.
        """

        await self.cache.delete(*await self.cache.keys())
