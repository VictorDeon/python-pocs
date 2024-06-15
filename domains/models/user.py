from pydantic import BaseModel, Field


class User(BaseModel):
    """
    Modelo de referência de usuário.
    """

    id: int = Field(..., description="Identificador único do usuário.")
    name: str = Field(..., description="Nome completo do usuário.")
    email: str = Field(..., description="Email do usuário.")
