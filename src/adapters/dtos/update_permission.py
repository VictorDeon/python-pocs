from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Permission


class UpdatePermissionInputDTO(BaseModel):
    """
    Dados de entrada para atualizar uma permissão do usuário.
    """

    name: Optional[str] = Field(None, description="Nome da permissão.")
    code: Optional[str] = Field(None, description="Código da permissão.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "name": "Permissão para criar permissões atualizado",
                "code": "permission_create"
            },
        }

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class UpdatePermissionOutputDTO(BaseModel):
    """
    Dados de saída para atualizar uma permissão.
    """

    permission: Permission = Field(..., description="Dados da permissão atualizados.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "permission": {
                    "id": 371,
                    "name": "Permissão para criar permissões atualizado",
                    "code": "permission_create"
                }
            }
        }
