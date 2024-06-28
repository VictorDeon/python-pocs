import os
import uvicorn
import logging


if __name__ == "__main__":
    if os.environ.get("APP_ENV") in ("development", "tests"):
        logging.info("Iniciando ambiente de desenvolvimento")
        uvicorn.run("src.application.api.main:app", host="0.0.0.0", port=8000, workers=1, reload=True)
    else:
        logging.info("Iniciando ambiente de produção")
        uvicorn.run("src.application.api.main:app", host="0.0.0.0", port=8000, workers=3)
