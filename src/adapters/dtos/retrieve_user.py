from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import User


class RetrieveUserInputDTO(BaseModel):
    """
    Dados de entrada para buscar um usuário.
    """

    email: str = Field(..., description="Email do usuário.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class RetrieveUserOutputDTO(BaseModel):
    """
    Dados de saída para buscar um usuário.
    """

    user: Optional[User] = Field(None, description="Dados do usuário.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "user": {
                    "id": 1,
                    "name": "Fulano 01",
                    "email": "fulano01@gmail.com",
                    "profile": {
                        "id": 1,
                        "address": "Rua ABC bairro Ipanema N 244, Sorocaba, SP. CEP: 7059483",
                        "phone": "61998283934"
                    },
                    "work_company": "11111111111111",
                    "companies": ["22222222222222", "33333333333333"],
                    "groups": [{
                        "id": 1,
                        "name": "Grupo 01",
                        "permissions": {
                            "id": 1,
                            "name": "Permissão 01"
                        }
                    }],
                    "permissions": [{
                        "id": 1,
                        "name": "Permissão 01"
                    }]
                }
            }
        }
