from fastapi import Query
from typing import Optional
from src.routes import router
from src.engines.databases import DBConnectionHandler
from ..dtos import ListPermissionInputDTO, ListPermissionOutputDTO
from ..repositories import ListPermissionDAO
from ..presenters import ListPermissionPresenter


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
    offset: int = Query(0, description="Pular os N primeiros itens da lista."),
    limit: int = Query(25, description="Quantidade limite de itens que irá aparecer na listagem.")):
    """
    Listas as permissões do usuário ou grupo.
    """

    async with DBConnectionHandler() as session:
        repository = ListPermissionDAO(session=session)
        output = ListPermissionPresenter(session=session)
        data = ListPermissionInputDTO(
            name=name,
            code=code,
            group_id=group_id,
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        models = await repository.list(dto=data)
        return await output.present(models, limit=limit, offset=offset)
