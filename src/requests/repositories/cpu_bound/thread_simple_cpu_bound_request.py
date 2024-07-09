import math
from time import time
import threading
from concurrent.futures.thread import ThreadPoolExecutor as Executor
from src.engines.logger import ProjectLoggerSingleton
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocSimplethreadCPUBoundRequestRepository:
    """
    Testando o uso de threads simples em cpu bound
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "SimpleThreadCPUBoundRequests"

    def computer(self, start: int, end: int) -> None:
        """
        Realiza o pode computacional.
        """

        thread_name = threading.current_thread().name
        logger.info(f"Iniciando o cálculo na {thread_name}")

        i = start
        factor = 1000 * 1000
        while i < end:
            i += 1
            math.sqrt((i - factor) * (i - factor))

        logger.info(f"Finalizando o cálculo na {thread_name}")

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command} na thread {threading.current_thread().name}")

        logger.info("Criando a thread e inserindo na pool de threads prontas para execução do processador.")
        with Executor() as executor:
            executor.submit(self.computer, start=1, end=10_000_000)

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
