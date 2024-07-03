from fastapi import Path, Query
from typing import Optional
from src.application.api.routes import router
from src.adapters.controllers import RetrieveUserController, GetUserByIdController
from src.adapters.dtos import RetrieveUserInputDTO, RetrieveUserOutputDTO


@router.get(
    "/users/{user_id}",
    tags=["Banco de Dados"],
    response_model=RetrieveUserOutputDTO,
    summary="Busca um usuário."
)
async def retrieve_user(
    user_id: int = Path(..., description="ID da permissão."),
    email: Optional[str] = Query(None, description="Email do usuário.")):
    """
    Busca um usuário pelo id ou pelo email.
    """

    if email:
        controller = RetrieveUserController(input=RetrieveUserInputDTO(email=email))
    else:
        controller = GetUserByIdController(_id=user_id)

    return await controller.execute()
