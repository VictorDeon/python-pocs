from abc import ABC, abstractmethod
from main.input_mediator import InputAdapterMediator
from typing import Any


class AdapterInterface(ABC):
    """
    Interface para padronizar as formas de comunicação de entrada e saída.
    """

    def __init__(self, mediator: InputAdapterMediator) -> None:
        """
        Recebe o mediador da comunicação
        """

        self.mediator = mediator

    def send(self, *args, **kwargs) -> Any:
        """
        Envia a mensagem ao recebedor.
        """

        self.mediator.send(self, *args, **kwargs)

    @abstractmethod
    def receive(self, *args, **kwargs) -> Any:
        """
        Recebe a mensagem de resposta.
        """

        pass
