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
