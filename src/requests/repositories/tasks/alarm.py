from time import sleep
from src.engines.logger import ProjectLoggerSingleton
from .connection import celery_app

logger = ProjectLoggerSingleton.get_logger()


@celery_app.task(name='tasks.alarm')
def hit_alarm():
    """
    Dispara o alarme.
    """

    try:
        logger.info("TRIM TRIM TRIM!!!!!")
        logger.info("TRIM TRIM TRIM!!!!!")
        sleep(5)
    finally:
        logger.info("Alarme finalizado.")
