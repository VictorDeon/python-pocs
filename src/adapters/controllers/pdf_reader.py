from src.adapters import ControllerInterface
from src.adapters.dtos import PDFReaderInputDTO
from src.adapters.presenters import PDFReaderPresenter
from src.domains.user_cases import PDFReader
from src.infrastructure.storage.repositories import LocalStorageSingleton


class PDFReaderController(ControllerInterface):
    """
    Controladora de acesso externo para buscar os dados de uma API.
    """

    def __init__(self, trace_id: str, year: int, month: int) -> None:
        """
        Construtor
        """

        self.input_dto = PDFReaderInputDTO(trace_id=trace_id, year=year, month=month)

    async def execute(self) -> dict:
        """
        Lida com a entrada e saida dos dados.
        """

        repository = await LocalStorageSingleton.get_instance()
        output = PDFReaderPresenter()
        use_case = PDFReader(output, repository)
        return await use_case.execute(self.input_dto)
