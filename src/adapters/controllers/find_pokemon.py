from ..interfaces import ControllerInterface
from ..presenters import FindPokemonPresenter
from ..dtos import FindPokemonInputDto
from src.infrastructure.caches.repositories import RedisCache
from src.infrastructure.clients.repositories import HTTPxClient
from src.infrastructure.requests.repositories import PokemonPokeAPIRepository
from src.domains.user_cases import FindPokemonUseCase


class FindPokemonController(ControllerInterface):
    def __init__(self):
        self.input_dto: FindPokemonInputDto

    def get_pokemon_id(self, params: dict) -> None:
        self.input_dto = FindPokemonInputDto(
            id=params.get("id")
        )

    async def execute(self) -> dict:
        http_client = HTTPxClient()
        cache_client = RedisCache()
        repository = PokemonPokeAPIRepository(http_client, cache_client)
        presenter = FindPokemonPresenter()
        use_case = FindPokemonUseCase(presenter, repository)
        return await use_case.execute(self.input_dto)
