from src.adapters.dtos import PDFGeneratorOutputDTO
from src.adapters.interfaces import PresenterInterface


class PDFGeneratorPresenter(PresenterInterface):
    """
    Formatação de saída da API da geração de PDF.
    """

    def present(self, path: str) -> PDFGeneratorOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        return PDFGeneratorOutputDTO(filename=path)
