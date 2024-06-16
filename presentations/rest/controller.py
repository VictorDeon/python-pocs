# pylint: disable=missing-function-docstring
from abc import ABC, abstractmethod
from fastapi import Request, Response


class ControllerInterface(ABC):
    """
    Interface que irá controlar a camada de apresentação que irá interagir
    com os casos de uso.
    """

    @abstractmethod
    def receive(self, request: Request) -> Response: pass
