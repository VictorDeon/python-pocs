from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from sqlalchemy import select, Select, func
from src.crud.companies.models import Company
from src.crud.users.dtos import ListUserInputDTO
from src.crud.groups.models import Group
from ..models import User, UsersVsGroups


class ListUserRepository:
    """
    Repositorio de manipulação da entidade de usuários
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def list(self, dto: ListUserInputDTO) -> list[User]:
        """
        Pega uma lista de usuários.
        """

        statement: Select = select(User)

        if dto:
            if dto.work_company_cnpj:
                statement: Select = statement \
                    .join(Company, Company.cnpj == User.work_company_cnpj) \
                    .where(User.work_company_cnpj == dto.work_company_cnpj)

            if dto.group:
                statement: Select = statement \
                    .join(UsersVsGroups, UsersVsGroups.user_id == User.id) \
                    .join(Group, Group.id == UsersVsGroups.group_id) \
                    .where(Group.id == dto.group)

            if dto.name:
                statement: Select = statement.where(User.name.like(f"%{dto.name}%"))

            if dto.email:
                statement: Select = statement.where(User.email == dto.email)

        try:
            results = await self.session.scalars(statement=statement)
            users: list[User] = results.all()
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao listar os usuários: {e}")
            raise e

        return users

    async def count(self) -> int:
        """
        Pega a quantidade de usuários registradas no banco.
        """

        statement: Select = select(func.count(User.id))
        try:
            qtd: int = await self.session.scalar(statement)
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao realizar a contagem de usuários: {e}")
            raise e

        return qtd
