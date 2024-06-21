from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Permission


class UpdatePermissionInputDTO(BaseModel):
    """
    Dados de entrada para atualizar uma permissão do usuário.
    """

    name: Optional[str] = Field(None, description="Nome da permissão.")
    code: Optional[str] = Field(None, description="Código da permissão.")

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
