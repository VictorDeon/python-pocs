""" DATA TRANSFER OBJECT (DTO) """
from .find_pokemon import FindPokemonInputDTO, FindPokemonOutputDTO
from .list_pokemons import ListPokemonsInputDTO, ListPokemonsOutputDTO

__all__ = [
    FindPokemonInputDTO,
    FindPokemonOutputDTO,
    ListPokemonsInputDTO,
    ListPokemonsOutputDTO
]
