import time
import asyncio
from ...dtos import PocRequestsOutputDTO
from src.engines.clients import AIOHTTPSingleton
from src.engines.constants import POKEAPI_URL
from src.engines.logger import ProjectLoggerSingleton

logger = ProjectLoggerSingleton.get_logger()


class CorotineTasksRepository:
    """
    Aqui temos alguns exemplos de scripts utilizando corotines com tasks
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "CorotineTaskRequests"

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
        attempt = 0
        logger.info("Processando as requisições inseridas na queue.")
        while True:
            if queue.empty():
                if attempt > 3:
                    break

                await asyncio.sleep(0.001)
                attempt += 1
                continue

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
        event_loop = asyncio.get_event_loop()

        t1 = event_loop.create_task(self.make_requests(queue, 10, 0))
        t2 = event_loop.create_task(self.make_requests(queue, 10, 0))
        t3 = event_loop.create_task(self.make_requests(queue, 10, 0))
        await asyncio.gather(t1, t2, t3)

        results = await self.process_request(queue, session)

        logger.info(f"Quantidade de pokemons retornados: {len(results)}")

        end_time = time.time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
