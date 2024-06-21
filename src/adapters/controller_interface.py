from abc import ABC, abstractmethod
from typing import Any


class ControllerInterface(ABC):
    """
    Interface de controle.
    """

    @abstractmethod
    async def execute(self) -> Any:
        """
        Executa a controladora.
        """
