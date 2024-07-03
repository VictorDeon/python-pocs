import asyncio
import os
from src.adapters import ControllerInterface
from src.adapters.presenters import ListPokemonsPresenter
from src.adapters.dtos import ListPokemonsInputDTO
from src.domains.user_cases import ListPokemonsUseCase
from src.infrastructure.caches.repositories import RedisCache
from src.infrastructure.clients.repositories import HTTPxClient
from src.infrastructure.requests.repositories import PokemonPokeAPIRepository


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

        # O semaforo limita a quantidade de tarefas/requisições a acessar
        # um recurso simultaneamente por segundo, no caso: 5 TPS
        async with asyncio.Semaphore(int(os.environ.get("SEMAPHORE", 5))):
            async with HTTPxClient() as client, RedisCache() as cache:
                repository = PokemonPokeAPIRepository(client, cache)
                presenter = ListPokemonsPresenter()
                use_case = ListPokemonsUseCase(presenter, repository)
                return await use_case.execute(self.input_dto)
