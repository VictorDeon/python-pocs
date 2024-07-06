from sqlalchemy import insert, Insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from src.crud.permissions.repositories import RetrievePermissionDAO
from src.crud.permissions.dtos import RetrievePermissionInputDTO
from ..dtos import CreateGroupInputDTO
from ..models import Group, GroupsVsPermissions


class CreateGroupDAO:
    """
    Repositorio de manipulação da entidade de grupos
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def execute(self, dto: CreateGroupInputDTO, commit: bool = True) -> Group:
        """
        Cria o grupo passando como argumento os dados do mesmo.
        """

        permission_dao = RetrievePermissionDAO(session=self.session)
        statement: Insert = insert(Group).values(name=dto.name).returning(Group)

        try:
            group: Group = await self.session.scalar(statement)

            for permission_code in dto.permissions:
                permission = await permission_dao.retrieve(
                    dto=RetrievePermissionInputDTO(code=permission_code)
                )
                if permission:
                    statement: Insert = insert(GroupsVsPermissions).values(
                        group_id=group.id,
                        permission_id=permission.id
                    )
                    await self.session.execute(statement)

            if commit:
                await self.session.commit()
                self.logger.info("Grupo atualizado no banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao criar o grupo: {e}")
            await self.session.rollback()
            raise e

        return group
