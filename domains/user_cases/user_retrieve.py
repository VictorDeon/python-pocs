from abc import ABC, abstractmethod


class UserRetrieveInterface(ABC):
    """
    Interface de implementação relacionado ao caso de uso de procura de um usuários.
    """

    @abstractmethod
    def find(self, email: str) -> dict:
        """
        Encontra o usuário pelo email.
        """
