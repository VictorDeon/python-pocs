from src.adapters.dtos import ListPermissionInputDTO, RetrieveUserOutputDTO, ListGroupInputDTO
from src.adapters import PresenterInterface
from src.domains.entities import User, Profile
from src.infrastructure.databases.models import (
    Group as GroupModel,
    Permission as PermissionModel,
    User as UserModel,
    Profile as ProfileModel
)
from src.infrastructure.databases.daos import PermissionDAO, GroupDAO, ProfileDAO
from .list_permissions import ListPermissionPresenter
from .list_groups import ListGroupPresenter


class RetrieveUserPresenter(PresenterInterface):
    """
    Formatação de saída da API que buscar um usuário.
    """

    async def present(self, model: UserModel) -> RetrieveUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        permission_dao = PermissionDAO(session=self.session)
        permissions: list[PermissionModel] = permission_dao.list(dto=ListPermissionInputDTO(user_id=model.id))
        permission_presenter = ListPermissionPresenter(session=self.session)

        group_dao = GroupDAO(session=self.session)
        groups: list[GroupModel] = group_dao.list(dto=ListGroupInputDTO(user_id=model.id))
        group_presenter = ListGroupPresenter(session=self.session)

        profile_dao = ProfileDAO(session=self.session)
        profile_model: ProfileModel = profile_dao.get_by_id(user_id=model.id)
        profile: Profile = Profile(id=profile_model.id, phone=profile_model.phone, address=profile_model.address)

        user = User(
            id=model.id,
            name=model.name,
            profile=profile,
            groups=group_presenter.present(groups),
            permissions=permission_presenter.present(permissions)
        )

        return RetrieveUserOutputDTO(user=user)
