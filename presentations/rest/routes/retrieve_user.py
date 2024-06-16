# pylint: disable=unused-argument
from pydantic import BaseModel, Field
from fastapi import status
from engines.db.repositories import UserRepository
from domains.user_cases import UserRetrieve
from presentations.rest.controllers import UserRetrieveController
from . import router


class UserResponse(BaseModel):
    """
    Dados de saída.
    """

    id: int = Field(..., description="Identificador do usuário.")
    email: str = Field(..., description="Email para autenticação.")
    name: str = Field(..., description="Nome do usuário.")

    class Config:
        """
        Metadados de configuração.
        """

        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "fulano@gmail.com",
                "name": "Fulano de Tal"
            }
        }


@router.get(
    "/users/{user_id}",
    tags=["Users"],
    name="Busca de um usuário",
    responses={
        "200": {"model": UserResponse}
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
    response = controller.send(user_id)
    return response
