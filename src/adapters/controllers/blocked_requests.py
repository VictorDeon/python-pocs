import time
import logging
import asyncer
import asyncio
from src.adapters.interfaces import ControllerInterface
from src.adapters.dtos import BlockedRequestsOutputDTO


def io_bound_method(seconds: int) -> None:
    """
    Método que bloqueia.
    """

    logging.info(f"Iniciando o método de sleep {seconds}")
    time.sleep(seconds)
    logging.info(f"Finalizando o método de sleep {seconds}")


class BlockingRequestSyncController(ControllerInterface):
    """
    Realiza uma requisição sincrona qualquer que bloqueia as outras requisições.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.commmand = "BlockingRequestSync"

    async def execute(self) -> BlockedRequestsOutputDTO:
        """
        Essa requisição executa códigos de forma assincrona usando tasks
        """

        start_time = time.time()
        logging.info(f"Iniciando a chamada {self.commmand}")
        io_bound_method(5)
        end_time = time.time() - start_time
        return BlockedRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")



class BlockingRequestAsyncWithSyncController(ControllerInterface):
    """
    Aqui iremos testar uma requisição assincrona com código
    sincrono, ao executar ele bloqueia as outras requisições.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.commmand = "BlockingRequestAsyncWithSync"

    async def execute(self) -> BlockedRequestsOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        start_time = time.time()
        logging.info(f"Iniciando a chamada {self.commmand}")
        logging.info("Iniciando o código sync de sleep 5 segundos de forma sync")
        io_bound_method(5)
        logging.info("Finalizando o código sync de sleep 5 segundos de forma sync")
        end_time = time.time() - start_time
        return BlockedRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")



class NotBlockingRequestAsyncWithSyncController(ControllerInterface):
    """
    Aqui iremos testar uma requisição assincrona com código
    sincrono, porém sem bloquear as outras requisições.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.commmand = "NotBlockingRequestAsyncWithSync"

    async def execute(self) -> BlockedRequestsOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        start_time = time.time()
        logging.info(f"Iniciando a chamada {self.commmand}")
        await asyncer.asyncify(io_bound_method)(5)
        end_time = time.time() - start_time
        return BlockedRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class NotBlockingRequestAsyncController(ControllerInterface):
    """
    Realizando a requisição com o método de sleep assincrono.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.commmand = "NotBlockingRequestAsync"

    async def execute(self) -> BlockedRequestsOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        start_time = time.time()
        logging.info(f"Iniciando a chamada {self.commmand}")
        await asyncio.sleep(5)
        end_time = time.time() - start_time
        return BlockedRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class NotBlockingRequestTaskController(ControllerInterface):
    """
    Aqui iremos testar uma requisição assincrona com código
    sincrono, porém sem bloquear as outras requisições.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.commmand = "NotBlockingRequestTask"

    async def execute(self) -> BlockedRequestsOutputDTO:
        """
        Essa requisição executa códigos de forma assincrona usando tasks
        """

        start_time = time.time()
        logging.info(f"Iniciando a chamada {self.commmand}")
        asyncio.create_task(asyncio.sleep(5))
        end_time = time.time() - start_time
        return BlockedRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
