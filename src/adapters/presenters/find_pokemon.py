import math
from src.adapters.dtos import FindPokemonOutputDTO
from src.adapters.interfaces import PresenterInterface


class FindPokemonPresenter(PresenterInterface):
    """
    Formatação de saída da API que busca um pokemon.
    """

    def present(self, output_dto: FindPokemonOutputDTO) -> dict:
        """
        Forma final de apresentação dos dados.
        """

        pokemon = output_dto.pokemon.to_dict()
        pokemon['types'] = ", ".join(_type['type']['name'] for _type in output_dto.pokemon.types)
        pokemon['sprites'] = output_dto.pokemon.sprites['front_default']
        pokemon['weight'] = self.__convert_hectograms_to_pounds(output_dto.pokemon.weight)
        pokemon['height'] = self.__convert_decimeters_to_feet_and_inches(output_dto.pokemon.height)
        pokemon['species'] = self.__get_en_category(output_dto.pokemon.species)
        pokemon['abilities'] = self.__get_abilities(pokemon['abilities'])
        pokemon['stats'] = {}
        for stat in output_dto.pokemon.stats:
            pokemon['stats'][f"{stat['stat']['name']}"] = stat['base_stat']

        return pokemon

    def __convert_decimeters_to_feet_and_inches(self, decimeters: int) -> str:
        """
        Converte decimal para feet ou inches.
        """

        centimeters = decimeters * 10
        total_inches = centimeters / 2.54
        feet = int(total_inches // 12)
        inches = math.ceil(total_inches % 12)
        return f"{feet} feet {inches:02} inches"

    def __convert_hectograms_to_pounds(self, hectograms: int) -> float:
        """
        Converte hectogram para pounds
        """

        return round(hectograms * 0.1 * 2.20462, 1)

    def __get_abilities(self, abilities: list[dict[str, str]]) -> list[str]:
        """
        Formata a lista de habilidades.
        """

        return [ability['ability']['name'] for ability in abilities if not ability['is_hidden']]

    def __get_en_category(self, species: dict[str, str]) -> str:
        """
        Pega as categorias.
        """

        category = ''
        for genus in species.get('genera', []):
            if genus.get('language', {}).get('name') == 'en':
                category = genus.get('genus').replace(' Pokémon', '')
                break
        return category
