from src.adapters import PresenterInterface
from src.adapters.presenters.retrieve_user import RetrieveUserPresenter
from sqlalchemy.ext.asyncio import AsyncSession
from ..dtos import CreateUserOutputDTO
from ..models import User


class CreateUserPresenter(PresenterInterface):
    """
    Formatação de saída da API que cria um usuário.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, model: User) -> CreateUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveUserPresenter(session=self.session)
        result = await presenter.present(model)
        return CreateUserOutputDTO(user=result.user)
