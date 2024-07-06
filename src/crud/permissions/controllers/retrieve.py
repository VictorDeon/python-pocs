from fastapi import Path
from typing import Union
from src.routes import router
from src.engines.databases import DBConnectionHandler
from src.shared.error import ErrorOutputDTO
from ..dtos import RetrievePermissionInputDTO, RetrievePermissionOutputDTO
from ..repositories import RetrievePermissionDAO
from ..presenters import RetrievePermissionPresenter


@router.get(
    "/permissions/{permission_id}",
    tags=["CRUDs"],
    response_model=Union[RetrievePermissionOutputDTO, ErrorOutputDTO],
    summary="Busca uma permissão."
)
async def retrieve_permission(permission_id: Union[int, str] = Path(..., description="ID ou código da permissão.")):
    """
    Busca uma permissão do usuário ou grupo pelo id ou pelo código.
    """

    async with DBConnectionHandler() as session:
        repository = RetrievePermissionDAO(session=session)
        output = RetrievePermissionPresenter(session=session)
        if permission_id.isnumeric():
            model = await repository.get_by_id(int(permission_id))
        else:
            await repository.retrieve(dto=RetrievePermissionInputDTO(code=permission_id))

        return await output.present(model)
