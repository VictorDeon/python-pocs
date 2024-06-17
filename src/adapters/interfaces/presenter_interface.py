from abc import ABC, abstractmethod
from typing import Any


class PresenterInterface(ABC):
    """
    Interface de saída das APIs.
    """

    @abstractmethod
    def present(self, output_dto: Any) -> dict:
        """
        Forma final de apresentação dos dados.
        """

        pass
