from fastapi import Response, Query
from src.routes import router
from ..repositories import ListPokemonRepository, ListXMLPokemonRepository
from ..dtos import ListPokemonsOutputDTO


@router.get(
    "/pokemons",
    summary="Listar pokemons",
    tags=["Requests"],
    response_model=ListPokemonsOutputDTO,
    response_description="Lista de pokemons"
)
async def list_pokemons(
    limit: int = Query(None, description="Quantidade limite de itens que irá aparecer na listagem."),
    offset: int = Query(None, description="Pular os N primeiros itens da lista.")):
    """
    Endpoint para listar todos os pokemons.
    """

    controller = ListPokemonRepository(limit=limit, offset=offset)
    return await controller.execute()


@router.get(
    "/pokemons/xml",
    summary="Lista pokemons em XML",
    tags=["Requests"],
    response_model=ListPokemonsOutputDTO,
    response_description="Lista de pokemons em XML"
)
async def list_xml_pokemons(
    limit: int = Query(20, description="Quantidade limite de itens que irá aparecer na listagem."),
    offset: int = Query(0, description="Pular os N primeiros itens da lista.")):
    """
    Lista todos os pokemons no formato XML.
    """

    controller = ListXMLPokemonRepository(limit=limit, offset=offset)
    xml_str = await controller.execute()
    headers = {
        "Content-Disposition": "attachment; filename=pokemons.xml",
        "Content-Type": "application/xml"
    }
    return Response(content=xml_str, media_type="application/xml", headers=headers)
