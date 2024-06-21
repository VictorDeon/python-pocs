from src.adapters import ControllerInterface
from src.adapters.presenters import FindPokemonPresenter
from src.adapters.dtos import FindPokemonInputDTO
from src.domains.user_cases import FindPokemonUseCase
from src.infrastructure.caches.repositories import RedisCache
from src.infrastructure.clients.repositories import HTTPxClient
from src.infrastructure.requests.repositories import PokemonPokeAPIRepository


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

        async with HTTPxClient() as client, RedisCache() as cache:
            repository = PokemonPokeAPIRepository(client, cache)
            output = FindPokemonPresenter()
            use_case = FindPokemonUseCase(output, repository)
            return await use_case.execute(self.input)
