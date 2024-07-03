from fastapi import Query
from typing import Optional
from src.application.api.routes import router
from src.adapters.controllers import ListGroupsController
from src.adapters.dtos import ListGroupInputDTO, ListGroupOutputDTO


@router.get(
    "/groups",
    tags=["Banco de Dados"],
    response_model=ListGroupOutputDTO,
    summary="Lista grupos."
)
async def list_groups(
    name: Optional[str] = Query(None, description="Nome do grupo"),
    code: Optional[str] = Query(None, description="Código da permissão no grupo."),
    user_id: Optional[int] = Query(None, description="Filtrar todos os grupos de um usuário."),
    offset: Optional[int] = Query(None, description="Pular os N primeiros itens da lista."),
    limit: Optional[int] = Query(None, description="Quantidade limite de itens que irá aparecer na listagem.")):
    """
    Listas os grupos de usuários.
    """

    controller = ListGroupsController(
        input=ListGroupInputDTO(
            name=name,
            code=code,
            user_id=user_id,
            limit=limit,
            offset=offset
        )
    )
    return await controller.execute()
