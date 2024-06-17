from abc import ABC, abstractmethod


class ControllerInterface(ABC):
    @abstractmethod
    def execute(self) -> dict:
        pass
