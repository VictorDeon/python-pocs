from typing import Optional
from pydantic import BaseModel, Field
from .retrieve import RetrieveUserOutputDTO


class UpdateProfileInputDTO(BaseModel):
    """
    Dados de entrada para atualizar um perfil.
    """

    phone: Optional[str] = Field(None, description="Telefone do usuário.")
    address: Optional[str] = Field(None, description="Endereço do usuário.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


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

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "name": "Fulano 01 atualizado",
                "email": "fulano01@gmail.com",
                "profile": {
                    "address": "Rua XYZ kkkk N 244, Sorocaba, SP. CEP: 7059483",
                    "phone": "61998283934"
                },
                "work_company_cnpj": "11111111111111",
                "groups": [226],
                "permissions": ["permission_create"],
            }
        }

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class UpdateUserOutputDTO(RetrieveUserOutputDTO):
    """
    Dados de saída para atualizar um usuário.
    """

    pass
