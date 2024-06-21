from src.adapters.dtos import PDFReaderOutputDTO
from src.adapters import PresenterInterface
from src.domains.entities import Invoice
from typing import List


class PDFReaderPresenter(PresenterInterface):
    """
    Formatação de saída da API da leitura de PDF.
    """

    def present(self, path: str, invoices: List[Invoice]) -> PDFReaderOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        return PDFReaderOutputDTO(filename=path, invoices=invoices)
