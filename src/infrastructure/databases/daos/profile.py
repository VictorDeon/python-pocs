import logging
from typing import Optional
from sqlalchemy import select
from src.adapters.dtos import CreateProfileInputDTO, UpdateProfileInputDTO
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import Profile
from src.infrastructure.databases import DAOInterface


class ProfileDAO(DAOInterface):
    """
    Repositorio de manipulação da entidade de perfis
    """

    async def create(
        self,
        dto: CreateProfileInputDTO,
        commit: bool = True,
        close_session: bool = True) -> Profile:
        """
        Cria a perfil passando como argumento os seus dados.
        """

        profile = Profile(**dto.to_dict())

        with DBConnectionHandler.connect(close_session) as database:
            try:
                database.session.add(profile)
                if commit:
                    database.session.commit()
                    logging.info("Perfil inseridado no banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar o perfil: {e}")
                database.session.rollback()
                database.close_session(True)
                raise e

        return profile

    async def get_by_id(self, _id: int, close_session: bool = True) -> Optional[Profile]:
        """
        Pega os dados de uma perfil pelo _id
        """

        profile: Profile = None
        with DBConnectionHandler.connect(close_session) as database:
            try:
                profile = database.session.get(Profile, _id)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao pegar os dados do perfil: {e}")
                database.close_session(True)
                raise e

        return profile

    async def update(
        self,
        _id: int,
        dto: UpdateProfileInputDTO,
        commit: bool = True,
        close_session: bool = True) -> Optional[Profile]:
        """
        Pega os dados de um perfil pelo _id e atualiza
        """

        profile: Profile = None
        with DBConnectionHandler.connect(close_session) as database:
            statement = select(Profile).where(Profile.id == _id)

            try:
                profile = database.session.scalars(statement).one()
                profile.phone = dto.phone
                profile.address = dto.address
                if commit:
                    database.session.commit()
                    logging.info("Perfil atualizado no banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao atualizar o pefil: {e}")
                database.session.rollback()
                database.close_session()
                raise e

        return profile
