from fastapi import Path
from src.routes import router
from src.engines.databases import DBConnectionHandler
from ..dtos import UpdatePermissionInputDTO, UpdatePermissionOutputDTO
from ..repositories import UpdatePermissionDAO
from ..presenters import UpdatePermissionPresenter


@router.put(
    "/permissions/{permission_id}",
    tags=["Banco de Dados"],
    response_model=UpdatePermissionOutputDTO,
    summary="Atualiza uma permissão."
)
async def update_permission(
    data: UpdatePermissionInputDTO,
    permission_id: int = Path(..., description="ID da permissão")):
    """
    Atualiza uma permissão do usuário ou grupo.
    """

    async with DBConnectionHandler() as session:
        repository = UpdatePermissionDAO(session=session)
        output = UpdatePermissionPresenter(session=session)
        model = await repository.execute(permission_id, dto=data)
        return await output.present(model)
