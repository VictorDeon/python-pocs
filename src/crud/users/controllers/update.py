from fastapi import Path
from src.routes import router
from src.infrastructure.databases import DBConnectionHandler
from ..repositories import UpdateUserRepository
from ..dtos import UpdateUserInputDTO, UpdateUserOutputDTO
from ..presenters import UpdateUserPresenter


@router.put(
    "/users/{user_id}",
    tags=["Banco de Dados"],
    response_model=UpdateUserOutputDTO,
    summary="Atualiza um usuário."
)
async def update_user(
    data: UpdateUserInputDTO,
    user_id: int = Path(..., description="ID do usuário")):
    """
    Atualiza um usuário.
    """

    async with DBConnectionHandler() as session:
        repository = UpdateUserRepository(session=session)
        output = UpdateUserPresenter(session=session)
        model = await repository.execute(user_id, dto=data)
        return await output.present(model)
