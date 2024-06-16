from fastapi import Response
from presentations.rest.controller import ControllerInterface
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

    def send(self, user_id: int) -> Response:
        """
        Lida com a entrada e saida dos dados.
        """

        if not user_id:
            raise ValueError("O user id é obrigatório.")

        response = self.__user_case.find(user_id)

        return Response(
            content=response,
            status_code=200
        )
