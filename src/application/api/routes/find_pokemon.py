from fastapi import Path
from src.adapters.controllers import FindPokemonController
from src.adapters.dtos import FindPokemonOutputDTO
from . import router


@router.get(
    "/pokemons/{pokemon_id}",
    tags=["Requests"],
    response_model=FindPokemonOutputDTO,
    summary="Pesquisar pokemon pelo ID"
)
async def find_pokemon(pokemon_id: int = Path(..., description="Identificador do pokemon na pokedex.")):
    """
    Encontre um pokemon pelo seu ID.
    """

    controller = FindPokemonController(pokemon_id)
    return await controller.execute()
