from pydantic import BaseModel, Field


class BlockedRequestsOutputDTO(BaseModel):
    """
    Dados de saída para requisições de bloqueio
    """

    result: str = Field(..., description="Resultado dos testes de desempenho.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "result": "Requisição executada em 5 segundos"
            },
        }
