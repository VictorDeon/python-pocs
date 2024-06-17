from dataclasses import dataclass, asdict
from src.domains.entities.pokemon import Pokemon


@dataclass
class ListPokemonsInputDto:
    offset: int | None = None
    limit: int | None = None

    def to_dict(self):
        return asdict(self)


@dataclass
class ListPokemonsOutputDto:
    pokemons: list[Pokemon]
