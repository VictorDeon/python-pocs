from src.adapters.dtos import ListUserOutputDTO
from src.adapters import PresenterInterface
from src.domains.utils.formatters import paginated
from src.domains.entities import User
from src.infrastructure.databases.models import User as UserModel
from .retrieve_user import RetrieveUserPresenter


class ListUserPresenter(PresenterInterface):
    """
    Formatação de saída da API que listar usuários.
    """

    async def present(self, models: list[UserModel], limit: int, offset: int) -> ListUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveUserPresenter(session=self.session)
        users: list[User] = []
        for model in models:
            result = await presenter.present(model)
            users.append(result.user)

        paginated_users: list[User] = paginated(users, offset, limit)

        return ListUserOutputDTO(
            total=len(users),
            users=paginated_users
        )
