from pydantic import BaseModel, Field
from typing import Optional
from src.domains.entities.pokemon import Pokemon


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


class ListPokemonsOutputDTO(BaseModel):
    """
    Dados de saída para listar os pokemons
    """

    pokemons: list[Pokemon] = Field([], description="Lista de pokemons.")
