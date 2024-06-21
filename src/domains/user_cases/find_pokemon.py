from src.adapters.dtos import FindPokemonInputDTO
from src.adapters import PresenterInterface
from src.domains import UserCaseInterface
from src.infrastructure.requests.interfaces import PokemonRepositoryInterface


class FindPokemonUseCase(UserCaseInterface):
    """
    Realiza o caso de uso de encontrar um pokemon pelo seu ID.
    """

    def __init__(self, presenter: PresenterInterface, repository: PokemonRepositoryInterface):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: FindPokemonInputDTO) -> dict:
        """
        Executa o caso de uso.
        """

        pokemon = await self.repository.find_by_id(input_dto.id)
        return self.presenter.present(pokemon)
