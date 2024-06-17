from fastapi import Response, Query
from src.adapters.controllers import ListPokemonController
from src.adapters.controllers import ListXMLPokemonController
from . import router


@router.get(
    "/pokemons",
    summary="Listar pokemons",
    tags=["Requests"],
    response_description="Lista de pokemons"
)
async def list_pokemons(
    limit: int = Query(None, description="Quantidade limite de itens que irá aparecer na listagem."),
    offset: int = Query(None, description="Pular os N primeiros itens da lista.")):
    """
    Endpoint para listar todos os pokemons.
    """

    controller = ListPokemonController(limit=limit, offset=offset)
    return await controller.execute()


@router.get(
    "/pokemons/xml",
    summary="List pokemons in XML",
    tags=["Requests"],
    response_description="List of pokemons in XML"
)
async def list_xml_pokemons(limit: int = None, offset: int = None):
    """
    Lista todos os pokemons no formato XML.
    """

    controller = ListXMLPokemonController()
    controller.get_search_params({"limit": limit, "offset": offset})
    xml_str = await controller.execute()
    headers = {
        "Content-Disposition": "attachment; filename=pokemons.xml",
        "Content-Type": "application/xml"
    }
    return Response(content=xml_str, media_type="application/xml", headers=headers)
