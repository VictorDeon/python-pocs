from fastapi import status
from src.adapters.dtos import FindUserOutputDTO
from src.adapters.controllers import UserRetrieveController
from . import router


@router.get(
    "/users/{user_id}",
    tags=["Users"],
    name="Busca de um usuário",
    responses={
        "200": {"model": FindUserOutputDTO}
    },
    status_code=status.HTTP_200_OK
)
async def retrieve_user(user_id: int):
    """
    Endpoint que retorna os dados de um usuário.
    """

    controller = UserRetrieveController(user_id=user_id)
    return await controller.execute()
