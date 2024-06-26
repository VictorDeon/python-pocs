from src.adapters import ControllerInterface
from src.adapters.dtos import PDFGeneratorInputDTO
from src.adapters.presenters import PDFGeneratorPresenter
from src.domains.user_cases import PDFGenerator
from src.infrastructure.storage.repositories import LocalStorageSingleton


class PDFGeneratorController(ControllerInterface):
    """
    Controladora de acesso externo para buscar os dados de uma API.
    """

    def __init__(self, invoice: PDFGeneratorInputDTO) -> None:
        """
        Construtor
        """

        self.input_dto = invoice

    async def execute(self) -> dict:
        """
        Lida com a entrada e saida dos dados.
        """

        repository = await LocalStorageSingleton.get_instance()
        output = PDFGeneratorPresenter()
        use_case = PDFGenerator(output, repository)
        return await use_case.execute(self.input_dto)
