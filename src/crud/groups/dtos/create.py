from typing import Optional
from pydantic import BaseModel, Field
from src.crud.permissions.dtos import RetrievePermissionOutputDTO


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

    id: int = Field(..., description="Identificador único do grupo.")
    name: str = Field(..., description="Nome do grupo.")
    permissions: Optional[list[RetrievePermissionOutputDTO]] = Field([], description="Lista de permissões do grupo de usuários.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "group": {
                    "id": 224,
                    "name": "Grupo 01",
                    "permissions": [
                        {
                            "id": 371,
                            "name": "Permissão para criar permissões",
                            "code": "permission_create"
                        },
                        {
                            "id": 373,
                            "name": "Permissão para deletar permissões",
                            "code": "permission_delete"
                        }
                    ]
                }
            }
        }
