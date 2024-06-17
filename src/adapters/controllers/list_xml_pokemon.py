from ..interfaces import ControllerInterface
from ..presenters import ListXMLPokemonsPresenter
from ..dtos import ListPokemonsInputDTO
from src.infrastructure.caches.repositories import RedisCacheSingleton
from src.infrastructure.clients.repositories import HTTPxClientSingleton
from src.infrastructure.requests.repositories import PokemonPokeAPIRepository
from src.domains.user_cases import ListPokemonsUseCase


class ListXMLPokemonController(ControllerInterface):
    def __init__(self):
        self.input_dto: ListPokemonsInputDTO

    def get_search_params(self, params: dict) -> None:
        self.input_dto = ListPokemonsInputDTO(
            limit=params.get("limit"),
            offset=params.get("offset")
        )

    async def execute(self) -> str:
        client = HTTPxClientSingleton.get_instance()
        cache = RedisCacheSingleton.get_instance()
        repository = PokemonPokeAPIRepository(client, cache)
        presenter = ListXMLPokemonsPresenter()
        use_case = ListPokemonsUseCase(presenter, repository)
        return await use_case.execute(self.input_dto)
