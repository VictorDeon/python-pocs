from src.adapters.dtos import FindUserOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import User as UserModel
from src.domains.entities import User, Profile, Permission, Group


class FindUserPresenter(PresenterInterface):
    """
    Formatação de saída da API que busca um usuário.
    """

    def present(self, model: UserModel) -> FindUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        user = User(
            id=model.id,
            name=model.name,
            email=model.email,
            profile=Profile(
                id=model.profile.id,
                phone=model.profile.phone,
                address=model.profile.address
            ),
            permissions=[
                Permission(
                    id=permission.id,
                    name=permission.name
                ) for permission in model.permissions
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
                ) for group in model.groups
            ]
        )

        return FindUserOutputDTO(user=user)
