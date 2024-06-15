from typing import Callable
from fastapi import Request
from presentations.rest.scheme import HttpRequest, HttpResponse


async def fastapi_adapter(request: Request, handle_control: Callable) -> HttpResponse:
    """
    Adapta o framework para o nosso projeto.
    """

    try:
        body = await request.json()
    except Exception:
        body = None

    headers = {}
    for key, value in request.headers.items():
        headers[key] = value

    query = {}
    for key, value in request.query_params.items():
        query[key] = value

    http_request = HttpRequest(
        headers=headers,
        url=str(request.url),
        body=body,
        query=query,
        path=request.path_params
    )

    http_response = handle_control(http_request)
    return http_response
