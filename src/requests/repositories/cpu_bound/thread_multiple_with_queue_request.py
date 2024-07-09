import threading
import queue
from time import time
from src.engines.logger import ProjectLoggerSingleton
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocMultiThreadWithQueueRequestRepository:
    """
    Realizando a comunicação entre threads que dependem uma das outras
    usando queue.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "MultiThreadWithQueueRequests"

    def generate_data(self, queue: queue.Queue) -> None:
        """
        Gera os dados e insere na queue.
        """

        logger.info(f"Gerando dados na {threading.current_thread().name}")

        for i in range(1, 11):
            logger.info(f"Dado {i} gerado.")
            queue.put(i)

    def process_data(self, queue: queue.Queue) -> None:
        """
        Processa os dados recebidos.
        """
        logger.info(f"Processando dados na {threading.current_thread().name}")

        while queue.qsize() > 0:
            value = queue.get()
            logger.info(f"Dado {value * 2} processado.")
            queue.task_done()

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        data_queue = queue.Queue()
        logger.info(f"Iniciando a chamada {self.command} na {threading.current_thread().name}")

        thread_generator = threading.Thread(target=self.generate_data, args=(data_queue,))
        thread_processor = threading.Thread(target=self.process_data, args=(data_queue,))

        thread_generator.start()
        thread_generator.join()

        thread_processor.start()
        thread_processor.join()

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
