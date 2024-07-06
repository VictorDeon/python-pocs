from typing import Optional
from pydantic import BaseModel, Field
from src.crud.permissions.dtos import RetrievePermissionOutputDTO


class RetrieveGroupOutputDTO(BaseModel):
    """
    Dados de saída para buscar um grupo.
    """

    id: int = Field(..., description="Identificador único do grupo.")
    name: str = Field(..., description="Nome do grupo.")
    permissions: Optional[list[RetrievePermissionOutputDTO]] = Field([], description="Lista de permissões do grupo de usuários.")

    def to_dict(self):
        """
        Transforma o objeto em dicionário.
        """

        return self.model_dump()
