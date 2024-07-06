from pydantic import BaseModel, Field


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

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "name": "Permissão para criar permissões",
                "code": "permission_create"
            },
        }


class CreatePermissionOutputDTO(BaseModel):
    """
    Dados de saída para criar uma permissão.
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
