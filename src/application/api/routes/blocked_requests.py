from fastapi import Header
from src.application.api.routes import router
from src.infrastructure.mediator.repositories import Mediator


@router.get(
    "/blocked-requests",
    tags=["Requests"],
    summary="Realiza requisições bloqueantes."
)
async def blocked_requests(command: str = Header(..., description="Comando de requisição.")):
    """
    Quando executamos a requisição http para algum endpoint sync ele bloqueia
    os outros endpoints até a finalização de sua execução devido ao time.sleep
    ou qualquer outro método sync bloqueante. Já os endpoint totalmente async ele
    roda o time.sleep de forma que não bloqueie a execução dos coleguinhas.

    Rode o endpoint uma vez com cada um dos headers "command" a seguir um em seguida do outro para verificar
    os que bloqueia a execução do outro.
    > BlockingRequestSync
    > BlockingRequestAsyncWithSync
    > NotBlockingRequestAsyncWithSync
    > NotBlockingRequestAsync
    > NotBlockingRequestTask
    """

    mediator = Mediator()

    # Adicionar as controllers

    mediator.send(command)

    # controller = FindPokemonController(pokemon_id)
    # return await controller.execute()
    return None
