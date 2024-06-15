# pylint: disable=no-name-in-module
import pytest
from engines.db.mocks.user_repository import (
    UserRepositorySpy, UserRepositoryNotFoundRetrive
)
from domains.user_cases import UserRetrieve


def test_user_retrieve():
    """
    Testando o caso de uso de retorno do usuário.
    """

    repository = UserRepositorySpy()
    user_retrieve = UserRetrieve(users_repository=repository)
    response = user_retrieve.find(1)
    assert repository.retrieve_result.model_dump() == response


def test_user_retrieve_not_found():
    """
    Testando o caso de uso de retorno do usuário.
    """

    repository = UserRepositoryNotFoundRetrive()
    user_retrieve = UserRetrieve(users_repository=repository)

    with pytest.raises(ValueError) as e:
        user_retrieve.find(5)

    assert str(e.value) == "User not found"
