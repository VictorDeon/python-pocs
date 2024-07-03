from fastapi import Path, status
from src.application.api.routes import router
from src.adapters.controllers import DeleteUserController


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

    controller = DeleteUserController(_id=user_id)
    await controller.execute()
