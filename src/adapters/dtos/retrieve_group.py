from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Group


class RetrieveGroupOutputDTO(BaseModel):
    """
    Dados de saída para buscar um grupo.
    """

    group: Optional[Group] = Field(None, description="Dados do grupo.")
