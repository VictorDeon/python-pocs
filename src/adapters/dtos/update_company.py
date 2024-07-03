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

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "cnpj": "11111111111111",
                "name": "Empresa Y LTDA",
                "fantasy_name": "Empresa Y"
            },
        }

    def to_dict(self, exclude: list[str] = []):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump(exclude=exclude)


class UpdateCompanyOutputDTO(BaseModel):
    """
    Dados de saída para atualizar uma empresa.
    """

    company: Company = Field(..., description="Dados da empresa atualizados.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "owner_id": 316,
                "cnpj": "11111111111111",
                "name": "Empresa Y LTDA",
                "fantasy_name": "Empresa Y",
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
            },
        }
