from fastapi import Path
from src.application.api.routes import router
from src.adapters.controllers import RetrievePokemonController
from src.adapters.dtos import RetrievePokemonOutputDTO


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

    controller = RetrievePokemonController(pokemon_id)
    return await controller.execute()
