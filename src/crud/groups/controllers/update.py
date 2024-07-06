from fastapi import Path
from src.routes import router
from src.engines.databases import DBConnectionHandler
from ..dtos import UpdateGroupInputDTO, UpdateGroupOutputDTO
from ..presenters import UpdateGroupPresenter
from ..repositories import UpdateGroupDAO


@router.put(
    "/groups/{group_id}",
    tags=["Banco de Dados"],
    response_model=UpdateGroupOutputDTO,
    summary="Atualiza um grupo."
)
async def update_group(
    data: UpdateGroupInputDTO,
    group_id: int = Path(..., description="ID do grupo")):
    """
    Atualiza um grupo de usuários.
    """

    async with DBConnectionHandler() as session:
        repository = UpdateGroupDAO(session=session)
        output = UpdateGroupPresenter(session=session)
        model = await repository.execute(group_id, dto=data)
        return await output.present(model)
