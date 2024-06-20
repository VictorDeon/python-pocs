from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import User


class CreateProfileInputDTO(BaseModel):
    """
    Dados de entrada para criar o perfil do usuário.
    """

    phone: Optional[str] = Field(None, description="Telefone do usuário.")
    address: Optional[str] = Field(None, description="Endereço do usuário.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class CreatePermissionInputDTO(BaseModel):
    """
    Dados de entrada para criar permissões.
    """

    name: str = Field(..., description="Nome do permissão.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()



class CreateUserInputDTO(BaseModel):
    """
    Dados de entrada para criar um usuário
    """

    name: str = Field(..., description="Nome completo do usuário.")
    email: str = Field(..., description="Email do usuário.")
    password: str = Field(..., description="Senha de acesso do usuário.")
    profile: CreateProfileInputDTO = Field(None, description="Perfil do usuário com dados adicionais.")
    work_company_cnpj: Optional[str] = Field(None, description="Empresa na qual o usuário trabalha")
    permissions: Optional[list[int]] = Field([], description="Lista de permissões do usuário.")
    groups: Optional[list[int]] = Field([], description="Lista de grupos na qual o usuário pertence.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class CreateUserOutputDTO(BaseModel):
    """
    Dados de saída para criar um usuário
    """

    user: User = Field(..., description="Dados do usuário criado.")
