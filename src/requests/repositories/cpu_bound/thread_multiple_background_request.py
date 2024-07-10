from time import time, sleep
import threading
from src.engines.logger import ProjectLoggerSingleton
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocMultiThreadBackgroundRequestRepository:
    """
    Testando o uso de multi threads em background
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "MultiThreadBackgroundRequests"

    def countdown(self, count: int) -> None:
        """
        Contando para baixo.
        """

        while count >= 0:
            logger.info(f"Contagem regressiva na thread {threading.current_thread().name}: {count}")
            count -= 1
            sleep(3)

    def countup(self, count: int) -> None:
        """
        Contando para cima.
        """

        while count <= 10:
            logger.info(f"Contagem progressiva na thread {threading.current_thread().name}: {count}")
            count += 1
            sleep(5)

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")

        logger.info("Criando a threads e inserindo-as na pool de threads prontas para execução do processador.")
        t1 = threading.Thread(name="countdown", args=(10,), target=self.countdown)
        t1.start()

        t2 = threading.Thread(name="countup", args=(0,), target=self.countup)
        t2.start()

        logger.info("Threads inseridas no pool!")

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
