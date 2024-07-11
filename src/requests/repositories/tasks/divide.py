from src.engines.logger import ProjectLoggerSingleton
from .connection import celery_app, retry_attempt


@celery_app.task(name='tasks.divide', bind=True, max_retries=5, soft_time_limit=5)
def divide(self, x: int, y: int) -> float:
    """
    Realiza a divisão de dois inteiros e se falhar tente novamente.
    """

    logger = ProjectLoggerSingleton.get_logger()

    try:
        result = x / y
        logger.info(f"{x} / {y} = {result}")
    except Exception as e:
        attempts = retry_attempt(self.request.retries)
        logger.error(f"Ocorreu uma divisão por zero. Retentando após {attempts} segundos.")
        raise self.retry(exc=e, countdown=attempts)

    return result
