# pylint: disable=unused-argument
from fastapi import status
from src.infrastructure.databases.daos import UserDAO
from src.domains.user_cases import UserRetrieve
from src.domains.entities import User
from src.adapters.controllers import UserRetrieveController
from . import router


@router.get(
    "/users/{user_id}",
    tags=["Users"],
    name="Busca de um usuário",
    responses={
        "200": {"model": User}
    },
    status_code=status.HTTP_200_OK
)
async def retrieve_user(user_id: int):
    """
    Endpoint que retorna os dados de um usuário.
    """

    repository = UserDAO()
    user_case = UserRetrieve(users_repository=repository)
    controller = UserRetrieveController(user_case=user_case)
    response = await controller.send(user_id)
    return response
