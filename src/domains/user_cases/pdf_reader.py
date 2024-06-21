from src.adapters import PresenterInterface
from src.adapters.dtos import PDFReaderInputDTO
from src.domains import UserCaseInterface
from src.infrastructure.storage import StorageSingletonInterface


class PDFReader(UserCaseInterface):
    """
    Caso de uso de procura de um usuários.
    """

    def __init__(self, presenter: PresenterInterface, repository: StorageSingletonInterface):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

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

    async def execute(self, input_dto: PDFReaderInputDTO) -> list[dict]:
        """
        Le um pdf e retorna a lista de dados.
        TODO: Fazer a lógica para extrair os dados do PDF
        TODO: Fazer a lógica para consultar os arquivos locais.
        """

        path = self.handler_path(input_dto)
        # Fazer a consulta dos arquivos locais
        blobs = list(await self.repository.list_blobs(path=path))
        response = []
        for blob in blobs:
            blob_path_splited = blob.name.split("/")
            filename = blob_path_splited[-1]
            data = {"filename": filename}
            # Extrair dados do pdf e inserir no response
            response.append(data)

        return self.presenter.present(path=path, invoices=response)
