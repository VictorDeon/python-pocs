from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Any

T = TypeVar("T")

class PresenterInterface(Generic[T], metaclass=ABCMeta):
    """
    Interface de saída das APIs.
    """

    @abstractmethod
    def present(self, model: Any) -> Any:
        """
        Forma final de apresentação dos dados.
        """

        pass
