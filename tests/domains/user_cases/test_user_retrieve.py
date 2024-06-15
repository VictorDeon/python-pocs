#pylint: disable=no-name-in-module
from engines.db.mocks import UserRepositorySpy
from domains.user_cases import UserRetrieve


def test_user_retrieve():
    """
    Testando o caso de uso de retorno do usuário.
    """

    repository = UserRepositorySpy()
    user_retrieve = UserRetrieve(users_repository=repository)
    response = user_retrieve.find()
    assert response['qtd'] == len(response['results'])
    assert repository.list_results == response['results']
