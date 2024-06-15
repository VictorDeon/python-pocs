import logging
from datetime import datetime
from pytz import timezone
from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI
from main.routes import router

sp = timezone("America/Sao_Paulo")
logging.Formatter.converter = lambda *args: datetime.now(tz=sp).timetuple()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)
logging.getLogger('httpx').propagate = False
logging.getLogger('asyncio').propagate = False
logging.getLogger('urllib3').propagate = False

app = FastAPI(
    title="VKSoftware",
    version="1.0.0",
    redoc_url="/redocs",
    docs_url="/docs",
)


@app.get("/")
def health_check():
    """
    Health check da aplicação.
    """

    return {"success": True}


app.include_router(router)


@app.exception_handler(HTTPException)
def handle_http_exception(_: Request, error: HTTPException) -> JSONResponse:
    """
    Mapeia as exceções.
    """

    return JSONResponse(
        status_code=error.status_code or status.HTTP_400_BAD_REQUEST,
        content={"message": error.detail},
        headers=error.headers  # type: ignore
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Melhora os inputs de error.
    """

    content = jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    try:
        attr = content['detail'][0]['loc'][-1]
        _type = content['detail'][0]['type']

        msg_map = {
            "value_error.missing": f"Parâmetro {attr} obrigatório.",
            "type_error.integer": f"Parâmetro {attr} deve ser do tipo inteiro."
        }

        result = {"message": msg_map[_type]}
    except Exception:
        result = {"message": str(content['detail'])}

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=result,
    )


@app.exception_handler(Exception)
def generic_exception(_: Request, error: Exception) -> JSONResponse:
    """
    Mapeia as exceções genêricas.
    """

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(error)}
    )
