from typing import Optional
from pydantic import BaseModel, Field
from src.crud.users.dtos import RetrieveUserOutputDTO


class RetrieveCompanyOutputDTO(BaseModel):
    """
    Dados de saída para buscar uma empresa.
    """

    cnpj: str = Field(..., description="CNPJ da empresa.")
    name: str = Field(..., description="Nome da empresa.")
    owner_id: int = Field(..., description="Identificador do dono.")
    fantasy_name: Optional[str] = Field(None, description="Nome fantasia da empresa.")
    employees: list[RetrieveUserOutputDTO] = Field([], description="Funcionários da empresa.")

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
                "company": {
                    "owner_id": 316,
                    "cnpj": "11111111111111",
                    "name": "Empresa X LTDA",
                    "fantasy_name": "Empresa X",
                    "employees": [
                        {
                            "id": 1,
                            "name": "Fulano 01",
                            "email": "fulano01@gmail.com",
                            "profile": {
                                "id": 1,
                                "address": "Rua ABC bairro Ipanema N 244, Sorocaba, SP. CEP: 7059483",
                                "phone": "61998283934"
                            },
                            "work_company": "11111111111111",
                            "companies": [],
                            "groups": [{
                                "id": 226,
                                "name": "Grupo 01",
                                "permissions": {
                                    "id": 1,
                                    "name": "Permissão 02"
                                }
                            }],
                            "permissions": [
                                {
                                    "id": 1,
                                    "name": "Permissão de Criação"
                                },
                                {
                                    "id": 2,
                                    "name": "Permissão de Atualização"
                                }
                            ]
                        }
                    ]
                }
            }
        }
