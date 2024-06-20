from pydantic import BaseModel, Field
from src.domains.entities import Permission


class CreatePermissionInputDTO(BaseModel):
    """
    Dados de entrada para criar uma permissão do usuário.
    """

    name: str = Field(..., description="Nome da permissão.")
    code: str = Field(..., description="Código da permissão.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class CreatePermissionOutputDTO(BaseModel):
    """
    Dados de saída para criar uma empresa.
    """

    permission: Permission = Field(..., description="Dados da permissão criada.")
