""" DATA TRANSFER OBJECT (DTO) """
from .find_pokemon import FindPokemonInputDTO, FindPokemonOutputDTO
from .list_pokemons import ListPokemonsInputDTO, ListPokemonsOutputDTO
from .pdf_generator import PDFGeneratorInputDTO, PDFGeneratorOutputDTO

__all__ = [
    FindPokemonInputDTO,
    FindPokemonOutputDTO,
    ListPokemonsInputDTO,
    ListPokemonsOutputDTO,
    PDFGeneratorInputDTO,
    PDFGeneratorOutputDTO
]
