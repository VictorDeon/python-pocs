import time
import asyncio
from ...dtos import PocRequestsOutputDTO
from src.engines.clients import AIOHTTPSingleton
from src.engines.constants import POKEAPI_URL
from src.engines.logger import ProjectLoggerSingleton

logger = ProjectLoggerSingleton.get_logger()


class CorotineRepository:
    """
    Aqui temos alguns exemplos de scripts utilizando corotines
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "CorotineRequests"

    async def make_requests(self, queue: asyncio.Queue, limit: int, offset: int) -> None:
        """
        Monta as requisições.
        """

        logger.info("Inserindo as requisições na queue.")
        await queue.put(f'{POKEAPI_URL}/pokemon?limit={limit}&offset={offset}')

    async def process_request(self, queue: asyncio.Queue, session: AIOHTTPSingleton) -> list[dict]:
        """
        Processa as requisições.
        """

        results = []
        qtd: int = queue.qsize()
        logger.info(f"Processando as {qtd} requisições inseridas na queue.")
        while queue.qsize() > 0:
            url = await queue.get()
            response = await session.get(url)
            results += response['results']

        return results

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Essa requisição executa fibonnati usando geradores.
        """

        start_time = time.time()
        logger.info(f"Iniciando a chamada {self.command}")
        session = await AIOHTTPSingleton.get_instance()
        queue = asyncio.Queue()

        await self.make_requests(queue, 10, 0)
        await self.make_requests(queue, 10, 10)
        await self.make_requests(queue, 10, 20)
        results = await self.process_request(queue, session)
        logger.info(f"Quantidade de pokemons retornados: {len(results)}")

        end_time = time.time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
