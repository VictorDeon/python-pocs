from pydantic import BaseModel, Field


class User(BaseModel):
    """
    Modelo de referência de usuário.
    """

    id: int = Field(..., description="Identificador único do usuário.")
    name: str = Field(..., description="Nome completo do usuário.")
    email: str = Field(..., description="Email do usuário.")

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
                "name": "Fulano 01",
                "email": "fulano@gmail.com"
            }
        }
