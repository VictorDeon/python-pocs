from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Company


class ListCompaniesInputDTO(BaseModel):
    """
    Dados de entrada para listar empresas.
    """

    owner_id: Optional[int] = Field(None, description="Filtra pelo identificador do dona da empresa.")
    name: Optional[str] = Field(None, description="Filtra pelo nome da empresa.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class ListCompaniesOutputDTO(BaseModel):
    """
    Dados de saída para listar empresas.
    """

    companies: list[Company] = Field([], description="Lista de empresas filtradas.")
