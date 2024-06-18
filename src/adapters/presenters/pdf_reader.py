from src.adapters.dtos import PDFReaderOutputDTO
from src.adapters.interfaces import PresenterInterface


class PDFReaderPresenter(PresenterInterface):
    """
    Formatação de saída da API da leitura de PDF.
    """

    def present(self, output_dto: PDFReaderOutputDTO) -> dict:
        """
        Forma final de apresentação dos dados.
        """

        return {
            "filename": output_dto.filename,
            "invoices": [invoice.to_dict() for invoice in output_dto.invoices]
        }
