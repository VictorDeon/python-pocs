from engines.storage.interfaces import StorageSingletonInterface
from domains.interfaces import PDFReaderInterface
from domains.models import InvoiceFileResponse


class PDFReader(PDFReaderInterface):
    """
    Caso de uso de procura de um usuários.
    """

    def __init__(self, storage_repository: StorageSingletonInterface) -> None:
        """
        Construtor.
        """

        self.storage_repository = storage_repository

    def handler_path(self, trace_id: str = None, year: int = None, month: int = None) -> str:
        """
        Cria o caminho de filtro do bucket.
        """

        if trace_id and year and month:
            path = "pdfs/invoices/%d_%02d-invoice-%s.pdf" % (year, month, trace_id)
        elif trace_id and year:
            path = "pdfs/invoices/%d_*-invoice-%s.pdf" % (year, trace_id)
        elif trace_id and month:
            path = "pdfs/invoices/*_%02d-invoice-%s.pdf" % (month, trace_id)
        elif year and month:
            path = "pdfs/invoices/%d_%02d-*.pdf" % (year, month)
        elif trace_id:
            path = "pdfs/invoices/*-invoice-%s.pdf" % trace_id
        elif year:
            path = "pdfs/invoices/%d_*.pdf" % year
        elif month:
            path = "pdfs/invoices/*_%02d-*.pdf" % month
        else:
            path = "pdfs/invoices/*.pdf"

        return path

    async def list_invoices(self, trace_id: str, year: int, month: int) -> InvoiceFileResponse:
        """
        Le um pdf e retorna a lista de dados.
        TODO: Fazer a lógica para extrair os dados do PDF
        """

        path = self.handler_path(trace_id, year, month)
        blobs = list(await self.storage_repository.list_blobs(path=path))
        response = []
        for blob in blobs:
            blob_path_splited = blob.name.split("/")
            filename = blob_path_splited[-1]
            data = {"filename": filename}
            # Extrair dados do pdf e inserir no response
            response.append(data)

        return response
