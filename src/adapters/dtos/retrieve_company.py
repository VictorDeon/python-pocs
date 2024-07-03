from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Company


class RetrieveCompanyOutputDTO(BaseModel):
    """
    Dados de saída para buscar uma empresa.
    """

    company: Optional[Company] = Field(None, description="Dados da empresa.")

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
