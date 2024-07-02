from fastapi import Query
from typing import Optional
from src.application.api.routes import router
from src.adapters.controllers import ListPermissionsController
from src.adapters.dtos import ListPermissionInputDTO, ListPermissionOutputDTO


@router.get(
    "/permissions",
    tags=["Banco de Dados"],
    response_model=ListPermissionOutputDTO,
    summary="Lista permissões."
)
async def list_permission(
    name: Optional[str] = Query(None, description="Nome da permissão"),
    code: Optional[str] = Query(None, description="Código da permissão."),
    group_id: Optional[int] = Query(None, description="ID do grupo na qual a permissão ta vinculada"),
    user_id: Optional[int] = Query(None, description="ID do usuário na qual a permissão ta vinculada"),
    offset: Optional[int] = Query(None, description="Pular os N primeiros itens da lista."),
    limit: Optional[int] = Query(None, description="Quantidade limite de itens que irá aparecer na listagem.")):
    """
    Listas as permissões do usuário ou grupo.
    """

    controller = ListPermissionsController(
        input=ListPermissionInputDTO(
            name=name,
            code=code,
            group_id=group_id,
            user_id=user_id,
            limit=limit,
            offset=offset
        )
    )
    return await controller.execute()
