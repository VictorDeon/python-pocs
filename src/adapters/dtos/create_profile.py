from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Profile


class CreateProfileInputDTO(BaseModel):
    """
    Dados de entrada para criar um perfil.
    """

    phone: Optional[str] = Field(None, description="Telefone do usuário.")
    address: Optional[str] = Field(None, description="Endereço do usuário.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class CreateProfileOutputDTO(BaseModel):
    """
    Dados de saída para criar um perfil.
    """

    profile: Profile = Field(..., description="Dados do perfil do usuário.")
