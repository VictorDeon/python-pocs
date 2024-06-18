from pydantic import BaseModel, Field
from src.domains.entities import User


class BlockedRequestsOutputDTO(BaseModel):
    """
    Dados de saída para requisições de bloqueio
    """

    result: str = Field(..., description="Resultado dos testes de desempenho.")
