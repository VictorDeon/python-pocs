from pydantic import BaseModel, Field
from typing import Optional, Any


class Pokemon(BaseModel):
    """
    Entidade de pokemon.
    """

    id: int = Field(..., description="Identificador único do pokemon na pokedex.")
    name: str = Field(..., description="Nome do pokemon.")
    sprites: Optional[dict[str, Any]] = Field(None, description="Foto do pokemon.")
    height: Optional[int] = Field(None, description="Altura do pokemon.")
    weight: Optional[float | int] = Field(None, description="Largura do pokemon.")
    types: Optional[list[dict[str, Any]]] = Field(None, description="Tipo do pokemon.")
    weaknesses: Optional[list[str]] = Field(None, description="Fraqueza do pokemon.")
    strengths: Optional[list[str]] = Field([], description="Fortalizas do pokemon.")
    stats: Optional[list[dict[str, Any]]] = Field(None, description="Status do pokemon.")
    abilities: Optional[list[dict[str, Any]]] = Field(None, description="Habilidades do pokemon.")
    species: Optional[dict[str, Any]] = Field(None, description="Espécie do pokemon.")

    @classmethod
    def from_dict(cls, data: dict):
        """
        Transforma um dicionário em objeto.
        """

        return cls(**data)

    def to_dict(self) -> dict:
        """
        Transforma objeto em dicionário.
        """

        return self.model_dump()

    class Config:
        """
        Metadados da modelo
        """

        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "bulbasaur",
                "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                "height": 7,
                "weight": 69,
                "types": "grass, poison",
                "weaknesses": ["flying", "poison", "bug", "fire", "ice", "ground", "psychic"],
                "strengths": ["ground", "rock", "water", "grass", "fairy"],
                "abilities": ["overgrow", "chlorophyll"],
                "species": "Seed",
                "stats": [
                    {
                        "base_stat": 45,
                        "effort": 0,
                        "stat": {
                            "name": "hp",
                            "url": "https://pokeapi.co/api/v2/stat/1/"
                        }
                    },
                    {
                        "base_stat": 49,
                        "effort": 0,
                        "stat": {
                            "name": "attack",
                            "url": "https://pokeapi.co/api/v2/stat/2/"
                        }
                    },
                    {
                        "base_stat": 49,
                        "effort": 0,
                        "stat": {
                            "name": "defense",
                            "url": "https://pokeapi.co/api/v2/stat/3/"
                        }
                    },
                    {
                        "base_stat": 65,
                        "effort": 1,
                        "stat": {
                            "name": "special-attack",
                            "url": "https://pokeapi.co/api/v2/stat/4/"
                        }
                    },
                    {
                        "base_stat": 65,
                        "effort": 0,
                        "stat": {
                            "name": "special-defense",
                            "url": "https://pokeapi.co/api/v2/stat/5/"
                        }
                    },
                    {
                        "base_stat": 45,
                        "effort": 0,
                        "stat": {
                            "name": "speed",
                            "url": "https://pokeapi.co/api/v2/stat/6/"
                        }
                    }
                ]
            }
        }
