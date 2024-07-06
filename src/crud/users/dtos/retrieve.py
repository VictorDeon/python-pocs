from typing import Optional
from pydantic import BaseModel, Field
from src.crud.permissions.dtos import RetrievePermissionOutputDTO
from src.crud.groups.dtos import RetrieveGroupOutputDTO


class RetrieveUserInputDTO(BaseModel):
    """
    Dados de entrada para buscar um usuário.
    """

    email: str = Field(..., description="Email do usuário.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class RetrieveProfileOutputDTO(BaseModel):
    """
    Dados de saída para buscar um perfil do usuário.
    """

    id: int = Field(..., description="Identificador único do perfil do usuário.")
    phone: Optional[str] = Field(None, description="Telefone do usuário.")
    address: Optional[str] = Field(None, description="Endereço do usuário.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class RetrieveUserOutputDTO(BaseModel):
    """
    Dados de saída para buscar um usuário.
    """

    id: int = Field(..., description="Identificador único do usuário.")
    name: str = Field(..., description="Nome completo do usuário.")
    email: str = Field(..., description="Email do usuário.")
    profile: RetrieveProfileOutputDTO = Field(..., description="Perfil do usuário com dados adicionais.")
    companies: list[str] = Field([], description="CNPJ das empresas na qual o usuário é dono.")
    work_company: Optional[str] = Field(None, description="CNPJ da empresa na qual o usuário trabalha.")
    permissions: list[RetrievePermissionOutputDTO] = Field([], description="Lista de permissões do usuário.")
    groups: list[RetrieveGroupOutputDTO] = Field([], description="Lista de grupos na qual o usuário pertence.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Fulano 01",
                "email": "fulano01@gmail.com",
                "profile": {
                    "id": 1,
                    "address": "Rua ABC bairro Ipanema N 244, Sorocaba, SP. CEP: 7059483",
                    "phone": "61998283934"
                },
                "work_company": "11111111111111",
                "companies": ["22222222222222", "33333333333333"],
                "groups": [{
                    "id": 1,
                    "name": "Grupo 01",
                    "permissions": {
                        "id": 1,
                        "name": "Permissão 01"
                    }
                }],
                "permissions": [{
                    "id": 1,
                    "name": "Permissão 01"
                }]
            }
        }
