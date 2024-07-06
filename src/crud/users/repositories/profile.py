from typing import Optional
from datetime import datetime
from sqlalchemy import (
    select, Select,
    insert, Insert,
    update as sql_update, Update
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from ..dtos import CreateProfileInputDTO, UpdateProfileInputDTO
from ..models import Profile


class ProfileDAO:
    """
    Repositorio de manipulação da entidade de perfis
    """

    def __init__(self, session: AsyncSession):
        """
        Contrutor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def create(self, user_id: int, dto: CreateProfileInputDTO, commit: bool = True) -> Profile:
        """
        Cria a perfil passando como argumento os seus dados.
        """

        statement: Insert = insert(Profile).values(
            **dto.to_dict(),
            user_id=user_id
        ).returning(Profile)

        try:
            profile: Profile = await self.session.scalar(statement)
            if commit:
                await self.session.commit()
                self.logger.info("Perfil inseridado no banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao criar o perfil: {e}")
            await self.session.rollback()
            raise e

        return profile

    async def get_by_id(self, user_id: int) -> Optional[Profile]:
        """
        Pega os dados de uma perfil pelo id do usuário dono do perfil
        """

        statement: Select = select(Profile).where(Profile.user_id == user_id)
        try:
            profile: Profile = await self.session.scalar(statement)
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao pegar os dados do perfil: {e}")
            raise e

        return profile

    async def update(self, user_id: int, dto: UpdateProfileInputDTO, commit: bool = True) -> Optional[Profile]:
        """
        Pega os dados de um perfil pelo _id e atualiza
        """

        statement: Update = sql_update(Profile).values(
            **dto.to_dict(), updated_at=datetime.now()
        ).where(Profile.user_id == user_id).returning(Profile)

        try:
            profile: Profile = await self.session.scalar(statement)
            if commit:
                await self.session.commit()
                self.logger.info("Perfil atualizado no banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao atualizar o pefil: {e}")
            await self.session.rollback()
            raise e

        return profile
