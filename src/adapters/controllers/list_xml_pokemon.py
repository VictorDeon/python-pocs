from ..interfaces import ControllerInterface
from ..presenters import ListXMLPokemonsPresenter
from ..dtos import ListPokemonsInputDto
from src.infrastructure.caches.repositories import RedisCache
from src.infrastructure.clients.repositories import HTTPxClientSingleton
from src.infrastructure.requests.repositories import PokemonPokeAPIRepository
from src.domains.user_cases import ListPokemonsUseCase


class ListXMLPokemonController(ControllerInterface):
    def __init__(self):
        self.input_dto: ListPokemonsInputDto

    def get_search_params(self, params: dict) -> None:
        self.input_dto = ListPokemonsInputDto(
            limit=params.get("limit"),
            offset=params.get("offset")
        )

    async def execute(self) -> str:
        client = HTTPxClientSingleton.get_instance()
        cache_client = RedisCache()
        repository = PokemonPokeAPIRepository(client, cache_client)
        presenter = ListXMLPokemonsPresenter()
        use_case = ListPokemonsUseCase(presenter, repository)
        return await use_case.execute(self.input_dto)
