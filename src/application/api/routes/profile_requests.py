from fastapi import Header, Query
from src.application.api.routes import router
from src.adapters.controllers import (
    ProfileRequestTimeitController,
)
from src.adapters.dtos import ProfileRequestsOutputDTO
from src.infrastructure.mediator.repositories import Mediator


@router.get(
    "/profile-requests",
    tags=["Requests"],
    response_model=ProfileRequestsOutputDTO,
    summary="Realiza requisições de perfil."
)
async def profile_requests(
    func: str = Query(..., description="Caminho da função que será executada."),
    qtd: int = Query(..., description="Quantidade de vezes a ser executada a função."),
    command: str = Header(..., description="Comando de requisição.")
):
    """
    Tipos de requisições para teste de profile

    * TimeIt
    """

    mediator = Mediator()
    mediator.add(ProfileRequestTimeitController())

    return await mediator.send(command, func, qtd)
