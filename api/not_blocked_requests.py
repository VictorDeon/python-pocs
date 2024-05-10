"""
Quando executamos a requisição http para algum endpoint sync ele bloqueia
os outros endpoints até a finalização de sua execução devido ao time.sleep.
Já os endpoint totalmente async ele roda o time.sleep de forma que não bloqueie
a execução dos coleguinhas.

Rode cada um dos endpoints um em seguida do outro para verificar os que bloqueia a execução do outro.
"""

from pydantic import BaseModel, Field
from . import router
import asyncio
import asyncer
import logging
import time


class Error(BaseModel):
    """
    Retorna os dados de error.
    """

    message: str = Field(..., title="Mensagem", description="Mensagem de erro.")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Parâmetro nome obrigatório.",
            }
        }


class Response(BaseModel):
    """
    Retorna os dados de sucesso.
    """

    result: str = Field(..., title="Resultado", description="Tempo de execução da requisição.")

    class Config:
        json_schema_extra = {
            "example": {
                "result": "Requisição executada em 5.4 segundos",
            }
        }

def io_bound_method(seconds: int) -> None:
    """
    Método que bloqueia.
    """

    logging.info(f"Iniciando o método de sleep {seconds}")
    time.sleep(seconds)
    logging.info(f"Finalizando o método de sleep {seconds}")


@router.get(
    "/blocking-request-async",
    summary="Blocking Request Async",
    responses={
        200: {'model': Response},
        422: {'model': Error},
    },
    tags=['Requests']
)
async def blocking_request1():
    """
    Aqui iremos testar uma requisição assincrona com código
    sincrono, ao executar ele bloqueia as outras requisições.    
    """

    start_time = time.time()
    logging.info("Iniciando a chamada async2")
    logging.info("Iniciando o código sync de sleep 30 segundos de forma sync")
    io_bound_method(5)
    logging.info("Finalizando o código sync de sleep 30 segundos de forma sync")
    end_time = time.time() - start_time
    return {"result": f"Requisição executada em {round(end_time, 2)} segundos"}


@router.get(
    "/not-blockeing-request-async-with-sync",
    summary="Not Blocking Request Async With Sync code",
    responses={
        200: {'model': Response},
        422: {'model': Error},
    },
    tags=['Requests']
)
async def not_blocking_request1():
    """
    Aqui iremos testar uma requisição assincrona com código
    sincrono, porém sem bloquear as outras requisições.    
    """

    start_time = time.time()
    logging.info("Iniciando a chamada async2")
    await asyncer.asyncify(io_bound_method)(5)
    end_time = time.time() - start_time
    return {"result": f"Requisição executada em {round(end_time, 2)} segundos"}


@router.get(
    "/not-blocking-request-async",
    summary="Not Blocking Request All Async",
    responses={
        200: {'model': Response},
        422: {'model': Error},
    },
    tags=['Requests']
)
async def not_blocking_request2():
    """
    Realizando a requisição com o método de sleep assincrono.    
    """

    start_time = time.time()
    logging.info("Iniciando a chamada async3")
    await asyncio.sleep(5)
    end_time = time.time() - start_time
    return {"result": f"Requisição executada em {round(end_time, 2)} segundos"}


@router.get(
    "/not-blocking-request-task",
    summary="Not Blocking Request Async Task",
    responses={
        200: {'model': Response},
        422: {'model': Error},
    },
    tags=['Requests']
)
async def not_blocking_request3():
    """
    Essa requisição executa códigos de forma assincrona.
    """

    start_time = time.time()
    logging.info("Iniciando a chamada async4")
    asyncio.create_task(asyncio.sleep(5))
    end_time = time.time() - start_time
    return {"result": f"Requisição executada em {round(end_time, 2)} segundos"}


@router.get(
    "/blocking-request-sync",
    summary="Blocking Request Sync",
    responses={
        200: {'model': Response},
        422: {'model': Error},
    },
    tags=['Requests']
)
def blocking_request2():
    """
    Realiza uma requisição sincrona qualquer que bloqueia as outras requisições.
    """

    start_time = time.time()
    logging.info("Iniciando a chamada sync")
    io_bound_method(5)
    end_time = time.time() - start_time
    return {"result": f"Requisição executada em {round(end_time, 2)} segundos"}
