from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import User


class ListUserInputDTO(BaseModel):
    """
    Dados de entrada para listar usuários.
    """

    name: Optional[str] = Field(None, description="Filtrar todos os usuário com nome.")
    email: Optional[str] = Field(None, description="Filtrar todos os usuário com um email.")
    groups: Optional[list[int]] = Field(None, description="Filtrar todos os usuário de um determinado grupo.")
    work_company_cnpj: Optional[str] = Field(False, description="Listar todos os funcionários de uma empresa.")

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
