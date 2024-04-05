from fastapi import FastAPI
from api import router
from datetime import datetime
from pytz import timezone
import logging

sp = timezone("America/Sao_Paulo")
logging.getLogger().setLevel(logging.INFO)
logging.getLogger('urllib3').propagate = False
logging.getLogger('httpx').propagate = False
logging.getLogger('asyncio').propagate = False
logging.Formatter.converter = lambda *args: datetime.now(tz=sp).timetuple()
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")

app = FastAPI(
    title="VKSoftware",
    version="1.0.0",
    redoc_url="/docs",
    docs_url=None,
)


@app.get("/")
def health_check():
    return {"success": True}


app.include_router(router)
