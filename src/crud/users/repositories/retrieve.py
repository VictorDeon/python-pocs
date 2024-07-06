from typing import Optional
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from ..dtos import RetrieveUserInputDTO
from ..models import User


class RetrieveUserRepository:
    """
    Repositorio de manipulação da entidade de usuários
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def get_by_id(self, _id: int) -> Optional[User]:
        """
        Pega os dados de um usuário pelo _id
        """

        statement: Select = select(User).where(User.id == _id)
        try:
            user: User = await self.session.scalar(statement)
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao pegar os dados do usuário: {e}")
            raise e

        return user

    async def retrieve(self, dto: RetrieveUserInputDTO) -> Optional[User]:
        """
        Pega os dados de um usuário pelo email
        """

        statement: Select = select(User).where(User.email == dto.email)

        try:
            user: User = await self.session.scalar(statement)
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao pegar os dados do usuário: {e}")
            raise e

        return user
