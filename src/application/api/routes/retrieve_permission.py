from fastapi import Path
from typing import Union
from src.application.api.routes import router
from src.adapters.controllers import RetrievePermissionController, GetPermissionByIdController
from src.adapters.dtos import RetrievePermissionInputDTO, RetrievePermissionOutputDTO, ErrorOutputDTO


@router.get(
    "/permissions/{permission_id}",
    tags=["Banco de Dados"],
    response_model=Union[RetrievePermissionOutputDTO, ErrorOutputDTO],
    summary="Busca uma permissão."
)
async def retrieve_permission(permission_id: Union[int, str] = Path(..., description="ID da permissão.")):
    """
    Busca uma permissão do usuário ou grupo pelo id ou pelo código.
    """

    if permission_id.isnumeric():
        controller = GetPermissionByIdController(_id=int(permission_id))
    else:
        controller = RetrievePermissionController(input=RetrievePermissionInputDTO(code=permission_id))

    return await controller.execute()
