from src.adapters.dtos import ListPokemonsOutputDto, ListPokemonsInputDto
from src.adapters.interfaces import PresenterInterface
from src.infrastructure.databases.interfaces import PokemonRepositoryInterface


class ListPokemonsUseCase:
    def __init__(
            self,
            presenter: PresenterInterface,
            repository: PokemonRepositoryInterface
    ):
        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: ListPokemonsInputDto):
        pokemons = await self.repository.list(
            limit=input_dto.limit,
            offset=input_dto.offset
        )
        output_dto = ListPokemonsOutputDto(pokemons)
        return self.presenter.present(output_dto)
