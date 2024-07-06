from ..presenters import RetrievePokemonPresenter
from ..dtos import RetrievePokemonInputDTO
from src.engines.caches import RedisCache
from src.engines.clients import HTTPxClient
from src.engines.requests import PokemonPokeAPIRepository


class RetrievePokemonRepository:
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
            model = await repository.get_by_id(self.input.id)
            return await output.present(model)
