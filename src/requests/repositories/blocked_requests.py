import time
import asyncio
import asyncer
from ..dtos import PocRequestsOutputDTO
from src.engines.logger import ProjectLoggerSingleton

SLEEP = 5
logger = ProjectLoggerSingleton.get_logger()


def io_bound_method(seconds: int) -> None:
    """
    Método que bloqueia.
    """

    logger.info(f"Iniciando o método de sleep {seconds}")
    time.sleep(seconds)
    logger.info(f"Finalizando o método de sleep {seconds}")


class BlockingRequestSyncRepository:
    """
    Realiza uma requisição sincrona qualquer que bloqueia as outras requisições.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "BlockingRequestSync"

    def execute(self) -> PocRequestsOutputDTO:
        """
        Essa requisição executa códigos de forma assincrona usando tasks
        """

        start_time = time.time()
        logger.info(f"Iniciando a chamada {self.command}")
        io_bound_method(SLEEP)
        end_time = time.time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class BlockingRequestAsyncWithSyncRepository:
    """
    Aqui iremos testar uma requisição assincrona com código
    sincrono, ao executar ele bloqueia as outras requisições.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "BlockingRequestAsyncWithSync"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        start_time = time.time()
        logger.info(f"Iniciando a chamada {self.command}")
        io_bound_method(SLEEP)
        end_time = time.time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class NotBlockingRequestAsyncWithSyncRepository:
    """
    Aqui iremos testar uma requisição assincrona com código
    sincrono, porém sem bloquear as outras requisições.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "NotBlockingRequestAsyncWithSync"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        start_time = time.time()
        logger.info(f"Iniciando a chamada {self.command}")
        await asyncer.asyncify(io_bound_method)(SLEEP)
        end_time = time.time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class NotBlockingRequestAsyncRepository:
    """
    Realizando a requisição com o método de sleep assincrono.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "NotBlockingRequestAsync"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        start_time = time.time()
        logger.info(f"Iniciando a chamada {self.command}")
        await asyncio.sleep(SLEEP)
        end_time = time.time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class NotBlockingRequestTaskRepository:
    """
    Aqui iremos testar uma requisição assincrona com código
    sincrono, porém sem bloquear as outras requisições.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "NotBlockingRequestTask"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Essa requisição executa códigos de forma assincrona usando tasks
        """

        start_time = time.time()
        logger.info(f"Iniciando a chamada {self.command}")
        asyncio.create_task(asyncio.sleep(SLEEP))
        end_time = time.time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
