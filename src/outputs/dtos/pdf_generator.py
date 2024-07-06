from pydantic import BaseModel, Field
from .invoice import Invoice


class PDFGeneratorInputDTO(Invoice):
    """
    Dados de entrada para gerar um PDF de invoice.
    """

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class PDFGeneratorOutputDTO(BaseModel):
    """
    Dados de saída para gerar uma invoice.
    """

    filename: str = Field(..., description="Nome do arquivo no bucket.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "filename": "assets/docs/2024-05-invoice-abcd1234.pdf"
            }
        }
