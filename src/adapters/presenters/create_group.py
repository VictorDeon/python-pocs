from src.adapters.dtos import CreateGroupOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import Group as GroupModel
from .retrieve_group import RetrieveGroupPresenter


class CreateGroupPresenter(PresenterInterface):
    """
    Formatação de saída da API que cria um grupo.
    """

    async def present(self, model: GroupModel) -> CreateGroupOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveGroupPresenter(session=self.session)
        group = await presenter.present(model)
        return CreateGroupOutputDTO(group=group)
