from time import time
from src.engines.logger import ProjectLoggerSingleton
from ..dtos import PocRequestsOutputDTO

SLEEP = 5
logger = ProjectLoggerSingleton.get_logger()


class PocHTTPxConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do httpx.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "HTTPxConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Essa requisição executa códigos de forma assincrona usando tasks
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        end_time = time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
