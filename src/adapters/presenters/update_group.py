from src.adapters.dtos import UpdateGroupOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import Group as GroupModel
from .retrieve_group import RetrieveGroupPresenter


class UpdateGroupPresenter(PresenterInterface):
    """
    Formatação de saída da API que atualizar um grupo.
    """

    async def present(self, model: GroupModel) -> UpdateGroupOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveGroupPresenter(session=self.session)
        group = await presenter.present(model)
        return UpdateGroupOutputDTO(group=group)
