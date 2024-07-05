from src.infrastructure.logger import ProjectLoggerSingleton
from src.application.api.routes import router
import threading
import time


def worker(thread_id):
    logger = ProjectLoggerSingleton.get_logger()
    logger.info("Thread %d started", thread_id)
    time.sleep(3)
    logger.info("Thread %d ended", thread_id)


@router.get(
    "/logger-requests",
    tags=["Requests"],
    summary="Realiza requisições com logger."
)
async def logger_request():
    """
    Testando o uso de loggs
    """

    msg = "Opa sou o logger"
    logger = ProjectLoggerSingleton.get_logger()
    logger.info("LOG: %s", msg)

    threads: list[threading.Thread] = []
    for i in range(3):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return {"success": True}
