import time
import asyncer
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


class NotBlockingRequestAsyncWithSyncRepository:
    """
    Aqui iremos testar uma requisição assincrona com código
    sincrono, porém sem bloquear as outras requisições.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "NotBlockingRequestAsyncWithSync"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        start_time = time.time()
        logger.info(f"Iniciando a chamada {self.command}")
        await asyncer.asyncify(io_bound_method)(SLEEP)
        end_time = time.time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
