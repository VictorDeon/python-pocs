from typing import Optional
from pydantic import BaseModel, Field
from src.domains.entities import Invoice as EntityInvoice


class PDFReaderInputDTO(BaseModel):
    """
    Dados de entrada para ler um PDF de invoice.
    """

    trace_id: Optional[str] = Field(None, description="Identificador único da invoice")
    year: Optional[int] = Field(None, description="Ano na qual a invoice foi criada.")
    month: Optional[int] = Field(None, description="Mês na qual a invoice foi criada.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class Invoice(EntityInvoice):
    """
    More data to output.
    """

    total: float = Field(..., description="Valor total da invoice.")


class PDFReaderOutputDTO(BaseModel):
    """
    Dados de saída para ler uma invoice.
    """

    filename: str = Field(..., description="Nome do arquivo no bucket.")
    invoices: list[Invoice] = Field([], description="Lista de dados das invoices.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "filename": "assets/docs/2024-05-invoice-abcd1234.pdf",
                "invoices": [Invoice.Config.json_schema_extra['example']]
            }
        }
