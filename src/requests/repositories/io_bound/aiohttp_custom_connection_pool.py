from time import time
import asyncio
from src.engines.logger import ProjectLoggerSingleton
from src.engines.constants import POKEAPI_URL
from src.engines.clients import AIOHTTPClient
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocAIOHTTPCustomConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do iohttp customizado.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "AIOHTTPCustomConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        async with AIOHTTPClient() as session:
            logger.info("Abrindo conexão")
            results = []
            tasks = [
                session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=0'),
                session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=10'),
                session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=20'),
            ]
            responses: list[dict] = await asyncio.gather(*tasks)
            for response in responses:
                results += response['results']

            logger.info(f"Quantidade retornada requisição: {len(results)}")

        logger.info("Fechando conexão")
        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
