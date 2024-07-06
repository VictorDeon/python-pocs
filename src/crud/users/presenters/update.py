from src.adapters.dtos import UpdateUserOutputDTO
from src.adapters import PresenterInterface
from src.users.model import User as UserModel
from .retrieve_user import RetrieveUserPresenter


class UpdateUserPresenter(PresenterInterface):
    """
    Formatação de saída da API que atualizar um usuário.
    """

    async def present(self, model: UserModel) -> UpdateUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveUserPresenter(session=self.session)
        result = await presenter.present(model)
        return UpdateUserOutputDTO(user=result.user)
