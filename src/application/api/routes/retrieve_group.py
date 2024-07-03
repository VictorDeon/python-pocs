from fastapi import Path
from typing import Union
from src.application.api.routes import router
from src.adapters.controllers import GetGroupByIdController
from src.adapters.dtos import RetrieveGroupOutputDTO, ErrorOutputDTO


@router.get(
    "/groups/{group_id}",
    tags=["Banco de Dados"],
    response_model=Union[RetrieveGroupOutputDTO, ErrorOutputDTO],
    summary="Busca um grupo."
)
async def retrieve_group(group_id: int = Path(..., description="ID do grupo.")):
    """
    Busca um grupo de usuários.
    """

    controller = GetGroupByIdController(_id=group_id)
    return await controller.execute()
