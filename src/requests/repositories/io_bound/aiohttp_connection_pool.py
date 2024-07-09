from time import time
import asyncio
import aiohttp
from src.engines.logger import ProjectLoggerSingleton
from src.engines.constants import POKEAPI_URL
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocAIOHTTPConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do iohttp.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "AIOHTTPConnectionPool"

    async def make_request(self, session: aiohttp.ClientSession, limit: int = 10, offset: int = 0) -> list[dict]:
        """
        Realiza a requisição.
        """

        async with session.get(f'{POKEAPI_URL}/pokemon?limit={limit}&offset={offset}') as response:
            r1 = await response.json()
            return r1['results']

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        async with aiohttp.ClientSession() as session:
            logger.info("Abrindo conexão")
            results = []
            tasks = [
                self.make_request(session, 10, 0),
                self.make_request(session, 10, 10),
                self.make_request(session, 10, 20),
            ]
            responses: list[list[dict]] = await asyncio.gather(*tasks)
            for response in responses:
                results += response

            logger.info(f"Quantidade retornada requisição: {len(results)}")

        logger.info("Fechando conexão")
        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
