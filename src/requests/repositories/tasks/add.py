from time import sleep
from src.engines.logger import ProjectLoggerSingleton
from .connection import celery_app


@celery_app.task(name='tasks.add')
def add(x: int, y: int) -> int:
    """
    Realiza a soma de dois inteiros.
    """

    logger = ProjectLoggerSingleton.get_logger()

    result = x + y
    sleep(10)
    logger.info(f"{x} + {y} = {result}")
    return result
