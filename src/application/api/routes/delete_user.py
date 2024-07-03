from fastapi import Path
from src.application.api.routes import router
from src.adapters.controllers import DeleteUserController


@router.delete(
    "/users/{user_id}",
    tags=["Banco de Dados"],
    summary="Deleta um usuário."
)
async def delete_user(user_id: int = Path(..., description="ID do usuário")):
    """
    Deleta um usuário.
    """

    controller = DeleteUserController(_id=user_id)
    return await controller.execute()
