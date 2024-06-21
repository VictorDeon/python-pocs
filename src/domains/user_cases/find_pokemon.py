from src.adapters.dtos import FindPokemonInputDTO, FindPokemonOutputDTO
from src.adapters import PresenterInterface
from src.domains import UserCaseInterface
from src.domains.entities import Pokemon
from src.infrastructure.requests import RequestRepositoryInterface


class FindPokemonUseCase(UserCaseInterface):
    """
    Realiza o caso de uso de encontrar um pokemon pelo seu ID.
    """

    def __init__(
        self,
        presenter: PresenterInterface[Pokemon, FindPokemonOutputDTO],
        repository: RequestRepositoryInterface[Pokemon]):
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
