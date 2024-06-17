from pydantic import BaseModel, Field
from src.domains.entities import User


class FindUserInputDTO(BaseModel):
    """
    Dados de entrada para encontrar um usuário
    """

    id: int = Field(..., description="Identificador único do usuário.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class FindUserOutputDTO(BaseModel):
    """
    Dados de saída para encontrar um usuário
    """

    user: User = Field(..., description="Dados do usuário.")
