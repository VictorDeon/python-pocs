from fastapi import Path, status
from src.application.api.routes import router
from src.adapters.controllers import DeleteGroupController


@router.delete(
    "/groups/{group_id}",
    tags=["Banco de Dados"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um grupo."
)
async def delete_group(group_id: int = Path(..., description="ID do grupo")):
    """
    Deleta um grupo de usuários.
    """

    controller = DeleteGroupController(_id=group_id)
    await controller.execute()
