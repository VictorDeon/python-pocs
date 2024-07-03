from pydantic import BaseModel, Field
from typing import Optional


class RetrievePokemonInputDTO(BaseModel):
    """
    Dados de entrada para encontrar um pokemon
    """

    id: int = Field(..., description="Identificador único do pokemon na pokedex.")


class PokemonOutput(BaseModel):
    """
    Dados de saída do pokemon.
    """

    id: int = Field(..., description="Identificador único do pokemon na pokedex.")
    name: str = Field(..., description="Nome do pokemon.")
    sprite: Optional[str] = Field(None, description="Foto do pokemon.")
    height: Optional[str] = Field(None, description="Altura do pokemon.")
    weight: Optional[float | int] = Field(None, description="Largura do pokemon.")
    types: Optional[str] = Field(None, description="Tipos do pokemon.")
    weaknesses: Optional[list[str]] = Field([], description="Fraqueza do pokemon.")
    strengths: Optional[list[str]] = Field([], description="Fortalizas do pokemon.")
    status: Optional[dict] = Field(None, description="Status do pokemon.")
    abilities: Optional[list[str]] = Field([], description="Habilidades do pokemon.")
    category: Optional[str] = Field(None, description="Espécie do pokemon.")


class RetrievePokemonOutputDTO(BaseModel):
    """
    Dados de saída para encontrar um pokemon
    """

    pokemon: PokemonOutput = Field(..., description="Dados do pokemon.")

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "pokemon": {
                    "id": 1,
                    "name": "bulbasaur",
                    "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                    "height": "2 feet 04 inches",
                    "weight": 15.2,
                    "types": "grass, poison",
                    "weaknesses": [
                        "psychic",
                        "ground",
                        "bug",
                        "ice",
                        "flying",
                        "poison",
                        "fire"
                    ],
                    "strengths": [
                        "ground",
                        "rock",
                        "water",
                        "fairy",
                        "grass"
                    ],
                    "status": {
                        "hp": 45,
                        "attack": 49,
                        "defense": 49,
                        "special-attack": 65,
                        "special-defense": 65,
                        "speed": 45
                    },
                    "abilities": [
                        "overgrow"
                    ],
                    "category": "Seed"
                }
            },
        }
