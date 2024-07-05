import os
import uvicorn
from src.infrastructure.logger import ProjectLoggerSingleton


if __name__ == "__main__":
    logger = ProjectLoggerSingleton.get_logger()
    if os.environ.get("APP_ENV") in ("development", "tests"):
        logger.info("Iniciando ambiente de desenvolvimento")
        uvicorn.run("src.application.api.main:app", host="0.0.0.0", port=8000, workers=1, reload=True)
    else:
        logger.info("Iniciando ambiente de produção")
        uvicorn.run("src.application.api.main:app", host="0.0.0.0", port=8000, workers=3)
