from pydantic import BaseModel, Field


class ErrorOutputDTO(BaseModel):
    """
    Dados de saída para erros
    """

    message: str = Field(..., description="Mensagem de error")
