from fastapi import Path, status
from src.application.api.routes import router
from src.adapters.controllers import DeletePermissionController


@router.delete(
    "/permissions/{permission_id}",
    tags=["Banco de Dados"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma permissão."
)
async def delete_permission(permission_id: int = Path(..., description="ID da permissão")):
    """
    Deleta uma permissão do usuário ou grupo.
    """

    controller = DeletePermissionController(_id=permission_id)
    await controller.execute()
