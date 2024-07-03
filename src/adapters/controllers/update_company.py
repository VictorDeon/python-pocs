from src.adapters import ControllerInterface
from src.adapters.dtos import UpdateCompanyInputDTO, UpdateCompanyOutputDTO
from src.adapters.presenters import UpdateCompanyPresenter
from src.domains.user_cases import UpdateUserCase
from src.infrastructure.databases.daos import CompanyDAO
from src.infrastructure.databases import DBConnectionHandler


class UpdateCompanyController(ControllerInterface):
    """
    Controladora de atualização de empresas
    """

    def __init__(self, cnpj: str, input: UpdateCompanyInputDTO):
        """
        Construtor.
        """

        self.input = input
        self.cnpj = cnpj

    async def execute(self) -> UpdateCompanyOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = CompanyDAO(session=session)
            output = UpdateCompanyPresenter(session=session)
            use_case = UpdateUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.cnpj, self.input)
