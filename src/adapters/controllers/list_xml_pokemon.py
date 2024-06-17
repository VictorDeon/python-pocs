from ..interfaces import ControllerInterface
from ..presenters import ListXMLPokemonsPresenter
from ..dtos import ListPokemonsInputDTO
from src.infrastructure.caches.repositories import RedisCache
from src.infrastructure.clients.repositories import HTTPxClient
from src.infrastructure.requests.repositories import PokemonPokeAPIRepository
from src.domains.user_cases import ListPokemonsUseCase


class ListXMLPokemonController(ControllerInterface):
    """
    Constroladora para listar todos os pokemons em XML.
    """

    def __init__(self, limit: int, offset: int):
        """
        Construtor.
        """

        self.input_dto = ListPokemonsInputDTO(limit=limit, offset=offset)

    async def execute(self) -> str:
        """
        Executa os comandos para gerar o resultado.
        """

        async with HTTPxClient() as client, RedisCache() as cache:
            repository = PokemonPokeAPIRepository(client, cache)
            presenter = ListXMLPokemonsPresenter()
            use_case = ListPokemonsUseCase(presenter, repository)
            return await use_case.execute(self.input_dto)