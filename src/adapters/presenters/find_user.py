from src.adapters.dtos import FindUserOutputDTO
from src.adapters.interfaces import PresenterInterface
from src.domains.entities import User


class FindUserPresenter(PresenterInterface):
    """
    Formatação de saída da API que busca um usuário.
    """

    def present(self, user: User) -> FindUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        return FindUserOutputDTO(user=user)
