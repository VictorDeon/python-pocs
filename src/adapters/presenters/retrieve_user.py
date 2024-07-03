from src.adapters.dtos import ListPermissionInputDTO, RetrieveUserOutputDTO, ListGroupInputDTO, ListCompaniesInputDTO
from src.adapters import PresenterInterface
from src.domains.entities import User, Profile
from src.infrastructure.databases.models import (
    Group as GroupModel,
    Permission as PermissionModel,
    User as UserModel,
    Profile as ProfileModel,
    Company as CompanyModel
)
from src.infrastructure.databases.daos import PermissionDAO, GroupDAO, ProfileDAO, CompanyDAO
from .list_permissions import ListPermissionPresenter
from .list_groups import ListGroupPresenter
from .error import ErrorPresenter


class RetrieveUserPresenter(PresenterInterface):
    """
    Formatação de saída da API que buscar um usuário.
    """

    async def present(self, model: UserModel) -> RetrieveUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        if not model:
            return await ErrorPresenter(session=self.session).present(
                message="Usuário não encontrado.",
            )

        permission_dao = PermissionDAO(session=self.session)
        permissions: list[PermissionModel] = await permission_dao.list(dto=ListPermissionInputDTO(user_id=model.id))
        permission_presenter = ListPermissionPresenter(session=self.session)
        permission_result = await permission_presenter.present(permissions)

        group_dao = GroupDAO(session=self.session)
        groups: list[GroupModel] = await group_dao.list(dto=ListGroupInputDTO(user_id=model.id))
        group_presenter = ListGroupPresenter(session=self.session)
        group_result = await group_presenter.present(groups)

        profile_dao = ProfileDAO(session=self.session)
        profile_model: ProfileModel = await profile_dao.get_by_id(user_id=model.id)
        profile: Profile = Profile(id=profile_model.id, phone=profile_model.phone, address=profile_model.address)

        company_dao = CompanyDAO(session=self.session)
        company_models: list[CompanyModel] = await company_dao.list(dto=ListCompaniesInputDTO(owner_id=model.id))

        user = User(
            id=model.id,
            name=model.name,
            email=model.email,
            profile=profile,
            work_company=model.work_company_cnpj,
            companies=[company.cnpj for company in company_models],
            groups=group_result.groups,
            permissions=permission_result.permissions
        )

        return RetrieveUserOutputDTO(user=user)
