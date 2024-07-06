from typing import Optional
from pydantic import BaseModel, Field
from .retrieve import RetrieveUserOutputDTO


class CreateProfileInputDTO(BaseModel):
    """
    Dados de entrada para criar um perfil.
    """

    phone: Optional[str] = Field(None, description="Telefone do usuário.")
    address: Optional[str] = Field(None, description="Endereço do usuário.")

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
    permissions: Optional[list[str]] = Field([], description="Lista de códigos das permissões do usuário.")
    groups: Optional[list[int]] = Field([], description="Lista de grupos na qual o usuário pertence.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "name": "Fulano 01",
                "email": "fulano01@gmail.com",
                "password": "Django1234",
                "profile": {
                    "address": "Rua ABC bairro Ipanema N 244, Sorocaba, SP. CEP: 7059483",
                    "phone": "61998283934"
                },
                "work_company_cnpj": "11111111111111",
                "groups": [226],
                "permissions": ["permission_create", "permission_update"],
            }
        }

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class CreateUserOutputDTO(RetrieveUserOutputDTO):
    """
    Dados de saída para criar um usuário
    """

    pass
