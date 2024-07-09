import math
import multiprocessing
from time import time
from src.engines.logger import ProjectLoggerSingleton
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocMultiProcessCPUBoundRequestRepository:
    """
    Testando o uso de multi processos em cpu bound
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "MultiProcessCPUBoundRequests"
        self.qtd_cores = multiprocessing.cpu_count()
        self.main_proccess = multiprocessing.current_process().name

    def computer(self, start: int, end: int) -> None:
        """
        Realiza o pode computacional.
        """

        logger.info(f"Iniciando o cálculo {multiprocessing.current_process().name}")

        i = start
        factor = 1000 * 1000
        result = 0
        while i < end:
            i += 1
            result = math.sqrt((i - factor) * (i - factor))

        logger.info("Finalizando calculo")
        return result

    def process_name_into_pool(self) -> str:
        """
        Mostra o processo que está sendo executado dentro da pool
        """

        name = multiprocessing.current_process().name
        logger.info(f"Iniciando o processo: {name}")
        return name

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        pool = multiprocessing.Pool(self.qtd_cores, initializer=self.process_name_into_pool)
        logger.info(f"Iniciando a chamada {self.command} no processo {self.main_proccess} com {self.qtd_cores} core(s).")

        logger.info("Criando os processos e inserindo-as na pool de processos para execução.")
        inputs: list[dict] = []
        for n in range(1, self.qtd_cores + 1):
            initial = 10_000_000 * (n - 1) / self.qtd_cores
            end = 10_000_000 * n / self.qtd_cores
            logger.info(f"Core {n} processando de {initial} até {end}")
            inputs.append({"start": initial, "end": end})

        results = pool.map(lambda i: self.computer(**i), inputs)
        logger.info(f"Resultados: {results}")

        pool.close()
        pool.join()

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
