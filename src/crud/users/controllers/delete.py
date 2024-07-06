from fastapi import Path, status
from src.routes import router
from src.engines.databases import DBConnectionHandler
from ..repositories import DeleteUserRepository


@router.delete(
    "/users/{user_id}",
    tags=["Banco de Dados"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um usuário."
)
async def delete_user(user_id: int = Path(..., description="ID do usuário")):
    """
    Deleta um usuário.
    """

    async with DBConnectionHandler() as session:
        repository = DeleteUserRepository(session=session)
        return await repository.execute(user_id)
