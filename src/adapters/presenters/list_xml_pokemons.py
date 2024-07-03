from xml.etree.ElementTree import Element, tostring
from src.domains.entities import Pokemon
from src.adapters import PresenterInterface


class ListXMLPokemonsPresenter(PresenterInterface):
    """
    Formatação de saída da API que lista os pokemons em XML.
    """

    async def present(self, pokemons: list[Pokemon]) -> str:
        """
        Forma final de apresentação dos dados.
        """

        sorted_pokemons = sorted(pokemons, key=lambda pokemon: pokemon.id)
        root = Element('pokemons')
        for pokemon in sorted_pokemons:
            pokemon_element = Element('pokemon')
            id_element = Element('id')
            id_element.text = str(pokemon.id)
            name_element = Element('name')
            name_element.text = pokemon.name
            sprint_element = Element('sprite')
            sprint_element.text = pokemon.sprites['front_default']
            types_element = Element('types')
            types_element.text = ", ".join([_type['type']['name'] for _type in pokemon.types])

            pokemon_element.append(id_element)
            pokemon_element.append(name_element)
            pokemon_element.append(sprint_element)
            pokemon_element.append(types_element)
            root.append(pokemon_element)

        return tostring(root, encoding='utf8', method='xml')
