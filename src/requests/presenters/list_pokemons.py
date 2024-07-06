from ..dtos import ListPokemonsOutputDTO, ListPokemonOutput
from src.domains.entities import Pokemon


class ListPokemonsPresenter:
    """
    Formatação de saída da API que lista os pokemons.
    """

    async def present(self, model: list[Pokemon]) -> ListPokemonsOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        sorted_pokemons = sorted(model, key=lambda pokemon: pokemon.id)

        return ListPokemonsOutputDTO(pokemons=[
            ListPokemonOutput(
                id=pokemon.id,
                name=pokemon.name,
                sprite=pokemon.sprites['front_default'],
                types=", ".join([_type['type']['name'] for _type in pokemon.types])
            ) for pokemon in sorted_pokemons
        ])
