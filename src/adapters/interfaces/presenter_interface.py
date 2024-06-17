from abc import ABC, abstractmethod
from typing import Any


class PresenterInterface(ABC):
    @abstractmethod
    def present(self, output_dto: Any) -> dict:
        pass
