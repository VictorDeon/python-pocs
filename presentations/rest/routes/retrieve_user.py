# pylint: disable=unused-argument
from fastapi import status
from engines.db.repositories import UserRepository
from domains.user_cases import UserRetrieve
from domains.models import User
from presentations.rest.controllers import UserRetrieveController
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

    repository = UserRepository()
    user_case = UserRetrieve(users_repository=repository)
    controller = UserRetrieveController(user_case=user_case)
    response = await controller.send(user_id)
    return response