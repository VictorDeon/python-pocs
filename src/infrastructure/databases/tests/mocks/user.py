# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from typing import List
from copy import deepcopy
from faker import Faker
from src.domains.entities import User

faker = Faker()


class UserDAOSpy:
    def __init__(self) -> None:
        self.create_result: User = None
        self.retrieve_result: User = None
        self.list_results: List[User] = []

    def create(self, email: str, name: str, _: str) -> User:
        user = User(
            id=faker.random_number(digits=3),
            name=name,
            email=email
        )
        self.create_result = deepcopy(user)
        return user

    def retrieve(self, _id: int) -> User:
        user = User(
            id=_id,
            name=faker.name(),
            email=faker.email()
        )
        self.retrieve_result = deepcopy(user)
        return user

    def list(self, _: int = None) -> List[User]:
        users = []

        for i in range(10):
            user = User(
                id=i,
                name=faker.name(),
                email=faker.email()
            )
            self.list_results.append(user)
            users.append(user)

        self.list_results.sort(key=lambda user: user.id)
        users.sort(key=lambda user: user.id)

        return users


class UserDAONotFoundRetrive(UserDAOSpy):
    def retrieve(self, _: int) -> User:
        raise ValueError("User not found")


class UserDAOEmailFilterListSpy(UserDAOSpy):
    def list(self, email: int = None) -> List[User]:
        users = []

        for i in range(3):
            user = User(
                id=i,
                name=faker.name(),
                email=email
            )
            self.list_results.append(user)
            users.append(user)

        self.list_results.sort(key=lambda user: user.id)
        users.sort(key=lambda user: user.id)

        return users


class UserDAOEmptyListSpy(UserDAOSpy):
    def list(self, _: str = None) -> List[User]:
        return []
