from src.adapters.dtos import ListUserInputDTO, RetrieveCompanyOutputDTO
from src.adapters import PresenterInterface
from src.domains.entities import Company
from src.infrastructure.databases.models import (
    User as UserModel,
    Company as CompanyModel
)
from src.infrastructure.databases.daos import UserDAO
from .list_user import ListUserPresenter


class RetrieveCompanyPresenter(PresenterInterface):
    """
    Formatação de saída da API que buscar um grupo.
    """

    async def present(self, model: CompanyModel) -> RetrieveCompanyOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        user_dao = UserDAO(session=self.session)

        employees: list[UserModel] = await user_dao.list(dto=ListUserInputDTO(work_company_cnpj=model.cnpj))
        list_user_presentes = ListUserPresenter(session=self.session)

        company = Company(
            cnpj=model.cnpj,
            name=model.name,
            fantasy_name=model.fantasy_name,
            employees=list_user_presentes.present(employees)
        )

        return RetrieveCompanyOutputDTO(company=company)
