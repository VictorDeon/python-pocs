""" DATA TRANSFER OBJECT (DTO) """
from .find_pokemon import FindPokemonInputDto, FindPokemonOutputDto
from .list_pokemons import ListPokemonsInputDto, ListPokemonsOutputDto

__all__ = [
    FindPokemonInputDto,
    FindPokemonOutputDto,
    ListPokemonsInputDto,
    ListPokemonsOutputDto
]
