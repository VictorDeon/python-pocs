from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.formatters import paginated
from .retrieve import RetrieveGroupPresenter
from ..dtos import ListGroupOutputDTO, RetrieveGroupOutputDTO
from ..models import Group


class ListGroupPresenter(PresenterInterface):
    """
    Formatação de saída da API que listar grupos.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, models: list[Group], limit: int = None, offset: int = None) -> ListGroupOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        groups: list[RetrieveGroupOutputDTO] = []
        presenter = RetrieveGroupPresenter(session=self.session)
        for model in models:
            group = await presenter.present(model)
            groups.append(group)

        paginated_groups: list[RetrieveGroupOutputDTO] = paginated(groups, offset, limit)

        return ListGroupOutputDTO(
            total=len(groups),
            groups=paginated_groups
        )
