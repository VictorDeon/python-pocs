from ..dtos import PDFGeneratorOutputDTO


class PDFGeneratorPresenter:
    """
    Formatação de saída da API da geração de PDF.
    """

    async def present(self, path: str) -> PDFGeneratorOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        return PDFGeneratorOutputDTO(filename=path)
