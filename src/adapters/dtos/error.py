from pydantic import BaseModel, Field


class ErrorOutputDTO(BaseModel):
    """
    Dados de saída para erros
    """

    status_code: int = Field(..., description="Status code da exceção.")
    msg: str = Field(..., description="Mensagem de error")
