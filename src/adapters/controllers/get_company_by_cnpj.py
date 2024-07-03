from src.adapters import ControllerInterface
from src.domains.user_cases import GetByDocumentUserCase
from src.infrastructure.databases.daos import CompanyDAO
from src.infrastructure.databases import DBConnectionHandler
from src.adapters.presenters import RetrieveCompanyPresenter


class GetCompanyByCNPJController(ControllerInterface):
    """
    Controladora de busca de empresas pelo cnpj
    """

    def __init__(self, cnpj: str):
        """
        Construtor.
        """

        self.cnpj = cnpj

    async def execute(self) -> int:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = CompanyDAO(session=session)
            presenter = RetrieveCompanyPresenter(session=session)
            use_case = GetByDocumentUserCase(
                presenter=presenter,
                repository=repository
            )
            return await use_case.execute(self.cnpj)
