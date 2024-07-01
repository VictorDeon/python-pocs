from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import User
from .update_profile import UpdateProfileInputDTO


class UpdateUserInputDTO(BaseModel):
    """
    Dados de entrada para atualizar um usuário.
    """

    name: Optional[str] = Field(None, description="Nome do usuário.")
    email: Optional[str] = Field(None, description="Email do usuário.")
    work_company_cnpj: Optional[str] = Field(None, description="CNPJ da empresa na qual o usuário trabalha")
    profile: Optional[UpdateProfileInputDTO] = Field(None, description="Perfil do usuário.")
    permissions: Optional[list[str]] = Field(None, description="Lista de permissões do usuário.")
    groups: Optional[list[int]] = Field(None, description="Lista de grupos do usuário.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class UpdateUserOutputDTO(BaseModel):
    """
    Dados de saída para atualizar um usuário.
    """

    user: User = Field(..., description="Dados do usuário atualizados.")
