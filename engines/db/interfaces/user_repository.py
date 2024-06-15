#pylint: disable=missing-function-docstring
from typing import List
from abc import ABC, abstractmethod
from domains.models import User


class UserRepositoryInterface(ABC):
    """
    Interface de criação do repositorio de usuários.
    """

    @abstractmethod
    def create(self, *args, **kwargs) -> User: pass

    @abstractmethod
    def retrieve(self, *args, **kwargs) -> User: pass

    @abstractmethod
    def list(self, *args, **kwargs) -> List[User]: pass

    @abstractmethod
    def update(self, *args, **kwargs) -> User: pass

    @abstractmethod
    def delete(self, *args, **kwargs) -> None: pass
