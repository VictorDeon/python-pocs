from fastapi import Path
from src.application.api.routes import router
from src.adapters.controllers import UpdateUserController
from src.adapters.dtos import UpdateUserInputDTO, UpdateUserOutputDTO


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

    controller = UpdateUserController(user_id, input=data)
    return await controller.execute()
