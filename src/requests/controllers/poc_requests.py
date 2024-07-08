from fastapi import Header
from src.routes import router
from ..repositories import (
    BlockingRequestSyncRepository,
    BlockingRequestAsyncWithSyncRepository,
    NotBlockingRequestAsyncWithSyncRepository,
    NotBlockingRequestAsyncRepository,
    NotBlockingRequestTaskRepository,
    PocHTTPxConnectionPoolRepository,
    PocHTTPxCustomConnectionPoolRepository,
    PocHTTPxSingletonConnectionPoolRepository,
    PocHTTPxSingletonSemaphoreConnectionPoolRepository,
    PocAIOHTTPConnectionPoolRepository,
    PocAIOHTTPSingletonConnectionPoolRepository,
    PocAIOHTTPCustomConnectionPoolRepository,
    PocCPUBoundRequestRepository,
    PocSimplethreadCPUBoundRequestRepository,
    PocMultiplethreadCPUBoundRequestRepository,
    PocMultiThreadBackgroundCPUBoundRequestRepository,
    PocCacheConnectionPoolRepository,
    PocCacheSingletonConnectionPoolRepository,
    PocDBConnectionPoolRepository,
    PocDBSingletonConnectionPoolRepository
)
from ..dtos import PocRequestsOutputDTO
from src.engines.mediator import Mediator


@router.get(
    "/poc-requests",
    tags=["Requests"],
    response_model=PocRequestsOutputDTO,
    summary="Realiza pocs de requisições."
)
async def poc_requests(command: str = Header(..., description="Comando de requisição.")):
    """
    Quando executamos a requisição http para algum endpoint sync ele bloqueia
    os outros endpoints até a finalização de sua execução devido ao time.sleep
    ou qualquer outro método sync bloqueante. Já os endpoint totalmente async ele
    roda os métodos async de forma que não bloqueie a execução dos coleguinhas.

    Temos vários outros tipos de pocs aqui tb.

    Rode o endpoint uma vez com cada um dos headers "command" a seguir um em seguida do outro para verificar
    os que bloqueia a execução do outro, utilize o curl para fazer isso.

    `curl -X GET http://localhost:8000/poc-requests -H 'accept: application/json' -H 'command: ...'`

    * BlockingRequestSync
    * BlockingRequestAsyncWithSync
    * NotBlockingRequestAsyncWithSync
    * NotBlockingRequestAsync
    * NotBlockingRequestTask
    * HTTPxConnectionPool
    * HTTPxCustomConnectionPool
    * HTTPxSingletonConnectionPool
    * HTTPxSingletonSemaphoreConnectionPool
    * AIOHTTPConnectionPool
    * AIOHTTPCustomConnectionPool
    * AIOHTTPSingletonConnectionPool
    * CacheConnectionPool
    * CacheSingletonConnectionPool
    * DBConnectionPool
    * DBSingletonConnectionPool
    * CPUBoundRequests
    * SimpleThreadCPUBoundRequests
    * MultiThreadCPUBoundRequests
    * MultiThreadBackgroundCPUBoundRequests
    """

    mediator = Mediator()
    mediator.add(BlockingRequestSyncRepository())
    mediator.add(BlockingRequestAsyncWithSyncRepository())
    mediator.add(NotBlockingRequestAsyncWithSyncRepository())
    mediator.add(NotBlockingRequestAsyncRepository())
    mediator.add(NotBlockingRequestTaskRepository())
    mediator.add(PocHTTPxConnectionPoolRepository())
    mediator.add(PocHTTPxCustomConnectionPoolRepository())
    mediator.add(PocHTTPxSingletonConnectionPoolRepository())
    mediator.add(PocHTTPxSingletonSemaphoreConnectionPoolRepository())
    mediator.add(PocAIOHTTPConnectionPoolRepository())
    mediator.add(PocAIOHTTPCustomConnectionPoolRepository())
    mediator.add(PocAIOHTTPSingletonConnectionPoolRepository())
    mediator.add(PocCPUBoundRequestRepository())
    mediator.add(PocSimplethreadCPUBoundRequestRepository())
    mediator.add(PocMultiplethreadCPUBoundRequestRepository())
    mediator.add(PocMultiThreadBackgroundCPUBoundRequestRepository())
    mediator.add(PocCacheConnectionPoolRepository())
    mediator.add(PocCacheSingletonConnectionPoolRepository())
    mediator.add(PocDBConnectionPoolRepository())
    mediator.add(PocDBSingletonConnectionPoolRepository())

    return await mediator.send(command)
