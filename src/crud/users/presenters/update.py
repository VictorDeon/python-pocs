from sqlalchemy.ext.asyncio import AsyncSession
from .retrieve import RetrieveUserPresenter
from ..dtos import UpdateUserOutputDTO
from ..models import User


class UpdateUserPresenter:
    """
    Formatação de saída da API que atualizar um usuário.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, model: User) -> UpdateUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveUserPresenter(session=self.session)
        user = await presenter.present(model)
        return UpdateUserOutputDTO(**user.to_dict())
