import time
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


class BlockingRequestSyncRepository:
    """
    Realiza uma requisição sincrona qualquer que bloqueia as outras requisições.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "BlockingRequestSync"

    def execute(self) -> PocRequestsOutputDTO:
        """
        Essa requisição executa códigos de forma assincrona usando tasks
        """

        start_time = time.time()
        logger.info(f"Iniciando a chamada {self.command}")
        io_bound_method(SLEEP)
        end_time = time.time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
