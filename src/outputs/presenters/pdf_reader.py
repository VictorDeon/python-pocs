from ..dtos import PDFReaderOutputDTO, ReaderInvoices


class PDFReaderPresenter:
    """
    Formatação de saída da API da leitura de PDF.
    """

    async def present(self, model: ReaderInvoices) -> PDFReaderOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        return PDFReaderOutputDTO(filename=model.path, invoices=model.invoices)
