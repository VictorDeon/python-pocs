from time import time
import asyncio
import os
from src.engines.logger import ProjectLoggerSingleton
from src.engines.constants import POKEAPI_URL
from src.engines.clients import HTTPxSingleton
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


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

        async with asyncio.Semaphore(int(os.environ.get("SEMAPHORE", 1))):
            results = []
            tasks = [
                client.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=0'),
                client.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=10'),
                client.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=20')
            ]
            responses: list[dict] = await asyncio.gather(*tasks)
            for response in responses:
                results += response['results']

            logger.info(f"Quantidade retornada da requisição: {len(results)}")

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
