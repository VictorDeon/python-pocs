from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.formatters import paginated
from .retrieve import RetrieveUserPresenter
from ..dtos import ListUserOutputDTO, RetrieveUserOutputDTO
from ..models import User


class ListUserPresenter:
    """
    Formatação de saída da API que listar usuários.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, models: list[User], limit: int = None, offset: int = None) -> ListUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveUserPresenter(session=self.session)
        users: list[RetrieveUserOutputDTO] = []
        for model in models:
            user = await presenter.present(model)
            users.append(user)

        paginated_users: list[RetrieveUserOutputDTO] = paginated(users, offset, limit)

        return ListUserOutputDTO(
            total=len(users),
            users=paginated_users
        )
