from fastapi import Path
from typing import Union
from src.application.api.routes import router
from src.adapters.controllers import RetrieveUserController, GetUserByIdController
from src.adapters.dtos import RetrieveUserInputDTO, RetrieveUserOutputDTO, ErrorOutputDTO


@router.get(
    "/users/{user_id}",
    tags=["Banco de Dados"],
    response_model=Union[RetrieveUserOutputDTO, ErrorOutputDTO],
    summary="Busca um usuário."
)
async def retrieve_user(user_id: Union[int, str] = Path(..., description="ID ou email do usuário.")):
    """
    Busca um usuário pelo id ou pelo email.
    """

    if user_id.isnumeric():
        controller = GetUserByIdController(_id=int(user_id))
    else:
        controller = RetrieveUserController(input=RetrieveUserInputDTO(email=user_id))

    return await controller.execute()
