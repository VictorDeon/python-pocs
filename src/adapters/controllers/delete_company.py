from src.adapters import ControllerInterface
from src.domains.user_cases import DeleteUserCase
from src.infrastructure.databases.daos import CompanyDAO
from src.infrastructure.databases import DBConnectionHandler


class DeleteCompanyController(ControllerInterface):
    """
    Controladora de deleção de empresas
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
            use_case = DeleteUserCase(repository=repository)
            return await use_case.execute(self.cnpj)
