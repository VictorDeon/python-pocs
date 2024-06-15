# pylint: disable=missing-function-docstring
from abc import ABC, abstractmethod
from presentations.rest.scheme import HttpResponse, HttpRequest

class ControllerInterface(ABC):
    """
    Interface que irá controlar a camada de apresentação que irá interagir
    com os casos de uso.
    """

    @abstractmethod
    def handle(self, http_request: HttpRequest) -> HttpResponse: pass
