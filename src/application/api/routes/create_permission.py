from fastapi import Header
from src.application.api.routes import router
from src.adapters.controllers import CreatePermissionController
from src.adapters.dtos import CreatePermissionOutputDTO, CreatePermissionInputDTO


@router.post(
    "/permissions",
    tags=["Permissions"],
    response_model=CreatePermissionOutputDTO,
    summary="Cria uma permissão."
)
async def create_permission(input: CreatePermissionInputDTO):
    """
    Cria uma permissão do usuário ou grupo.
    """

    controller = CreatePermissionController(input=input)
    return await controller.execute()
