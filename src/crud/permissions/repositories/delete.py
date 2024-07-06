from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from sqlalchemy import delete, Delete
from src.shared.exceptions import GenericException
from src.crud.users.models import UsersVsPermissions
from src.crud.groups.models import GroupsVsPermissions
from ..models import Permission


class DeletePermissionDAO:
    """
    Repositorio de manipulação da entidade de permissão
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def execute(self, _id: int, commit: bool = True) -> int:
        """
        Pega os dados de uma permissão pelo _id e deleta
        """

        try:
            statement: Delete = delete(UsersVsPermissions).where(UsersVsPermissions.permission_id == _id)
            await self.session.execute(statement)

            statement: Delete = delete(GroupsVsPermissions).where(GroupsVsPermissions.permission_id == _id)
            await self.session.execute(statement)

            statement: Delete = delete(Permission).where(Permission.id == _id).returning(Permission.id)

            permission_id: int = await self.session.scalar(statement)
            if not permission_id:
                raise GenericException(f"Permissão com id {_id} não encontrado.")

            if commit:
                await self.session.commit()
                self.logger.info("Permissões deletadas do banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao deletar a permissão: {e}")
            await self.session.rollback()
            raise e

        return permission_id
