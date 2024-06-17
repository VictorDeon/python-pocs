import asyncio
import json
from src.infrastructure.constants import POKEAPI_URL
from src.domains.entities.pokemon import Pokemon
from src.infrastructure.caches.cache_interface import CacheClientInterface
from src.infrastructure.clients.client_interface import HttpClientSingletonInterface
from src.infrastructure.requests.interfaces import PokemonRepositoryInterface


class PokemonPokeAPIRepository(PokemonRepositoryInterface):
    def __init__(self, http_client: HttpClientSingletonInterface, cache_client: CacheClientInterface):
        self.base_url = POKEAPI_URL
        self.http_client = http_client
        self.cache_client = cache_client

    async def __worker(self, url_queue: asyncio.Queue, responses: list):
        while True:
            url = await url_queue.get()
            if url is None:
                break

            cached = await self.cache_client.get_value(url)

            if cached:
                response = json.loads(cached)
            else:
                response = await self.http_client.get(url)
                await self.cache_client.set_value(url, json.dumps(response), expire=3600)

            responses.append(response)
            url_queue.task_done()

    async def list(self, limit: int, offset: int) -> list[Pokemon]:
        responses = []
        worker_tasks = []
        url_queue = asyncio.Queue()

        if limit is None:
            response = await self.http_client.get(f'{self.base_url}/pokemon')
            limit = response.get('count')
            offset = 0

        response = await self.http_client.get(f'{self.base_url}/pokemon?limit={limit}&offset={offset}')
        pokemons = response.get('results')

        for pokemon in pokemons:
            await url_queue.put(pokemon['url'])

        for _ in range(20):
            worker_tasks.append(asyncio.create_task(self.__worker(url_queue, responses)))

        await url_queue.join()

        for _ in range(20):
            await url_queue.put(None)

        await asyncio.gather(*worker_tasks)
        return [Pokemon.from_dict(pokemon) for pokemon in responses]

    async def find_by_id(self, pokemon_id: int) -> Pokemon:
        response = await self.http_client.get(f'{self.base_url}/pokemon/{pokemon_id}')
        response['weaknesses'] = await self.__get_weaknesses(response.get('types', []))
        response['species'] = await self.__get_species(response.get('species', {}).get('url'))

        return Pokemon.from_dict(response)

    async def __get_weaknesses(self, types):
        weaknesses = set()
        for _type in types:
            type_url = _type['type']['url']
            type_data = await self.http_client.get(type_url)
            for damage_relation in type_data['damage_relations']['double_damage_from']:
                weaknesses.add(damage_relation['name'])
        return list(weaknesses)

    async def __get_species(self, species_url):
        return await self.http_client.get(species_url)
