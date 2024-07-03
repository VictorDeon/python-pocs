from fastapi import status
from src.application.api.routes import router
from src.adapters.controllers import CreatePermissionController
from src.adapters.dtos import CreatePermissionOutputDTO, CreatePermissionInputDTO


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

    controller = CreatePermissionController(input=data)
    return await controller.execute()
