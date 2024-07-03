from src.adapters.dtos import ListUserInputDTO, RetrieveCompanyOutputDTO
from src.adapters import PresenterInterface
from src.domains.entities import Company
from src.infrastructure.databases.models import (
    User as UserModel,
    Company as CompanyModel
)
from src.infrastructure.databases.daos import UserDAO
from .list_user import ListUserPresenter
from .error import ErrorPresenter


class RetrieveCompanyPresenter(PresenterInterface):
    """
    Formatação de saída da API que buscar um grupo.
    """

    async def present(self, model: CompanyModel) -> RetrieveCompanyOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        if not model:
            return await ErrorPresenter(session=self.session).present(
                message="Empresa não encontrada.",
            )

        user_dao = UserDAO(session=self.session)
        employees: list[UserModel] = await user_dao.list(dto=ListUserInputDTO(work_company_cnpj=model.cnpj))
        list_user_presentes = ListUserPresenter(session=self.session)
        presenter = await list_user_presentes.present(employees)

        company = Company(
            cnpj=model.cnpj,
            name=model.name,
            owner_id=model.owner_id,
            fantasy_name=model.fantasy_name,
            employees=presenter.users
        )

        return RetrieveCompanyOutputDTO(company=company)
