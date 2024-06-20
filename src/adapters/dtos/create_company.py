from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Company


class CreateCompanyInputDTO(BaseModel):
    """
    Dados de entrada para criar uma empresa.
    """

    user_id: int = Field(..., description="Identificador do usuário dono da oficina.")
    cnpj: str = Field(..., description="CNPJ da empresa.")
    name: str = Field(..., description="Nome da empresa.")
    fantasy_name: Optional[str] = Field(None, description="Nome fantasia da empresa.")
    employees: list[int] = Field([], description="Lista de identificadores dos funcionários da empresa.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class CreateCompanyOutputDTO(BaseModel):
    """
    Dados de saída para criar uma empresa.
    """

    company: Company = Field(..., description="Dados da empresa criada.")
