from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Group


class ListGroupInputDTO(BaseModel):
    """
    Dados de entrada para listar grupos.
    """

    name: Optional[str] = Field(None, description="Nome do grupo.")
    code: Optional[str] = Field(None, description="Código da permissão no grupo.")
    user_id: Optional[int] = Field(None, description="Filtrar todos os grupos de um usuário.")
    offset: int = Field(0, description="Pular os N primeiros itens da lista.")
    limit: int = Field(25, description="Quantidade limite de itens que irá aparecer na listagem.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class ListGroupOutputDTO(BaseModel):
    """
    Dados de saída para listar grupos.
    """

    total: int = Field(..., description="Total de grupos.")
    groups: list[Group] = Field([], description="Lista de grupos filtrados.")
