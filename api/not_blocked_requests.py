"""
Quando executamos a requisição http para o endpoint /async1 ele bloqueia
os outros endpoints até a finalização de sua execução devido ao time.sleep.
Já o /async2 ele roda o time.sleep de forma que não bloqueie a execução dos coleguinhas.

Rode cada um dos endpoints um em seguida do outro para verificar os que bloqueia a execução do outro.
"""

from . import router
import asyncio
import asyncer
import logging
import time


def io_bound_method(seconds: int) -> None:
    """
    Método que bloqueia.
    """

    logging.info(f"Iniciando o método de sleep {seconds}")
    time.sleep(seconds)
    logging.info(f"Finalizando o método de sleep {seconds}")


@router.get("/async1")
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


@router.get("/async2")
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


@router.get("/async3")
async def not_blocking_request2():
    """
    Realizando a requisição com o método de sleep assincrono.    
    """

    start_time = time.time()
    logging.info("Iniciando a chamada async3")
    await asyncio.sleep(5)
    end_time = time.time() - start_time
    return {"result": f"Requisição executada em {round(end_time, 2)} segundos"}


@router.get("/async4")
async def not_blocking_request3():
    """
    Essa requisição executa códigos de forma assincrona.
    """

    start_time = time.time()
    logging.info("Iniciando a chamada async4")
    asyncio.create_task(asyncio.sleep(5))
    end_time = time.time() - start_time
    return {"result": f"Requisição executada em {round(end_time, 2)} segundos"}


@router.get("/sync")
def blocking_request2():
    """
    Realiza uma requisição sincrona qualquer que bloqueia as outras requisições.
    """

    start_time = time.time()
    logging.info("Iniciando a chamada sync")
    io_bound_method(5)
    end_time = time.time() - start_time
    return {"result": f"Requisição executada em {round(end_time, 2)} segundos"}
