from src.adapters import ControllerInterface
from src.adapters.dtos import CreateCompanyInputDTO, CreateCompanyOutputDTO
from src.adapters.presenters import CreateCompanyPresenter
from src.domains.user_cases import CreateUserCase
from src.infrastructure.databases.daos import CompanyDAO
from src.infrastructure.databases import DBConnectionHandler


class CreateCompanyController(ControllerInterface):
    """
    Controladora de criação de empresas
    """

    def __init__(self, input: CreateCompanyInputDTO):
        """
        Construtor.
        """

        self.input = input

    async def execute(self) -> CreateCompanyOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = CompanyDAO(session=session)
            output = CreateCompanyPresenter(session=session)
            use_case = CreateUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.input)
