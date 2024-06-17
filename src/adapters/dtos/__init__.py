""" DATA TRANSFER OBJECT (DTO) """
from .find_pokemon import FindPokemonInputDTO, FindPokemonOutputDTO
from .list_pokemons import ListPokemonsInputDto, ListPokemonsOutputDto

__all__ = [
    FindPokemonInputDTO,
    FindPokemonOutputDTO,
    ListPokemonsInputDto,
    ListPokemonsOutputDto
]
