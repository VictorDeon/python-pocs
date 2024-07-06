from fastapi import status
from src.engines.databases import DBConnectionHandler
from src.routes import router
from ..repositories import CreatePermissionDAO
from ..dtos import CreatePermissionOutputDTO, CreatePermissionInputDTO
from ..presenters import CreatePermissionPresenter


@router.post(
    "/permissions",
    tags=["Banco de Dados"],
    response_model=CreatePermissionOutputDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma permissão."
)
async def create_permission(data: CreatePermissionInputDTO):
    """
    Cria uma permissão do usuário ou grupo.
    """

    async with DBConnectionHandler() as session:
        repository = CreatePermissionDAO(session=session)
        output = CreatePermissionPresenter(session=session)
        model = await repository.execute(dto=data)
        return await output.present(model)
