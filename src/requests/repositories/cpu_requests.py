import math
import threading
from time import time, sleep
from src.engines.logger import ProjectLoggerSingleton
from ..dtos import PocRequestsOutputDTO

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
        logger.info(f"Iniciando a chamada {self.command}")

        logger.info("Criando a thread e inserindo na pool de threads prontas para execução do processador.")
        self.thread = threading.Thread(name="cpu-bound", target=self.computer, args=(1, 10_000_000))
        self.thread.start()

        logger.info("Processando outras coisas")
        sleep(5)
        logger.info(f"Aguardando até a {self.thread.name} ser executada e finalizada.")
        self.thread.join()

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocMultiplethreadCPUBoundRequestRepository:
    """
    Testando o uso de multi threads em cpu bound
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "MultiThreadCPUBoundRequests"

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
        logger.info(f"Iniciando a chamada {self.command}")

        logger.info("Criando a threads e inserindo-as na pool de threads prontas para execução do processador.")
        self.threads = [
            threading.Thread(name="cpu-bound01", target=self.computer, args=(1, 10_000_000)),
            threading.Thread(name="cpu-bound02", target=self.computer, args=(1, 10_000_000)),
            threading.Thread(name="cpu-bound03", target=self.computer, args=(1, 10_000_000))
        ]
        [thread.start() for thread in self.threads]

        logger.info("Processando outras coisas")
        sleep(5)
        logger.info("Aguardando até as threads serem executadas e finalizadas.")
        [thread.join() for thread in self.threads]

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocMultiThreadBackgroundCPUBoundRequestRepository:
    """
    Testando o uso de multi threads em cpu bound em background
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "MultiThreadBackgroundCPUBoundRequests"

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

        logger.info("Finalizando calculo")

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")

        logger.info("Criando a threads e inserindo-as na pool de threads prontas para execução do processador.")
        self.threads = [
            threading.Thread(name="cpu-bound01", daemon=True, target=self.computer, args=(1, 10_000_000)),
            threading.Thread(name="cpu-bound02", daemon=True, target=self.computer, args=(1, 10_000_000)),
            threading.Thread(name="cpu-bound03", daemon=True, target=self.computer, args=(1, 10_000_000))
        ]
        [thread.start() for thread in self.threads]

        logger.info("Processando outras coisas")
        sleep(5)
        logger.info("Aguardando até as threads serem executadas e finalizadas.")

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
