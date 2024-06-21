from src.adapters.dtos import ListPokemonsInputDTO
from src.adapters import PresenterInterface
from src.infrastructure.requests.interfaces import PokemonRepositoryInterface


class ListPokemonsUseCase:
    """
    Realiza o caso de uso de listar os pokemons.
    """

    def __init__(self, presenter: PresenterInterface, repository: PokemonRepositoryInterface):
        """
        Construtor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: ListPokemonsInputDTO):
        """
        Executa o caso de uso.
        """

        pokemons = await self.repository.list(
            limit=input_dto.limit,
            offset=input_dto.offset
        )
        return self.presenter.present(pokemons)
