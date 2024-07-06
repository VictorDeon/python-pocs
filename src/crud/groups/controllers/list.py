from fastapi import Query
from typing import Optional
from src.routes import router
from src.engines.databases import DBConnectionHandler
from ..dtos import ListGroupInputDTO, ListGroupOutputDTO
from ..repositories import ListGroupDAO
from ..presenters import ListGroupPresenter


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
    offset: int = Query(0, description="Pular os N primeiros itens da lista."),
    limit: int = Query(25, description="Quantidade limite de itens que irá aparecer na listagem.")):
    """
    Listas os grupos de usuários.
    """

    async with DBConnectionHandler() as session:
        repository = ListGroupDAO(session=session)
        output = ListGroupPresenter(session=session)
        data = ListGroupInputDTO(
            name=name,
            code=code,
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        models = await repository.list(dto=data)
        return await output.present(models, limit=limit, offset=offset)
