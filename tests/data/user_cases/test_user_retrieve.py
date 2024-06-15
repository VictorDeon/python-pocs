#pylint: disable=no-name-in-module
from engines.db.repositories import UserRepository
from data.user_cases import UserRetrieve


def test_user_retrieve():
    """
    Testando o caso de uso de retorno do usuário.
    """

    repository = UserRepository()
    user_retrieve = UserRetrieve(users_repository=repository)
    print(user_retrieve)
