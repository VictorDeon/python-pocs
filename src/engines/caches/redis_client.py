import os
import json
from typing import Any, Union
from redis.asyncio import Redis
from redis.exceptions import ConnectionError
from src.shared.formatters import JsonFormatter
from src.engines.logger import ProjectLoggerSingleton


class RedisCache:
    """
    Modulo de cache do redis.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.cache: Redis = None

    async def __aenter__(self) -> "RedisCache":
        """
        Cria a instância de cache.
        """

        self.cache = Redis(
            host=os.environ.get("CACHE_HOST"),
            port=os.environ.get("CACHE_PORT"),
            decode_responses=True,
            max_connections=int(os.environ.get("CACHE_MAX_CONNECTIONS", 20))
        )
        self.logger = ProjectLoggerSingleton.get_logger()

        return self

    async def set(self, key: str, value: Any, exp: int = 86400) -> bool:
        """
        Configura o cache com expiração de 1 dia.
        """

        success = True
        try:
            await self.cache.setex(key, exp, json.dumps(value, cls=JsonFormatter, ensure_ascii=False))
        except ConnectionError as error:
            self.logger.error(f"Conexão com o redis falhou: {error}")
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
            self.logger.error(f"Conexão com o redis falhou: {error}")
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
                self.logger.error(f"Conexão com o redis falhou: {error}")
            except (TypeError, json.JSONDecodeError) as error:
                self.logger.error(f"Ocorreu um error ao puxar os dados do cache: {error}")

        return result

    async def clean(self) -> None:
        """
        Limpa todo o cache.
        """

        await self.cache.delete(*await self.cache.keys())

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Fecha a conexão com o cache.
        """

        await self.cache.close()
