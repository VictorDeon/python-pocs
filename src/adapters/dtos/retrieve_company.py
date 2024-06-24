from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Company


class RetrieveCompanyInputDTO(BaseModel):
    """
    Dados de entrada para buscar uma empresa.
    """

    cnpj: Optional[str] = Field(None, description="CNPJ da empresa.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class RetrieveCompanyOutputDTO(BaseModel):
    """
    Dados de saída para buscar uma empresa.
    """

    company: Optional[Company] = Field(None, description="Dados da empresa.")
