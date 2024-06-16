# pylint: disable=missing-function-docstring
from typing import List
from abc import ABC, abstractmethod
from domains.models import User


class UserRepositoryInterface(ABC):
    """
    Interface de criação do repositorio de usuários.
    """

    @abstractmethod
    async def create(self, email: str, name: str, password: str) -> User: pass

    @abstractmethod
    async def retrieve(self, _id: int) -> User: pass

    @abstractmethod
    async def list(self, email: str = None) -> List[User]: pass
