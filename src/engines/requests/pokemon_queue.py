import asyncio
import os
from typing import List
from src.requests.dtos.pokemon import Pokemon
from src.engines.logger import ProjectLoggerSingleton
from src.engines.constants import POKEAPI_URL
from src.engines.caches import RedisCache
from src.engines.clients import HTTPxClient


class PokemonQueueRequestRepository:
    """
    Repositorio que faz a lógica de consulta de pesquisa do pokemon
    usando a estratégia de requisição assincrona com Queue.
    """

    def __init__(self, client: HTTPxClient, cache: RedisCache) -> None:
        """
        Construtor.
        """

        self.base_url = POKEAPI_URL
        self.http_client = client
        self.cache_client = cache
        self.logger = ProjectLoggerSingleton.get_logger()
        self.qtd_workers = int(os.environ.get("QTD_WORKERS", 20))

    async def __worker(self, url_queue: asyncio.Queue, responses: List[dict]) -> None:
        """
        Trabalhador que irá consultar a API de pokemons.
        """

        while True:
            pokemon = await url_queue.get()
            if pokemon is None:
                break

            self.logger.info(f"Buscando dados do pokemon: {pokemon['name']}")
            response = await self.cache_client.get(pokemon['url'])

            if not response:
                response = await self.http_client.get(pokemon['url'])
                await self.cache_client.set(pokemon['url'], response, exp=3600)

            responses.append(response)
            url_queue.task_done()

    async def list(self, limit: int, offset: int) -> list[Pokemon]:
        """
        Método responsável por listar todos os pokemons.
        """

        self.logger.info("Iniciando a pesquisa")

        responses = []
        worker_tasks = []
        url_queue = asyncio.Queue()

        if limit is None:
            response = await self.http_client.get(f'{self.base_url}/pokemon')
            limit = response.get('count')
            offset = 0

        response = await self.http_client.get(f'{self.base_url}/pokemon?limit={limit}&offset={offset}')
        pokemons = response.get('results')

        # Insere todas as urls dentro da fila.
        for pokemon in pokemons:
            await url_queue.put(pokemon)

        # Cria 20 trabalhadores para puxar todos os pokemons
        for _ in range(self.qtd_workers):
            worker_tasks.append(asyncio.create_task(self.__worker(url_queue, responses)))

        # Espera todos os itens da fila ser processados.
        await url_queue.join()

        return [Pokemon.from_dict(pokemon) for pokemon in responses]

    async def get_by_id(self, _id: int) -> Pokemon:
        """
        Método responsável por encontrar um determinado pokemon.
        """

        response = await self.http_client.get(f'{self.base_url}/pokemon/{_id}')
        response['weaknesses'], response['strengths'] = await self.__get_weaknesses_and_strengths(
            response.get('types', [])
        )
        response['species'] = await self.__get_species(response.get('species', {}).get('url'))

        return Pokemon.from_dict(response)

    async def __get_weaknesses_and_strengths(self, types: List[dict]) -> tuple[dict]:
        """
        Pega as fraquezas do pokemon
        """

        weaknesses = set()
        strengths = set()
        for _type in types:
            type_url = _type['type']['url']
            type_data = await self.http_client.get(type_url)
            for damage_relation in type_data['damage_relations']['double_damage_from']:
                weaknesses.add(damage_relation['name'])

            for damage_relation in type_data['damage_relations']['double_damage_to']:
                strengths.add(damage_relation['name'])

        return list(weaknesses), list(strengths)

    async def __get_species(self, species_url: str):
        """
        Pega os dados da espécie do pokemon.
        """

        return await self.http_client.get(species_url)
