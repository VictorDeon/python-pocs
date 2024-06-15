from engines.db.repositories import UserRepository
from domains.user_cases import UserRetrieve
from presentations.rest.controllers import UserRetrieveController


def user_retriever_compose():
    """
    Método que junta tudo relacionado a busca de usuário.
    """

    repository = UserRepository()
    user_case = UserRetrieve(users_repository=repository)
    controller = UserRetrieveController(user_case=user_case)
    return controller.handle
