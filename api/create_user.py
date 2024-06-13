from pydantic import BaseModel, Field
from fastapi import status
from typing import Optional
from . import router


class UserInput(BaseModel):
    """
    Dados de entrada.
    """

    email: str = Field(..., description="Email para autenticação.")
    password: str = Field(..., description="Senha para autenticação.")
    name: str = Field(..., description="Nome do usuário.")
    phone: Optional[str] = Field(None, description="Telefone do usuário")
    document: Optional[str] = Field(None, description="CPF ou CNPJ do usuário.")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fulano@gmail.com",
                "name": "Fulano de Tal",
                "password": "django1234",
                "phone": "61993884543",
                "document": "01129334532"
            }
        }


class UserResponse(BaseModel):
    """
    Resposta da criação do usuário.
    """

    success: bool = Field(..., description="Verifica se foi criado com sucesso.")

    class Config:
        json_schema_extra = {"example": {"success": True}}


@router.post(
    "/users",
    tags=["Users"],
    name="Criação de usuário",
    responses={
        "201": {"model": UserResponse}
    },
    status_code=status.HTTP_201_CREATED
)
async def create_user(data: UserInput):
    """
    Endpoint que gera um pdf a partir dos dados inseridos como parâmetro.
    """

    return {"success": True}
