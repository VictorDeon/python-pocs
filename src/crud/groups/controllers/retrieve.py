from fastapi import Path
from typing import Union
from src.routes import router
from src.shared.error import ErrorOutputDTO
from ..dtos import RetrieveGroupOutputDTO
from ..repositories import RetrieveGroupDAO
from ..presenters import RetrieveGroupPresenter


@router.get(
    "/groups/{group_id}",
    tags=["CRUDs"],
    response_model=Union[RetrieveGroupOutputDTO, ErrorOutputDTO],
    summary="Busca um grupo."
)
async def retrieve_group(group_id: int = Path(..., description="ID do grupo.")):
    """
    Busca um grupo de usuários.
    """

    async with DBConnectionHandler() as session:
        repository = RetrieveGroupDAO(session=session)
        output = RetrieveGroupPresenter(session=session)
        model = await repository.get_by_id(group_id)
        return await output.present(model)
