from src.adapters.dtos import FindUserOutputDTO
from src.adapters.interfaces import PresenterInterface
from src.infrastructure.databases.models import User as UserModel
from src.domains.entities import User, Profile, Permission, Group


class FindUserPresenter(PresenterInterface):
    """
    Formatação de saída da API que busca um usuário.
    """

    def present(self, user: UserModel) -> FindUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        entity = User(
            id=user.id,
            name=user.name,
            email=user.email,
            profile=Profile(
                id=user.profile.id,
                phone=user.profile.phone,
                address=user.profile.address
            ),
            permissions=[
                Permission(
                    id=permission.id,
                    name=permission.name
                ) for permission in user.permissions
            ],
            groups=[
                Group(
                    id=group.id,
                    name=group.name,
                    permissions=[
                        Permission(
                            id=permission.id,
                            name=permission.name
                        ) for permission in group.permissions
                    ]
                ) for group in user.groups
            ]
        )

        return FindUserOutputDTO(user=entity)
