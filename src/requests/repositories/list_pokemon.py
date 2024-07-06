import asyncio
import os
from ..presenters import ListPokemonsPresenter
from ..dtos import ListPokemonsInputDTO
from src.engines.caches import RedisCache
from src.engines.clients import HTTPxClient
from src.engines.requests import PokemonPokeAPIRepository


class ListPokemonRepository:
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

        # O semaforo limita a quantidade de tarefas/requisições a acessar
        # um recurso simultaneamente por segundo, no caso: 5 TPS
        async with asyncio.Semaphore(int(os.environ.get("SEMAPHORE", 5))):
            async with HTTPxClient() as client, RedisCache() as cache:
                repository = PokemonPokeAPIRepository(client, cache)
                presenter = ListPokemonsPresenter()
                pokemons = await repository.list(
                    limit=self.input_dto.limit,
                    offset=self.input_dto.offset
                )
                return await presenter.present(pokemons)
