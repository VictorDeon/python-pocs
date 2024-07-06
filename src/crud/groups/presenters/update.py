from sqlalchemy.ext.asyncio import AsyncSession
from .retrieve import RetrieveGroupPresenter
from ..dtos import UpdateGroupOutputDTO
from ..models import Group


class UpdateGroupPresenter:
    """
    Formatação de saída da API que atualizar um grupo.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, model: Group) -> UpdateGroupOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveGroupPresenter(session=self.session)
        group = await presenter.present(model)
        return UpdateGroupOutputDTO(**group.to_dict())
