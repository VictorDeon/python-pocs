from fastapi import Request
from .adapter import AdapterInterface
from presentations.rest.controller import ControllerInterface


class ApiAdapter(AdapterInterface):
    """
    Adaptador para comunicação via API Rest.
    """

    def receive(self, request: Request, controller: ControllerInterface):
        """
        Pega a mensagem e envia para a controladora correta.
        """

        return controller.handle(request)
