from ..presenters import ListPokemonsPresenter
from ..dtos import ListPokemonsInputDTO
from src.engines.caches import RedisCache
from src.engines.clients import HTTPxClient
from src.engines.requests import PokemonQueueRequestRepository


class ListQueuePokemonRepository:
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

        async with HTTPxClient() as client, RedisCache() as cache:
            repository = PokemonQueueRequestRepository(client, cache)
            presenter = ListPokemonsPresenter()
            pokemons = await repository.list(
                limit=self.input_dto.limit,
                offset=self.input_dto.offset
            )
            return await presenter.present(pokemons)
