from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import User


class ListUserInputDTO(BaseModel):
    """
    Dados de entrada para listar usuários.
    """

    name: Optional[str] = Field(None, description="Filtrar pelo nome do usuário.")
    email: Optional[str] = Field(None, description="Filtrar pelo email do usuário.")
    groups: Optional[list[str]] = Field([], description="Filtrar pelos grupos.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class ListUserOutputDTO(BaseModel):
    """
    Dados de saída para listar usuários.
    """

    users: list[User] = Field([], description="Lista de usuários filtrados.")
