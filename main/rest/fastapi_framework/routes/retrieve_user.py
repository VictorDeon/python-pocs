from pydantic import BaseModel, Field
from fastapi import status, Request
from main.rest.adapters import fastapi_adapter
from main.rest.composers import user_retriever_compose
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
async def retrieve_user(request: Request):
    """
    Endpoint que retorna os dados de um usuário.
    """

    response = await fastapi_adapter(request, user_retriever_compose())
    return response
