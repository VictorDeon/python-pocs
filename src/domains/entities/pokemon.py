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
