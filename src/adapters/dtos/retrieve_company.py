from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Company


class RetrieveCompanyOutputDTO(BaseModel):
    """
    Dados de saída para buscar uma empresa.
    """

    company: Optional[Company] = Field(None, description="Dados da empresa.")
