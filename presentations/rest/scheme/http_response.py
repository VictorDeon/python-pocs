from typing import Any


class HttpResponse:
    """
    Define a resposta da requisição http.
    """

    def __init__(self, content: Any, status_code: int) -> None:
        """
        Construtor.
        """

        self.status_code = status_code
        self.content = content
