from ..interfaces import ControllerInterface
from ..presenters import ListPokemonsPresenter
from ..dtos import ListPokemonsInputDTO
from src.infrastructure.caches.repositories import RedisCacheSingleton
from src.infrastructure.clients.repositories import HTTPxClientSingleton
from src.infrastructure.requests.repositories import PokemonPokeAPIRepository
from src.domains.user_cases import ListPokemonsUseCase


class ListPokemonController(ControllerInterface):
    """
    Constroladora para listar todos os pokemons.
    """

    def __init__(self, limit: int, offset: int):
        """
        Construtor.
        """

        self.input_dto = ListPokemonsInputDTO(offset=offset, limit=limit)

    async def execute(self) -> dict:
        """
        Executa os comandos para gerar o resultado.
        """

        client = HTTPxClientSingleton.get_instance()
        cache = RedisCacheSingleton.get_instance()
        repository = PokemonPokeAPIRepository(client, cache)
        presenter = ListPokemonsPresenter()
        use_case = ListPokemonsUseCase(presenter, repository)

        try:
            results = await use_case.execute(self.input_dto)
        except Exception as error:
            # Instrumentalizar
            raise error
        finally:
            await client.close_connection()
            await cache.close_connection()

        return results
