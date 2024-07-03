from fastapi import Path
from src.application.api.routes import router
from src.adapters.controllers import UpdateGroupController
from src.adapters.dtos import UpdateGroupInputDTO, UpdateGroupOutputDTO


@router.put(
    "/groups/{group_id}",
    tags=["Banco de Dados"],
    response_model=UpdateGroupOutputDTO,
    summary="Atualiza um grupo."
)
async def update_group(
    data: UpdateGroupInputDTO,
    group_id: int = Path(..., description="ID do grupo")):
    """
    Atualiza um grupo de usuários.
    """

    controller = UpdateGroupController(group_id, input=data)
    return await controller.execute()
