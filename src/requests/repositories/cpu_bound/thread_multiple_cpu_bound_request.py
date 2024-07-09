import math
import multiprocessing
from concurrent.futures.thread import ThreadPoolExecutor as Executor
from time import time
from src.engines.logger import ProjectLoggerSingleton
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocMultiThreadCPUBoundRequestRepository:
    """
    Testando o uso de multi threads em cpu bound
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "MultiThreadCPUBoundRequests"
        self.qtd_cores = multiprocessing.cpu_count()

    def computer(self, start: int, end: int) -> None:
        """
        Realiza o pode computacional.
        """

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
        logger.info(f"Iniciando a chamada {self.command} com {self.qtd_cores} core(s).")

        logger.info("Criando a threads e inserindo-as na pool de threads prontas para execução do processador.")
        with Executor(max_workers=self.qtd_cores) as executor:
            for n in range(1, self.qtd_cores + 1):
                initial = 50_000_000 * (n - 1) / self.qtd_cores
                end = 50_000_000 * n / self.qtd_cores
                logger.info(f"Core {n} processando de {initial} até {end} usando threads")
                executor.submit(self.computer, start=initial, end=end)

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
