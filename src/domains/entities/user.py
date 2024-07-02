from pydantic import BaseModel, Field
from typing import Optional
from .profile import Profile
from .permission import Permission
from .group import Group


class User(BaseModel):
    """
    Modelo de referência de usuário.
    """

    id: int = Field(..., description="Identificador único do usuário.")
    name: str = Field(..., description="Nome completo do usuário.")
    email: str = Field(..., description="Email do usuário.")
    profile: Profile = Field(..., description="Perfil do usuário com dados adicionais.")
    companies: list[str] = Field([], description="CNPJ das empresas na qual o usuário é dono.")
    work_company: Optional[str] = Field(None, description="CNPJ da empresa na qual o usuário trabalha.")
    permissions: list[Permission] = Field([], description="Lista de permissões do usuário.")
    groups: list[Group] = Field([], description="Lista de grupos na qual o usuário pertence.")

    def to_dict(self):
        """
        Transforma o objeto em dicionário.
        """

        return self.model_dump()

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Fulano 01",
                "email": "fulano01@gmail.com",
                "profile": Profile.Config.json_schema_extra['example'],
                "permissions": Permission.Config.json_schema_extra['example'],
                "groups": Group.Config.json_schema_extra['example']
            }
        }
