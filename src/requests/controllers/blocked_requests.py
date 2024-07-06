from fastapi import Header
from src.routes import router
from ..repositories import (
    BlockingRequestSyncController,
    BlockingRequestAsyncWithSyncController,
    NotBlockingRequestAsyncWithSyncController,
    NotBlockingRequestAsyncController,
    NotBlockingRequestTaskController
)
from ..dtos import BlockedRequestsOutputDTO
from src.engines.mediator import Mediator


@router.get(
    "/blocked-requests",
    tags=["Requests"],
    response_model=BlockedRequestsOutputDTO,
    summary="Realiza requisições bloqueantes."
)
async def blocked_requests(command: str = Header(..., description="Comando de requisição.")):
    """
    Quando executamos a requisição http para algum endpoint sync ele bloqueia
    os outros endpoints até a finalização de sua execução devido ao time.sleep
    ou qualquer outro método sync bloqueante. Já os endpoint totalmente async ele
    roda os métodos async de forma que não bloqueie a execução dos coleguinhas.

    Rode o endpoint uma vez com cada um dos headers "command" a seguir um em seguida do outro para verificar
    os que bloqueia a execução do outro, utilize o curl para fazer isso.

    `curl -X GET http://localhost:8000/blocked-requests -H 'accept: application/json' -H 'command: ...'`

    * BlockingRequestSync
    * BlockingRequestAsyncWithSync
    * NotBlockingRequestAsyncWithSync
    * NotBlockingRequestAsync
    * NotBlockingRequestTask
    """

    mediator = Mediator()
    mediator.add(BlockingRequestSyncController())
    mediator.add(BlockingRequestAsyncWithSyncController())
    mediator.add(NotBlockingRequestAsyncWithSyncController())
    mediator.add(NotBlockingRequestAsyncController())
    mediator.add(NotBlockingRequestTaskController())

    return await mediator.send(command)
