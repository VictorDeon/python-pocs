from src.adapters import ControllerInterface
from src.adapters.dtos import ListCompaniesInputDTO, ListCompaniesOutputDTO
from src.adapters.presenters import ListCompanyPresenter
from src.domains.user_cases import ListUserCase
from src.infrastructure.databases.daos import CompanyDAO
from src.infrastructure.databases import DBConnectionHandler


class ListCompaniesController(ControllerInterface):
    """
    Controladora de listagem dos empresas
    """

    def __init__(self, input: ListCompaniesInputDTO):
        """
        Construtor.
        """

        self.input = input

    async def execute(self) -> ListCompaniesOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = CompanyDAO(session=session)
            output = ListCompanyPresenter(session=session)
            use_case = ListUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.input)
