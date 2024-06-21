from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic

MODEL = TypeVar("MODEL")
OUTPUT = TypeVar("OUTPUT")


class PresenterInterface(Generic[MODEL, OUTPUT], metaclass=ABCMeta):
    """
    Interface de saída das APIs.
    """

    @abstractmethod
    def present(self, model: MODEL) -> OUTPUT:
        """
        Forma final de apresentação dos dados.
        """
