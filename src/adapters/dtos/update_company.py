from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Company


class UpdateCompanyInputDTO(BaseModel):
    """
    Dados de entrada para atualizar uma empresa.
    """

    cnpj: Optional[str] = Field(None, description="CNPJ da empresa.")
    name: Optional[str] = Field(None, description="Nome da empresa.")
    fantasy_name: Optional[str] = Field(None, description="Nome fantasia da empresa.")
    employees: list[int] = Field([], description="Lista de identificadores dos funcionários da empresa.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class UpdateCompanyOutputDTO(BaseModel):
    """
    Dados de saída para atualizar uma empresa.
    """

    company: Company = Field(..., description="Dados da empresa atualizados.")
