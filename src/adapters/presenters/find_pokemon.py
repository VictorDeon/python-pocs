import math
from ..dtos import FindPokemonInputDTO
from ..interfaces import PresenterInterface


class FindPokemonPresenter(PresenterInterface):
    def present(self, output_dto: FindPokemonInputDTO) -> dict:
        pokemon = output_dto.pokemon.to_dict()
        pokemon['weight'] = self.__convert_hectograms_to_pounds(output_dto.pokemon.weight)
        pokemon['height'] = self.__convert_decimeters_to_feet_and_inches(output_dto.pokemon.height)
        pokemon['category'] = self.__get_en_category(output_dto.pokemon.species)
        pokemon['abilities'] = self.__get_abilities(pokemon['abilities'])
        return pokemon

    def __convert_decimeters_to_feet_and_inches(self, decimeters: int) -> str:
        centimeters = decimeters * 10
        total_inches = centimeters / 2.54
        feet = int(total_inches // 12)
        inches = math.ceil(total_inches % 12)
        return f"{feet}' {inches:02}\""

    def __convert_hectograms_to_pounds(self, hectograms: int) -> float:
        return round(hectograms * 0.1 * 2.20462, 1)

    def __get_abilities(self, abilities: list[dict[str, str]]) -> list[str]:
        return [ability['ability']['name'] for ability in abilities if not ability['is_hidden']]

    def __get_en_category(self, species: dict[str, str]) -> str:
        category = ''
        for genus in species.get('genera', []):
            if genus.get('language', {}).get('name') == 'en':
                category = genus.get('genus').replace(' Pokémon', '')
                break
        return category
