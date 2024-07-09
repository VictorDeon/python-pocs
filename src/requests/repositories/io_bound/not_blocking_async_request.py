import time
import asyncio
from src.engines.logger import ProjectLoggerSingleton
from ...dtos import PocRequestsOutputDTO

SLEEP = 5
logger = ProjectLoggerSingleton.get_logger()


def io_bound_method(seconds: int) -> None:
    """
    Método que bloqueia.
    """

    logger.info(f"Iniciando o método de sleep {seconds}")
    time.sleep(seconds)
    logger.info(f"Finalizando o método de sleep {seconds}")


class NotBlockingRequestAsyncRepository:
    """
    Realizando a requisição com o método de sleep assincrono.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "NotBlockingRequestAsync"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        start_time = time.time()
        logger.info(f"Iniciando a chamada {self.command}")
        await asyncio.sleep(SLEEP)
        end_time = time.time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
