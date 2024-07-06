from typing import Optional
from pydantic import BaseModel, Field
from .retrieve import RetrievePermissionOutputDTO


class ListPermissionInputDTO(BaseModel):
    """
    Dados de entrada para listar permissões.
    """

    name: Optional[str] = Field(None, description="Nome da permissão.")
    code: Optional[str] = Field(None, description="Código da permissão.")
    group_id: Optional[int] = Field(None, description="Buscar todas as permissões de um grupo.")
    user_id: Optional[int] = Field(None, description="Buscar todas as permissões de um usuário.")
    offset: int = Field(0, description="Pular os N primeiros itens da lista.")
    limit: int = Field(25, description="Quantidade limite de itens que irá aparecer na listagem.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class ListPermissionOutputDTO(BaseModel):
    """
    Dados de saída para listar permissões.
    """

    total: int = Field(..., description="Total de permissões.")
    permissions: list[RetrievePermissionOutputDTO] = Field([], description="Lista de permissões filtradas.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "total": 1,
                "permissions": [{
                    "id": 371,
                    "name": "Permissão para criar permissões",
                    "code": "permission_create"
                }]
            }
        }
