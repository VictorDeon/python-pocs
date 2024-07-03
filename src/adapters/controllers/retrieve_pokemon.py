from src.adapters import ControllerInterface
from src.adapters.presenters import RetrievePokemonPresenter
from src.adapters.dtos import RetrievePokemonInputDTO
from src.domains.user_cases import GetByIdUserCase
from src.infrastructure.caches.repositories import RedisCache
from src.infrastructure.clients.repositories import HTTPxClient
from src.infrastructure.requests.repositories import PokemonPokeAPIRepository


class RetrievePokemonController(ControllerInterface):
    """
    Constroladora para encontrar um pokemon.
    """

    def __init__(self, pokemon_id: int):
        """
        Construtor.
        """

        self.input = RetrievePokemonInputDTO(id=pokemon_id)

    async def execute(self) -> dict:
        """
        Executa os comandos para gerar o resultado.
        """

        async with HTTPxClient() as client, RedisCache() as cache:
            repository = PokemonPokeAPIRepository(client, cache)
            output = RetrievePokemonPresenter()
            use_case = GetByIdUserCase(output, repository)
            return await use_case.execute(self.input.id)
