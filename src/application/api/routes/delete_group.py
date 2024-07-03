from fastapi import Path
from src.application.api.routes import router
from src.adapters.controllers import DeleteGroupController


@router.delete(
    "/groups/{group_id}",
    tags=["Banco de Dados"],
    summary="Deleta um grupo."
)
async def delete_group(group_id: int = Path(..., description="ID do grupo")):
    """
    Deleta um grupo de usuários.
    """

    controller = DeleteGroupController(_id=group_id)
    return await controller.execute()
