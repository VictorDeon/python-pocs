# pylint: disable=missing-function-docstring
from abc import ABC, abstractmethod
from fastapi import Response


class ControllerInterface(ABC):
    """
    Interface que irá controlar a camada de apresentação que irá interagir
    com os casos de uso.
    """

    @abstractmethod
    async def send(self, *args, **kwargs) -> Response:
        """
        Lida com a entrada e da uma saida.
        """

        pass
