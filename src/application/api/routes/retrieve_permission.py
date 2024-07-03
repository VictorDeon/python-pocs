from fastapi import Path, Query
from typing import Optional
from src.application.api.routes import router
from src.adapters.controllers import RetrievePermissionController, GetPermissionByIdController
from src.adapters.dtos import RetrievePermissionInputDTO, RetrievePermissionOutputDTO


@router.get(
    "/permissions/{permission_id}",
    tags=["Banco de Dados"],
    response_model=RetrievePermissionOutputDTO,
    summary="Busca uma permissão."
)
async def retrieve_permission(
    permission_id: int = Path(..., description="ID da permissão."),
    code: Optional[str] = Query(None, description="Código da permissão.")):
    """
    Busca uma permissão do usuário ou grupo pelo id ou pelo código.
    """

    if code:
        controller = RetrievePermissionController(input=RetrievePermissionInputDTO(code=code))
    else:
        controller = GetPermissionByIdController(_id=permission_id)

    return await controller.execute()
