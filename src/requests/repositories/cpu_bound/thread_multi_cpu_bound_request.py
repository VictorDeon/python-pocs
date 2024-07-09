import math
import threading
import multiprocessing
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

        logger.info("Iniciando o cálculo")

        i = start
        factor = 1000 * 1000
        while i < end:
            i += 1
            math.sqrt((i - factor) * (i - factor))

        logger.info("Finalizando calculo")

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command} com {self.qtd_cores} core(s).")

        logger.info("Criando a threads e inserindo-as na pool de threads prontas para execução do processador.")
        threads: list[threading.Thread] = []
        for n in range(1, self.qtd_cores + 1):
            initial = 10_000_000 * (n - 1) / self.qtd_cores
            end = 10_000_000 * n / self.qtd_cores
            logger.info(f"Core {n} processando de {initial} até {end}")
            threads.append(
                threading.Thread(
                    name=f"cpu-bound-core-{n}",
                    daemon=True,
                    target=self.computer,
                    kwargs={"start": initial, "end": end}
                ),
            )

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
