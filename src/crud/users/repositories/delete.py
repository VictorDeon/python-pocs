from sqlalchemy import delete, Delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from ..models import User, UsersVsPermissions, UsersVsGroups


class DeleteUserRepository:
    """
    Repositorio de manipulação da entidade de usuários
    """

    def __init__(self, session: AsyncSession):
        """
        Contrutor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def execute(self, _id: int, commit: bool = True) -> int:
        """
        Pega os dados de um usuário pelo _id e deleta o usuário,
        suas empresas que é dona e seu perfil.
        """

        try:
            statement: Delete = delete(UsersVsGroups).where(UsersVsGroups.user_id == _id)
            await self.session.execute(statement)

            statement: Delete = delete(UsersVsPermissions).where(UsersVsPermissions.user_id == _id)
            await self.session.execute(statement)

            statement: Delete = delete(User).where(User.id == _id).returning(User.id)

            user_id: int = await self.session.scalar(statement)
            if not user_id:
                raise ValueError(f"Usuário com o id {_id} não encontrado.")

            if commit:
                await self.session.commit()
                self.logger.info("Usuário deletado do banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao deletar o usuário: {e}")
            await self.session.rollback()
            raise e

        return user_id
