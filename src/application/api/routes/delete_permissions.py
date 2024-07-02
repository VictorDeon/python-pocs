from fastapi import Path
from src.application.api.routes import router
from src.adapters.controllers import DeletePermissionController


@router.delete(
    "/permissions/{permission_id}",
    tags=["Banco de Dados"],
    summary="Deleta uma permissão."
)
async def update_permission(permission_id: int = Path(..., description="ID da permissão")):
    """
    Deleta uma permissão do usuário ou grupo.
    """

    controller = DeletePermissionController(_id=permission_id)
    return await controller.execute()
