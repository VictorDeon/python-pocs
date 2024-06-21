from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Permission


class ListPermissionInputDTO(BaseModel):
    """
    Dados de entrada para listar permissões.
    """

    name: Optional[str] = Field(None, description="Nome da permissão.")
    code: Optional[str] = Field(None, description="Código da permissão.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class ListPermissionOutputDTO(BaseModel):
    """
    Dados de saída para listar permissões.
    """

    permissions: list[Permission] = Field([], description="Lista de permissões filtradas.")
