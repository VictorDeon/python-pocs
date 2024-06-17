from pydantic import BaseModel, Field
from src.domains.entities import Invoice


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
