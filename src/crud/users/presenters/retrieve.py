from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.error import ErrorPresenter
from src.crud.permissions.models import Permission
from src.crud.permissions.presenters import ListPermissionPresenter
from src.crud.permissions.dtos import ListPermissionInputDTO
from src.crud.permissions.repositories import ListPermissionDAO
from src.crud.groups.models import Group
from src.crud.groups.dtos import ListGroupInputDTO
from src.crud.groups.presenters import ListGroupPresenter
from src.crud.groups.repositories import ListGroupDAO
from src.crud.companies.dtos import ListCompaniesInputDTO
from src.crud.companies.models import Company
from src.crud.companies.repositories import ListCompanyDAO
from ..dtos import RetrieveUserOutputDTO, RetrieveProfileOutputDTO
from ..models import User, Profile
from ..repositories import ProfileDAO


class RetrieveUserPresenter:
    """
    Formatação de saída da API que buscar um usuário.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, model: User) -> RetrieveUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        if not model:
            return await ErrorPresenter(session=self.session).present(
                message="Usuário não encontrado.",
            )

        permission_dao = ListPermissionDAO(session=self.session)
        permissions: list[Permission] = await permission_dao.list(dto=ListPermissionInputDTO(user_id=model.id))
        permission_presenter = ListPermissionPresenter(session=self.session)
        permission_result = await permission_presenter.present(permissions)

        group_dao = ListGroupDAO(session=self.session)
        groups: list[Group] = await group_dao.list(dto=ListGroupInputDTO(user_id=model.id))
        group_presenter = ListGroupPresenter(session=self.session)
        group_result = await group_presenter.present(groups)

        profile_dao = ProfileDAO(session=self.session)
        profile_model: Profile = await profile_dao.get_by_id(user_id=model.id)
        profile = RetrieveProfileOutputDTO(
            id=profile_model.id,
            phone=profile_model.phone,
            address=profile_model.address
        )

        company_dao = ListCompanyDAO(session=self.session)
        company_models: list[Company] = await company_dao.list(dto=ListCompaniesInputDTO(owner_id=model.id))

        return RetrieveUserOutputDTO(
            id=model.id,
            name=model.name,
            email=model.email,
            profile=profile,
            work_company=model.work_company_cnpj,
            companies=[company.cnpj for company in company_models],
            groups=group_result.groups,
            permissions=permission_result.permissions
        )
