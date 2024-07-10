from time import time
import asyncio
from src.engines.logger import ProjectLoggerSingleton
from src.engines.constants import POKEAPI_URL
from src.engines.clients import AIOHTTPSingleton
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocAIOHTTPSingletonConnectionPoolRepository:
    """
    Testando o uso do pool de conexões singleton do iohttp.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "AIOHTTPSingletonConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        session = await AIOHTTPSingleton.get_instance()

        results = []
        tasks = [
            session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=0'),
            session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=10'),
            session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=20'),
        ]
        responses: list[dict] = await asyncio.gather(*tasks)
        for response in responses:
            results += response['results']

        logger.info(f"Quantidade de pokemons retornados: {len(results)}")

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
