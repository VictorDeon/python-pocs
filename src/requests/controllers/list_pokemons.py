from fastapi import Query, Header
from fastapi.responses import Response
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
    content_accept: str = Header(default="application/json", description="Tipo de conteúdo de retorno da requisição"),
    limit: int = Query(20, description="Quantidade limite de itens que irá aparecer na listagem."),
    offset: int = Query(0, description="Pular os N primeiros itens da lista.")):
    """
    Endpoint para listar todos os pokemons.
    """

    if content_accept == "application/xml":
        controller = ListXMLPokemonRepository(limit=limit, offset=offset)
        xml_str = await controller.execute()
        headers = {
            "Content-Disposition": "attachment; filename=pokemons.xml",
            "Content-Type": "application/xml"
        }
        return Response(content=xml_str, media_type="application/xml", headers=headers)
    else:
        controller = ListPokemonRepository(limit=limit, offset=offset)
        return await controller.execute()
