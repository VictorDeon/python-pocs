from ..presenters import ListXMLPokemonsPresenter
from ..dtos import ListPokemonsInputDTO
from src.engines.caches import RedisCache
from src.engines.clients import HTTPxClient
from src.engines.requests import PokemonPokeAPIRepository


class ListXMLPokemonRepository:
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
            pokemons = await repository.list(
                limit=self.input_dto.limit,
                offset=self.input_dto.offset
            )
            return await presenter.present(pokemons)
