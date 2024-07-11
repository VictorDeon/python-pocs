from typing import Any
from time import sleep
from celery import Celery
from celery.result import AsyncResult, allow_join_result
from src.engines.logger import ProjectLoggerSingleton


celery_app = Celery('tasks', backend="redis://redis:6379/0", broker="redis://redis:6379/0")
logger = ProjectLoggerSingleton.get_logger()


def get_result(result) -> Any:
    """
    Pega o resultado da tarefa assincrona.
    """

    time = 3
    while True:
        async_result = AsyncResult(result.task_id, app=celery_app)
        status = async_result.status
        logger.info(f"Status do resultado da task é {status}")
        if async_result.ready():
            with allow_join_result():
                response = async_result.get()
                logger.info(f"Resultado gerado em {time} segundos: {response}")
                break

        sleep(3)
        time += 3

    return response


def retry_attempt(attempts):
    """
    Realiza as tentativas com intervalos diferentes.
    Ex: 1, 2, 4, 8, 16, 31
    """

    return 2 ** attempts
