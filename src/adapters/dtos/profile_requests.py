from pydantic import BaseModel, Field


class ProfileRequestsOutputDTO(BaseModel):
    """
    Dados de saída para requisições de perfil
    """

    min: float = Field(..., description="Tempo mínimo de execução.")
    max: float = Field(..., description="Tempo máximo de execução.")
    mean: float = Field(..., description="Média das execuções.")
    total: float = Field(..., description="Total de tempo que levou todas as execuções.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "min": 0.0033,
                "max": 0.2324,
                "mean": 0.0233
            },
        }
