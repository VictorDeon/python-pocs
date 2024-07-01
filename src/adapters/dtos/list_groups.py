from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Group


class ListGroupInputDTO(BaseModel):
    """
    Dados de entrada para listar grupos.
    """

    name: Optional[str] = Field(None, description="Nome do grupo.")
    code: Optional[str] = Field(None, description="Código da permissão no grupo.")
    user_id: Optional[str] = Field(None, description="Filtrar todos os grupos de um usuário.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class ListGroupOutputDTO(BaseModel):
    """
    Dados de saída para listar grupos.
    """

    groups: list[Group] = Field([], description="Lista de grupos filtrados.")
