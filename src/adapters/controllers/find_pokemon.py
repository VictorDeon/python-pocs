from ..interfaces import ControllerInterface
from ..presenters import FindPokemonPresenter
from ..dtos import FindPokemonInputDTO
from src.infrastructure.caches.repositories import RedisCacheSingleton
from src.infrastructure.clients.repositories import HTTPxClientSingleton
from src.infrastructure.requests.repositories import PokemonPokeAPIRepository
from src.domains.user_cases import FindPokemonUseCase


class FindPokemonController(ControllerInterface):
    """
    Constroladora para encontrar um pokemon.
    """

    def __init__(self, pokemon_id: int):
        """
        Construtor.
        """

        self.input = FindPokemonInputDTO(id=pokemon_id)

    async def execute(self) -> dict:
        """
        Executa os comandos para gerar o resultado.
        """

        results = None
        client = HTTPxClientSingleton.get_instance()
        cache = RedisCacheSingleton.get_instance()
        repository = PokemonPokeAPIRepository(client, cache)
        output = FindPokemonPresenter()
        use_case = FindPokemonUseCase(output, repository)

        try:
            results = await use_case.execute(self.input)
        except Exception as error:
            # Instrumentalizar
            raise error
        finally:
            await client.close_connection()
            await cache.close_connection()

        return results
