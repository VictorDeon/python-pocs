from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from sqlalchemy import select, Select, func
from ..dtos import ListPermissionInputDTO
from ..models import Permission
from src.crud.groups.models import GroupsVsPermissions
from src.crud.users.models import UsersVsPermissions


class ListPermissionDAO:
    """
    Repositorio de manipulação da entidade de permissão
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def list(self, dto: ListPermissionInputDTO) -> list[Permission]:
        """
        Pega uma lista de objetos.
        """

        statement: Select = select(Permission)

        if dto:
            if dto.group_id:
                statement: Select = statement \
                    .join(GroupsVsPermissions, GroupsVsPermissions.permission_id == Permission.id) \
                    .where(GroupsVsPermissions.group_id == dto.group_id)

            if dto.user_id:
                statement: Select = statement \
                    .join(UsersVsPermissions, UsersVsPermissions.permission_id == Permission.id) \
                    .where(UsersVsPermissions.user_id == dto.user_id)

            if dto.name:
                statement: Select = statement.where(Permission.name.like(f"%{dto.name}%"))

            if dto.code:
                statement: Select = statement.where(Permission.code == dto.code)

        try:
            result = await self.session.scalars(statement=statement)
            permissions: list[Permission] = result.all()
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao listar as permissões: {e}")
            raise e

        return permissions

    async def count(self) -> int:
        """
        Pega a quantidade de permissões registradas no banco.
        """

        statement = select(func.count(Permission.id))
        try:
            qtd: int = await self.session.scalar(statement)
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao realizar a contagem de permissões: {e}")
            raise e

        return qtd
