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

    def __validate_params(self, _id: int) -> None:
        """
        Valida os parâmetros de entrada.
        """

        if not _id:
            raise ValueError("Identificador inválido para a busca.")

    def find(self, _id: int) -> dict:
        """
        Encontra o usuário pelo email.
        """

        self.__validate_params(_id)

        user = self.__users_repository.retrieve(_id)

        return user.model_dump()
