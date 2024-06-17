from ..interfaces import ControllerInterface
from ..presenters import ListPokemonsPresenter
from ..dtos import ListPokemonsInputDto
from src.infrastructure.caches.repositories import RedisCache
from src.infrastructure.clients.repositories import HTTPxClient
from src.infrastructure.databases.repositories import PokemonPokeAPIRepository
from src.domains.user_cases import ListPokemonsUseCase


class ListPokemonController(ControllerInterface):
    def __init__(self):
        self.input_dto: ListPokemonsInputDto

    def get_search_params(self, params: dict) -> None:
        self.input_dto = ListPokemonsInputDto(
            limit=params.get("limit"),
            offset=params.get("offset")
        )

    async def execute(self) -> dict:
        http_client = HTTPxClient()
        cache_client = RedisCache()
        repository = PokemonPokeAPIRepository(http_client, cache_client)
        presenter = ListPokemonsPresenter()
        use_case = ListPokemonsUseCase(presenter, repository)
        return await use_case.execute(self.input_dto)
