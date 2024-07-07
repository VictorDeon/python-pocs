from pydantic import BaseModel, Field


class PocRequestsOutputDTO(BaseModel):
    """
    Dados de saída para pocs de requisições
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
