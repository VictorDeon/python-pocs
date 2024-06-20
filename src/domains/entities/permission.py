from pydantic import BaseModel, Field


class Permission(BaseModel):
    """
    Modelo de referência de permissões.
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
                "id": 1,
                "name": "Permissão 01"
            }
        }
