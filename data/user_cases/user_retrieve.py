from domains.interfaces import UserRetrieveInterface
from engines.db.interfaces import UserRepositoryInterface


class UserRetrieve(UserRetrieveInterface):
    """
    Caso de uso de procura de um usuários.
    """

    def __init__(self, users_repository: UserRepositoryInterface) -> None:
        """
        Construtor.
        """

        self.__users_repository = users_repository

    def find(self, email: str) -> dict:
        """
        Encontra o usuário pelo email.
        """
