from ..dtos import ListPokemonsOutputDto
from ..interfaces import PresenterInterface


class ListPokemonsPresenter(PresenterInterface):
    def present(self, output_dto: ListPokemonsOutputDto) -> dict:
        sorted_pokemons = sorted(output_dto.pokemons, key=lambda pokemon: pokemon.name)
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
