import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI
from pyinstrument import Profiler
from src.application.api.routes import router
from src.infrastructure.logger import ProjectLoggerSingleton

logger = ProjectLoggerSingleton.get_logger()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Executado antes e depois de dar o start no fastapi
    """

    logger.debug("Iniciando o projeto.")

    yield

    logger.debug("Finalizando o projeto.")


app = FastAPI(
    title="VKSoftware",
    version="1.0.0",
    redoc_url="/redocs",
    docs_url="/docs",
    lifespan=lifespan
)


@app.middleware("http")
async def profile_request(request: Request, call_next):
    PROFILE = int(os.environ.get("PROFILE", 0))
    if PROFILE:
        logger.info("Iniciando o profiling das requisições.")
        profiler = Profiler(interval=0.001, async_mode="enabled")
        profiler.start()
        response = await call_next(request)
        profiler.stop()
        profile_path = Path("/software/assets/profiles")
        profile_path.mkdir(parents=True, exist_ok=True)
        full_path = profile_path / "profile.html"
        string_path = str(full_path.resolve())
        profiler.write_html(string_path)
        logger.info(f"Finalizando o profiling da requisição {request.url} e salvando em {string_path}.")
        return response
    else:
        return await call_next(request)


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
