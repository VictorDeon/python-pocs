from src.adapters.dtos import PDFReaderOutputDTO
from src.adapters import PresenterInterface
from src.domains.entities import ReaderInvoices
from typing import List


class PDFReaderPresenter(PresenterInterface):
    """
    Formatação de saída da API da leitura de PDF.
    """

    def present(self, model: ReaderInvoices) -> PDFReaderOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        return PDFReaderOutputDTO(filename=model.path, invoices=model.invoices)
