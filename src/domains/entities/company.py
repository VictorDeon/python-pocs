from typing import Optional
from pydantic import BaseModel, Field
from .user import User


class Company(BaseModel):
    """
    Modelo de referência de empresas.
    """

    cnpj: str = Field(..., description="CNPJ da empresa.")
    name: str = Field(..., description="Nome da empresa.")
    fantasy_name: Optional[str] = Field(None, description="Nome fantasia da empresa.")
    employees: list[User] = Field([], description="Funcionários da empresa.")

    def to_dict(self):
        """
        Transforma o objeto em dicionário.
        """

        return self.model_dump()

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "cnpj": "19283049584322",
                "name": "Empresa 01 LTDA",
                "fantasy_name": "Empresa 01",
                "employees": [
                    {
                        "id": 2,
                        "name": "Fulano 02",
                        "email": "fulano02@gmail.com",
                    }
                ]
            }
        }
