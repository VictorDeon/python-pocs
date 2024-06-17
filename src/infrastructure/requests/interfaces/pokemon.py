from abc import ABC, abstractmethod
from src.domains.entities.pokemon import Pokemon


class PokemonRepositoryInterface(ABC):
    """
    Interface para gerar o repositório de consulta a API de pokemons.
    """

    @abstractmethod
    async def list(self, limit: int, offset: int) -> list[Pokemon]:
        """
        Método responsável por listar todos os pokemons.
        """

        pass

    @abstractmethod
    async def find_by_id(self, pokemon_id: int) -> Pokemon:
        """
        Método responsável por encontrar um determinado pokemon.
        """

        pass
