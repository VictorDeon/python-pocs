from pydantic import BaseModel, Field
from typing import List


class Product(BaseModel):
    """
    Produtos.
    """

    description: str = Field(..., description="Descrição do produto.")
    price: float = Field(..., description="Preço unitário do produto.")
    quantity: int = Field(..., description="Quantidade do produto.")


class Invoice(BaseModel):
    """
    Dados de entrada.
    """

    from_address: str = Field(..., description="Endereço de destino.")
    to_address: str = Field(..., description="Endereço de origem.")
    invoice_number: str = Field(..., description="Número da invoice.")
    products: List[Product] = Field([], description="Lista de produtos da invoice.")
    due_date: str = Field(..., description="Data de vencimento da invoice.")
    account: str = Field(..., description="Conta bancária")

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
                "from_address": "WeasyPrint 26 rue Emile Decorps 69100 Villeurbanne France",
                "to_address": "Our awesome developers From all around the world Earth",
                "invoice_number": "12345",
                "due_date": "2028-05-10",
                "account": "132 456 789 012",
                "products": [
                    {
                        "description": "Website design",
                        "price": 34.20,
                        "quantity": 100
                    },
                    {
                        "description": "Website development",
                        "price": 45.50,
                        "quantity": 100
                    },
                    {
                        "description": "Website integration",
                        "price": 25.75,
                        "quantity": 100
                    }
                ]
            }
        }


class ReaderInvoices(BaseModel):
    """
    Invoice de leitura.
    """

    path: str = Field(..., description="Path de pesquisa de invoices.")
    invoices: list[Invoice] = Field([], description="Dados das invoices.")
