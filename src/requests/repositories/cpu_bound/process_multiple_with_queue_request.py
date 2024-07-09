from multiprocessing import Process, Queue
from time import time
from src.engines.logger import ProjectLoggerSingleton
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


def sender(queue: Queue) -> None:
    """
    Envia msg
    """

    logger.info("Enviando a mensagem.")
    queue.put('Hello')


def receiver(queue: Queue) -> None:
    """
    Recebe msg
    """

    msg = queue.get()
    logger.info(f"{msg} World")


class PocMultiProcessWithQueueRequestRepository:
    """
    Testando o uso da comunicação entre processos usando queue
    """

    def __init__(self) -> None:
        """
        Construtor.
        """

        self.command = "MultiProcessWithQueueRequests"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        queue = Queue()

        proccess_sender = Process(target=sender, args=(queue,))
        proccess_receiver = Process(target=receiver, args=(queue,))

        proccess_sender.start()
        proccess_receiver.start()

        proccess_sender.join()
        proccess_receiver.join()

        end_time = time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
