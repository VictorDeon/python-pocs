from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.users.models import User
from src.crud.users.repositories import ListUserRepository
from src.crud.users.presenters import ListUserPresenter
from src.crud.users.dtos import ListUserInputDTO
from src.shared.error import ErrorPresenter
from ..dtos import RetrieveCompanyOutputDTO
from ..models import Company


class RetrieveCompanyPresenter:
    """
    Formatação de saída da API que buscar um grupo.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, model: Company) -> RetrieveCompanyOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        if not model:
            return await ErrorPresenter(session=self.session).present(
                message="Empresa não encontrada.",
            )

        user_dao = ListUserRepository(session=self.session)
        employees: list[User] = await user_dao.list(dto=ListUserInputDTO(work_company_cnpj=model.cnpj))
        list_user_presentes = ListUserPresenter(session=self.session)
        users = await list_user_presentes.present(employees)

        return RetrieveCompanyOutputDTO(
            cnpj=model.cnpj,
            name=model.name,
            owner_id=model.owner_id,
            fantasy_name=model.fantasy_name,
            employees=users
        )
