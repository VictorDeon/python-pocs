from fastapi import Path
from src.application.api.routes import router
from src.adapters.controllers import UpdatePermissionController
from src.adapters.dtos import UpdatePermissionInputDTO, UpdatePermissionOutputDTO


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

    controller = UpdatePermissionController(permission_id, input=data)
    return await controller.execute()
