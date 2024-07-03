from fastapi import Path
from src.application.api.routes import router
from src.adapters.controllers import GetGroupByIdController
from src.domains.entities import Group


@router.get(
    "/groups/{group_id}",
    tags=["Banco de Dados"],
    response_model=Group,
    summary="Busca um grupo."
)
async def retrieve_group(group_id: int = Path(..., description="ID do grupo.")):
    """
    Busca um grupo de usuários.
    """

    controller = GetGroupByIdController(_id=group_id)
    return await controller.execute()
