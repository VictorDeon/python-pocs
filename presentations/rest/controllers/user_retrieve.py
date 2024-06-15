from presentations.rest.interfaces import ControllerInterface
from presentations.rest.scheme import HttpResponse, HttpRequest
from domains.interfaces import UserRetrieveInterface


class UserRetrieveController(ControllerInterface):
    """
    Controladora de acesso externo para buscar os dados de uma API.
    """

    def __init__(self, user_case: UserRetrieveInterface) -> None:
        """
        Construtor
        """

        self.__user_case = user_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Lida com a entrada e saida dos dados.
        """

        user_id = http_request.path['user_id']

        response = self.__user_case.find(user_id)

        return HttpResponse(
            content=response,
            status_code=200
        )
