from src.domains.interfaces import UserRetrieveInterface
from src.infrastructure.databases.interfaces import UserDAOInterface


class UserRetrieve(UserRetrieveInterface):
    """
    Caso de uso de procura de um usuários.
    """

    def __init__(self, users_repository: UserDAOInterface) -> None:
        """
        Construtor.
        """

        self.__users_repository = users_repository

    async def find(self, _id: int) -> dict:
        """
        Encontra o usuário pelo email.
        """

        user = await self.__users_repository.retrieve(_id)

        return user.model_dump()
