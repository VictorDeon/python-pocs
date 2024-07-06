from fastapi import Path
from typing import Union
from src.routes import router
from src.engines.databases import DBConnectionHandler
from src.shared.error import ErrorOutputDTO
from ..repositories import RetrieveUserRepository
from ..presenters import RetrieveUserPresenter
from ..dtos import RetrieveUserOutputDTO


@router.get(
    "/users/{user_id}",
    tags=["CRUDs"],
    response_model=Union[RetrieveUserOutputDTO, ErrorOutputDTO],
    summary="Busca um usuário."
)
async def retrieve_user(user_id: Union[int, str] = Path(..., description="ID ou email do usuário.")):
    """
    Busca um usuário pelo id ou pelo email.
    """

    async with DBConnectionHandler() as session:
        repository = RetrieveUserRepository(session=session)
        presenter = RetrieveUserPresenter(session=session)
        if user_id.isnumeric():
            model = await repository.get_by_id(user_id)
        else:
            model = await repository.retrieve(dto=RetrieveUserInputDTO(email=user_id))

        return await presenter.present(model)
