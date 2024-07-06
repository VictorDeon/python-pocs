from sqlalchemy import select, Select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from src.crud.permissions.models import Permission
from src.crud.users.models import UsersVsGroups
from ..dtos import ListGroupInputDTO
from ..models import Group, GroupsVsPermissions


class ListGroupDAO:
    """
    Repositorio de manipulação da entidade de grupos
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def list(self, dto: ListGroupInputDTO) -> list[Group]:
        """
        Pega uma lista de grupos.
        """

        statement: Select = select(Group)

        if dto:
            if dto.user_id:
                statement: Select = statement \
                    .join(UsersVsGroups, UsersVsGroups.group_id == Group.id) \
                    .where(UsersVsGroups.user_id == dto.user_id)

            if dto.code:
                statement: Select = statement \
                    .join(GroupsVsPermissions, GroupsVsPermissions.group_id == Group.id) \
                    .join(Permission, Permission.id == GroupsVsPermissions.permission_id) \
                    .where(Permission.code == dto.code)

            if dto.name:
                statement: Select = statement.where(Group.name.like(f"%{dto.name}%"))

        try:
            result = await self.session.scalars(statement=statement)
            groups: list[Group] = result.all()
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao listar os grupos: {e}")
            raise e

        return groups

    async def count(self) -> int:
        """
        Pega a quantidade de grupos registrados no banco.
        """

        statement = select(func.count(Group.id))

        try:
            qtd = await self.session.scalar(statement)
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao realizar a contagem de grupos: {e}")
            raise e

        return qtd
