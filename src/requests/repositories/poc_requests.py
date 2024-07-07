from time import time
import asyncio
import os
from src.engines.logger import ProjectLoggerSingleton
from src.engines.constants import POKEAPI_URL
from src.engines.clients import HTTPxClient, HTTPxSingleton
from src.engines.caches import RedisCache, RedisSingleton
from ..dtos import PocRequestsOutputDTO

SLEEP = 5
logger = ProjectLoggerSingleton.get_logger()


class PocHTTPxConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do httpx.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "HTTPxConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        ProjectLoggerSingleton.change_log_level_to_console('httpcore.connection')

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        async with HTTPxClient() as client:
            logger.info("Abrindo conexão")
            r1 = await client.get(f'{POKEAPI_URL}/pokemon?limit=10')
            logger.info(f"Quantidade retornada da primeira requisição: {len(r1['results'])}")
            r2 = await client.get(f'{POKEAPI_URL}/pokemon?limit=15')
            logger.info(f"Quantidade retornada da segunda requisição: {len(r2['results'])}")
            r3 = await client.get(f'{POKEAPI_URL}/pokemon?limit=20')
            logger.info(f"Quantidade retornada da ultima requisição: {len(r3['results'])}")

        logger.info("Fechando conexão")
        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocHTTPxSingletonConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do httpx com singleton.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "HTTPxSingletonConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        ProjectLoggerSingleton.change_log_level_to_console('httpcore.connection')
        client = await HTTPxSingleton.get_instance()

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        r1 = await client.get(f'{POKEAPI_URL}/pokemon?limit=10')
        logger.info(f"Quantidade retornada da primeira requisição: {len(r1['results'])}")
        r2 = await client.get(f'{POKEAPI_URL}/pokemon?limit=15')
        logger.info(f"Quantidade retornada da segunda requisição: {len(r2['results'])}")
        r3 = await client.get(f'{POKEAPI_URL}/pokemon?limit=20')
        logger.info(f"Quantidade retornada da ultima requisição: {len(r3['results'])}")

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocHTTPxSingletonSemaphoreConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do httpx com singleton e semaforo.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "HTTPxSingletonSemaphoreConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        client = await HTTPxSingleton.get_instance()
        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")

        async with asyncio.Semaphore(int(os.environ.get("SEMAPHORE", 5))):
            r1 = await client.get(f'{POKEAPI_URL}/pokemon?limit=100')
            logger.info(f"Quantidade retornada: {len(r1['results'])}")

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocCacheConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do cache.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "CacheConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        async with RedisCache() as client:
            logger.info("Abrindo conexão")
            if await client.is_cached("hello"):
                response = await client.get("hello")
                logger.info(f"Resposta pega do cache: '{response}'")
            else:
                await client.set("hello", "Hello Wold", exp=60)
                logger.info("Resposta inserida no cache.")

        logger.info("Fechando conexão")
        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocCacheSingletonConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do cache singleton.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "CacheSingletonConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        client = await RedisSingleton.get_instance()
        if await client.is_cached("hello"):
            response = await client.get("hello")
            logger.info(f"Resposta pega do cache: '{response}'")
        else:
            await client.set("hello", "Hello Wold", exp=60)
            logger.info("Resposta inserida no cache.")

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
