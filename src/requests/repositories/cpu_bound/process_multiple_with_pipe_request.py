from multiprocessing import Pipe, Process, current_process
from multiprocessing.connection import Connection
from time import time
from src.engines.logger import ProjectLoggerSingleton
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


def sender(connection: Connection) -> None:
    """
    Envia msg
    """

    logger.info(f"Enviando a mensagem pelo processo {current_process().name}.")
    connection.send('Hello')


def receiver(connection: Connection) -> None:
    """
    Recebe msg
    """

    msg = connection.recv()
    logger.info(f"Mensagem recebida no processo {current_process().name}: {msg} World")


class PocMultiProcessWithPipeRequestRepository:
    """
    Testando o uso da comunicação entre processos usando pipe
    """

    def __init__(self) -> None:
        """
        Construtor.
        """

        self.command = "MultiProcessWithPipeRequests"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command} no processo {current_process().name}")
        # Queremos uma conexão enviar e a outra só receber por isso duplex=False
        # Se quisermos ambas enviar e receber usamos o duplex=True
        connection_receiver, connection_sender = Pipe(duplex=False)

        proccess_sender = Process(target=sender, args=(connection_sender,))
        proccess_receiver = Process(target=receiver, args=(connection_receiver,))

        proccess_sender.start()
        proccess_receiver.start()

        proccess_sender.join()
        proccess_receiver.join()

        end_time = time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
