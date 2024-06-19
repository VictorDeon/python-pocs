from pydantic import BaseModel, Field


class Profile(BaseModel):
    """
    Modelo de referência de usuário.
    """

    id: int = Field(..., description="Identificador único do perfil do usuário.")
    phone: str = Field(..., description="Telefone do usuário.")
    address: str = Field(..., description="Endereço do usuário.")

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
                "phone": "61998283934",
                "address": "Rua ABC bairro Ipanema N 244, Sorocaba, SP. CEP: 7059483"
            }
        }
