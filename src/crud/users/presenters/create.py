from sqlalchemy.ext.asyncio import AsyncSession
from .retrieve import RetrieveUserPresenter
from ..dtos import CreateUserOutputDTO
from ..models import User


class CreateUserPresenter:
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
        user = await presenter.present(model)
        return CreateUserOutputDTO(**user.to_dict())
