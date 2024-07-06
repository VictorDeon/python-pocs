from typing import Optional
from pydantic import BaseModel, Field
from .retrieve import RetrieveCompanyOutputDTO


class ListCompaniesInputDTO(BaseModel):
    """
    Dados de entrada para listar empresas.
    """

    owner_id: Optional[int] = Field(None, description="Filtra pelo identificador do dona da empresa.")
    name: Optional[str] = Field(None, description="Filtra pelo nome da empresa.")
    offset: int = Field(0, description="Pular os N primeiros itens da lista.")
    limit: int = Field(25, description="Quantidade limite de itens que irá aparecer na listagem.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class ListCompaniesOutputDTO(BaseModel):
    """
    Dados de saída para listar empresas.
    """

    total: int = Field(..., description="Total de empresas.")
    companies: list[RetrieveCompanyOutputDTO] = Field([], description="Lista de empresas filtradas.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "total": 1,
                "companies": [{
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
                }]
            },
        }
