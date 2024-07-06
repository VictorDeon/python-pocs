from typing import Optional
from pydantic import BaseModel, Field
from src.crud.permissions.dtos import RetrievePermissionOutputDTO


class UpdateGroupInputDTO(BaseModel):
    """
    Dados de entrada para atualizar um grupo de usuários.
    """

    name: Optional[str] = Field(None, description="Nome do grupo.")
    permissions: Optional[list[str]] = Field([], description="Lista de códigos de permissões do grupo de usuários.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "name": "Grupo 01 atualizado",
                "permissions": ["permission_create"]
            },
        }

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class UpdateGroupOutputDTO(BaseModel):
    """
    Dados de saída para atualizar um grupo.
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
                    "name": "Grupo 01 atualizado",
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
