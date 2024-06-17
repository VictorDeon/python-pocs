from fastapi import APIRouter
from src.adapters.controllers import FindPokemonController

router = APIRouter()


@router.get("/pokemons/{pokemon_id}", summary="Find a pokemon by id")
async def find_pokemon(pokemon_id: int):
    """
    Encontre um pokemon pelo seu ID.
    """

    controller = FindPokemonController()
    controller.get_pokemon_id({"id": pokemon_id})
    return await controller.execute()
