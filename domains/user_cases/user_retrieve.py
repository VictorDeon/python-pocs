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

    def __validate_params(self, email: str) -> None:
        """
        Valida os parâmetros de entrada.
        """

        if email == "invalido@gmail.com":
            raise ValueError(f"Email {email} inválido para a busca.")

    def find(self, email: str = None) -> dict:
        """
        Encontra o usuário pelo email.
        """

        self.__validate_params(email)

        users = self.__users_repository.list(email)

        if not users:
            raise ValueError(f"Usuários com email {email} não encontrado.")

        return {
            "qtd": len(users),
            "results": users
        }
