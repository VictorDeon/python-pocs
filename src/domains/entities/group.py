from pydantic import BaseModel, Field
from .permission import Permission


class Group(BaseModel):
    """
    Modelo de referência de grupos de usuários.
    """

    id: int = Field(..., description="Identificador único do grupo.")
    name: str = Field(..., description="Nome do grupo.")
    permissions: list[Permission] = Field([], description="Lista de permissões do grupo de usuários.")

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
                "name": "Grupo 01",
                "permissions": Permission.Config.json_schema_extra['example']
            }
        }
