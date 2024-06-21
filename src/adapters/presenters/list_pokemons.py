from src.adapters.dtos.list_pokemons import ListPokemonsOutputDTO, PokemonOutput
from src.adapters import PresenterInterface
from src.domains.entities import Pokemon


class ListPokemonsPresenter(PresenterInterface):
    """
    Formatação de saída da API que lista os pokemons.
    """

    def present(self, output: list[Pokemon]) -> ListPokemonsOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        sorted_pokemons = sorted(output, key=lambda pokemon: pokemon.id)

        return ListPokemonsOutputDTO(pokemons=[
            PokemonOutput(
                id=pokemon.id,
                name=pokemon.name,
                sprite=pokemon.sprites['front_default'],
                types=", ".join([_type['type']['name'] for _type in pokemon.types])
            ) for pokemon in sorted_pokemons
        ])
