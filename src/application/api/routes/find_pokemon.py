from fastapi import Path
from src.adapters.controllers import FindPokemonController
from src.application.api.routes import router


@router.get(
    "/pokemons/{pokemon_id}",
    tags=["Requests"],
    summary="Pesquisar pokemon pelo ID"
)
async def find_pokemon(pokemon_id: int = Path(..., description="Identificador do pokemon na pokedex.")):
    """
    Encontre um pokemon pelo seu ID.
    """

    controller = FindPokemonController(pokemon_id)
    return await controller.execute()
