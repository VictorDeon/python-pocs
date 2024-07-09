import math
import multiprocessing
from time import time
from src.engines.logger import ProjectLoggerSingleton
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocSimpleProcessCPUBoundRequestRepository:
    """
    Testando o uso de processos simples em cpu bound
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "SimpleProcessCPUBoundRequests"

    def computer(self, start: int, end: int) -> None:
        """
        Realiza o pode computacional.
        """

        logger.info(f"Iniciando o cálculo {multiprocessing.current_process().name}")

        i = start
        factor = 1000 * 1000
        while i < end:
            i += 1
            math.sqrt((i - factor) * (i - factor))

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste.
        > ps aux (lista todos os processos em execução)
        > ps -C <nome-do-processo> (filtra os processos pelo nome)
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command} no processo {multiprocessing.current_process().name}")

        process = multiprocessing.Process(name="cpu-bound", target=self.computer, args=(1, 10_000_000))
        logger.info(f"Iniciando o processo {process.name} e colocando na pool de execução.")
        process.start()

        logger.info(f"Aguardando até a {process.name} ser executada e finalizada.")
        process.join()

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
