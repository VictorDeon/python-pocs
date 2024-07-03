from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Group


class CreateGroupInputDTO(BaseModel):
    """
    Dados de entrada para criar um grupo de usuários.
    """

    name: str = Field(..., description="Nome do grupo.")
    permissions: Optional[list[str]] = Field([], description="Lista de códigos de permissões do grupo de usuários.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "name": "Grupo 01",
                "permissions": ["permission_create", "permission_delete"]
            },
        }

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class CreateGroupOutputDTO(BaseModel):
    """
    Dados de saída para criar um grupo de usuários.
    """

    group: Group = Field(..., description="Dados do grupo criado.")
