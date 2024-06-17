from abc import ABC, abstractmethod
from src.domains.entities.pokemon import Pokemon


class PokemonRepositoryInterface(ABC):
    @abstractmethod
    async def list(self, limit: int, offset: int) -> list[Pokemon]:
        pass

    @abstractmethod
    async def find_by_id(self, pokemon_id: int) -> Pokemon:
        pass
