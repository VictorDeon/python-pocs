from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Any

T = TypeVar("T")


class ControllerInterface(Generic[T], metaclass=ABCMeta):
    """
    Interface de controle.
    """

    @abstractmethod
    async def execute(self) -> Any:
        pass
