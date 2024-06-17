from src.adapters.dtos import ListPokemonsOutputDTO, ListPokemonsInputDTO
from src.adapters.interfaces import PresenterInterface
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
        output_dto = ListPokemonsOutputDTO(pokemons=pokemons)
        return self.presenter.present(output_dto)
