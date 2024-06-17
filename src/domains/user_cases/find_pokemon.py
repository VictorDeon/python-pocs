from src.adapters.dtos import FindPokemonInputDto, FindPokemonOutputDto
from src.adapters.interfaces import PresenterInterface
from src.infrastructure.databases.interfaces import PokemonRepositoryInterface


class FindPokemonUseCase:
    def __init__(
            self,
            presenter: PresenterInterface,
            repository: PokemonRepositoryInterface
    ):
        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: FindPokemonInputDto) -> dict:
        pokemon = await self.repository.find_by_id(input_dto.id)
        output_dto = FindPokemonOutputDto(pokemon)
        return self.presenter.present(output_dto)
