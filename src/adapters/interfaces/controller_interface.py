from abc import ABC, abstractmethod


class ControllerInterface(ABC):
    @abstractmethod
    async def execute(self) -> dict:
        pass
