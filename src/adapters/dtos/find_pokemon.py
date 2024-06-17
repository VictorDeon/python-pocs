from pydantic import BaseModel, Field
from src.domains.entities import Pokemon


class FindPokemonInputDTO(BaseModel):
    """
    Dados de entrada para encontrar um pokemon
    """

    id: int = Field(..., description="Identificador único do pokemon na pokedex.")

    def to_dict(self):
        """
        Transforma os dados em dicionário.
        """

        return self.model_dump()


class FindPokemonOutputDTO(BaseModel):
    """
    Dados de saída para encontrar um pokemon
    """

    pokemon: Pokemon = Field(..., description="Dados do pokemon.")
