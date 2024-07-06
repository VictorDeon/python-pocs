from src.engines.storage import LocalStorageSingleton
from ..dtos import PDFReaderInputDTO, ReaderInvoices
from ..presenters import PDFReaderPresenter


class PDFReaderRepository:
    """
    Controladora de acesso externo para buscar os dados de uma API.
    """

    def __init__(self, trace_id: str, year: int, month: int) -> None:
        """
        Construtor
        """

        self.input_dto = PDFReaderInputDTO(trace_id=trace_id, year=year, month=month)

    def handler_path(self, input_dto: PDFReaderInputDTO) -> str:
        """
        Cria o caminho de filtro do bucket.
        """

        if input_dto.trace_id and input_dto.year and input_dto.month:
            path = "assets/docs/%d_%02d-invoice-%s.pdf" % (input_dto.year, input_dto.month, input_dto.trace_id)
        elif input_dto.trace_id and input_dto.year:
            path = "assets/docs/%d_*-invoice-%s.pdf" % (input_dto.year, input_dto.trace_id)
        elif input_dto.trace_id and input_dto.month:
            path = "assets/docs/*_%02d-invoice-%s.pdf" % (input_dto.month, input_dto.trace_id)
        elif input_dto.year and input_dto.month:
            path = "assets/docs/%d_%02d-*.pdf" % (input_dto.year, input_dto.month)
        elif input_dto.trace_id:
            path = "assets/docs/*-invoice-%s.pdf" % input_dto.trace_id
        elif input_dto.year:
            path = "assets/docs/%d_*.pdf" % input_dto.year
        elif input_dto.month:
            path = "assets/docs/*_%02d-*.pdf" % input_dto.month
        else:
            path = "assets/docs/*.pdf"

        return path

    async def execute(self) -> dict:
        """
        Le um pdf e retorna a lista de dados.
        TODO: Fazer a lógica para extrair os dados do PDF
        TODO: Fazer a lógica para consultar os arquivos locais.
        """

        path = self.handler_path(self.input_dto)

        # Fazer a consulta dos arquivos locais
        repository = await LocalStorageSingleton.get_instance()
        blobs = list(await repository.list_blobs(path=path))
        response = []
        for blob in blobs:
            blob_path_splited = blob.name.split("/")
            filename = blob_path_splited[-1]
            data = {"filename": filename}
            # Extrair dados do pdf e inserir no response
            response.append(data)

        return await PDFReaderPresenter().present(model=ReaderInvoices(path=path, invoices=response))
