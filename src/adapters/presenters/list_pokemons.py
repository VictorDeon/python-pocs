from ..dtos import ListPokemonsOutputDTO
from ..interfaces import PresenterInterface


class ListPokemonsPresenter(PresenterInterface):
    """
    Formatação de saída da API que lista os pokemons.
    """

    def present(self, output_dto: ListPokemonsOutputDTO) -> dict:
        """
        Forma final de apresentação dos dados.
        """

        sorted_pokemons = sorted(output_dto.pokemons, key=lambda pokemon: pokemon.id)
        return {
            'results': [
                {
                    'id': pokemon.id,
                    'name': pokemon.name,
                    'sprites': pokemon.sprites,
                    'types': pokemon.types,
                } for pokemon in sorted_pokemons
            ]
        }
