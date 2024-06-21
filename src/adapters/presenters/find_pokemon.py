import math
from src.adapters.dtos.find_pokemon import FindPokemonOutputDTO, PokemonOutput
from src.adapters import PresenterInterface
from src.domains.entities import Pokemon


class FindPokemonPresenter(PresenterInterface):
    """
    Formatação de saída da API que busca um pokemon.
    """

    def present(self, pokemon: Pokemon) -> FindPokemonOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        output = PokemonOutput(
            id=pokemon.id,
            name=pokemon.name,
            types=", ".join(_type['type']['name'] for _type in pokemon.types),
            sprite=pokemon.sprites['front_default'],
            weight=self.__convert_hectograms_to_pounds(pokemon.weight),
            height=self.__convert_decimeters_to_feet_and_inches(pokemon.height),
            category=self.__get_en_category(pokemon.species),
            abilities=self.__get_abilities(pokemon.abilities),
            weaknesses=pokemon.weaknesses,
            strengths=pokemon.strengths,
            status={}
        )

        for stat in pokemon.stats:
            output.status[f"{stat['stat']['name']}"] = stat['base_stat']

        return FindPokemonOutputDTO(pokemon=output)

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
