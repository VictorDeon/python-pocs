from time import time
from src.engines.logger import ProjectLoggerSingleton
from src.engines.caches import RedisCache, RedisSingleton
from ..dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


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
