import math
from time import time
from src.engines.logger import ProjectLoggerSingleton
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocCPUBoundRequestRepository:
    """
    Testando o uso de requisição cpu bound
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "CPUBoundRequests"

    def computer(self, start: int, end: int) -> None:
        """
        Realiza o pode computacional.
        """

        logger.info("Iniciando o cálculo cpu-bound")

        i = start
        factor = 1000 * 1000
        while i < end:
            i += 1
            math.sqrt((i - factor) * (i - factor))

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        start = 1
        end = 10_000_000
        logger.info(f"Iniciando a chamada {self.command}")

        self.computer(start, end)

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
