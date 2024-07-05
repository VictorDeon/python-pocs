from src.infrastructure.logger import ProjectLoggerSingleton
from src.application.api.routes import router


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
    logger.info(f"LOG: {msg}")

    return {"success": True}
