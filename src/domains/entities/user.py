from pydantic import BaseModel, Field
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
