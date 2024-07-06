import math
from ..dtos import RetrievePokemonOutputDTO, RetrievePokemonOutput, Pokemon


class RetrievePokemonPresenter:
    """
    Formatação de saída da API que busca um pokemon.
    """

    async def present(self, model: Pokemon) -> RetrievePokemonOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        status = {}
        for stat in model.stats:
            status[f"{stat['stat']['name']}"] = stat['base_stat']

        pokemon = RetrievePokemonOutput(
            id=model.id,
            name=model.name,
            types=", ".join(_type['type']['name'] for _type in model.types),
            sprite=model.sprites['front_default'],
            weight=self.__convert_hectograms_to_pounds(model.weight),
            height=self.__convert_decimeters_to_feet_and_inches(model.height),
            category=self.__get_en_category(model.species),
            abilities=self.__get_abilities(model.abilities),
            weaknesses=model.weaknesses,
            strengths=model.strengths,
            status=status
        )

        return RetrievePokemonOutputDTO(pokemon=pokemon)

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
