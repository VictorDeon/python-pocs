from fastapi import Path
from src.routes import router
from ..repositories import RetrievePokemonRepository
from ..dtos import RetrievePokemonOutputDTO


@router.get(
    "/pokemons/{pokemon_id}",
    tags=["Requests"],
    response_model=RetrievePokemonOutputDTO,
    summary="Pesquisar pokemon pelo ID"
)
async def retrieve_pokemon(pokemon_id: int = Path(..., description="Identificador do pokemon na pokedex.")):
    """
    Encontre um pokemon pelo seu ID.
    """

    controller = RetrievePokemonRepository(pokemon_id)
    return await controller.execute()
