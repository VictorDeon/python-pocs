from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Permission


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

    permission: Optional[Permission] = Field(None, description="Dados da permissão.")
