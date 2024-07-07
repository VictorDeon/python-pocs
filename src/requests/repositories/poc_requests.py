from time import time
from src.engines.logger import ProjectLoggerSingleton
from src.engines.constants import POKEAPI_URL
from src.engines.clients import HTTPxClient, HTTPxSingleton
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
        Essa requisição executa códigos de forma assincrona usando tasks
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
        Essa requisição executa códigos de forma assincrona usando tasks
        """

        ProjectLoggerSingleton.change_log_level_to_console('httpcore.connection')
        client = HTTPxSingleton.get_instance()

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
