from src.adapters.dtos import FindPokemonInputDTO, FindPokemonOutputDTO
from src.adapters.interfaces import PresenterInterface
from src.infrastructure.requests.interfaces import PokemonRepositoryInterface


class FindPokemonUseCase:
    def __init__(
            self,
            presenter: PresenterInterface,
            repository: PokemonRepositoryInterface
    ):
        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: FindPokemonInputDTO) -> dict:
        pokemon = await self.repository.find_by_id(input_dto.id)
        output_dto = FindPokemonOutputDTO(pokemon)
        return self.presenter.present(output_dto)
