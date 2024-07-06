from typing import Optional
from pydantic import BaseModel, Field


class RetrievePermissionInputDTO(BaseModel):
    """
    Dados de entrada para buscar uma permissão.
    """

    code: Optional[str] = Field(None, description="Código da permissão.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class RetrievePermissionOutputDTO(BaseModel):
    """
    Dados de saída para buscar uma permissão.
    """

    id: int = Field(..., description="Identificador único da permissão.")
    name: str = Field(..., description="Nome do permissão.")
    code: str = Field(..., description="Código da permissão.")

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
                "permission": {
                    "id": 371,
                    "name": "Permissão para criar permissões",
                    "code": "permission_create"
                }
            }
        }
