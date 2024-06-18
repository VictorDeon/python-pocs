from pydantic import BaseModel, Field
from typing import Optional


class ListPokemonsInputDTO(BaseModel):
    """
    Dados de entrada para listar os pokemons
    """

    offset: Optional[int] = Field(None, description="Pular os N primeiros itens da lista.")
    limit: Optional[int] = Field(None, description="Quantidade limite de itens que irá aparecer na listagem.")

    def to_dict(self):
        """
        Transformar o objeto em dicionário.
        """

        return self.model_dump()


class PokemonOutput(BaseModel):
    """
    Dados do pokemon para listagem.
    """

    id: int = Field(..., description="Identificador único do pokemon na pokedex.")
    name: str = Field(..., description="Nome do pokemon.")
    sprite: Optional[str] = Field(None, description="Foto do pokemon.")
    types: Optional[str] = Field(None, description="Tipos do pokemon.")


class ListPokemonsOutputDTO(BaseModel):
    """
    Dados de saída para listar os pokemons
    """

    pokemons: list[PokemonOutput] = Field([], description="Lista de pokemons.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "pokemons": [
                    {
                        "id": 1,
                        "name": "bulbasaur",
                        "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                        "types": "grass, poison"
                    },
                    {
                        "id": 2,
                        "name": "ivysaur",
                        "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png",
                        "types": "grass, poison"
                    },
                    {
                        "id": 3,
                        "name": "venusaur",
                        "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/3.png",
                        "types": "grass, poison"
                    }
                ]
            },
        }
