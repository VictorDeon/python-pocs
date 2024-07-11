from time import time
from src.engines.logger import ProjectLoggerSingleton
from ..dtos import PocRequestsOutputDTO
from .tasks import add, get_result, divide


logger = ProjectLoggerSingleton.get_logger()


class CeleryTaskRepository:
    """
    Constroladora para tasks assincronas com celery.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "CeleryTaskRequest"

    async def execute(self) -> dict:
        """
        Executa os comandos para gerar o resultado.
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        divide.delay(1, 0)
        result = add.delay(1, 2)
        logger.info(f"Resultado: {get_result(result)}")
        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
