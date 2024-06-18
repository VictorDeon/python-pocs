from src.adapters.dtos import ListPokemonsOutputDTO
from src.adapters.interfaces import PresenterInterface


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
            'pokemons': [
                {
                    'id': pokemon.id,
                    'name': pokemon.name,
                    'sprite': pokemon.sprites['front_default'],
                    'types': ", ".join([_type['type']['name'] for _type in pokemon.types]),
                } for pokemon in sorted_pokemons
            ]
        }
