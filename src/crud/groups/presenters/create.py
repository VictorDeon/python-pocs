from sqlalchemy.ext.asyncio import AsyncSession
from .retrieve import RetrieveGroupPresenter
from ..dtos import CreateGroupOutputDTO
from ..models import Group


class CreateGroupPresenter:
    """
    Formatação de saída da API que cria um grupo.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, model: Group) -> CreateGroupOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveGroupPresenter(session=self.session)
        group = await presenter.present(model)
        return CreateGroupOutputDTO(**group.to_dict())
