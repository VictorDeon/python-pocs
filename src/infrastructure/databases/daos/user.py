import logging
from src.adapters.dtos import (
    CreateUserInputDTO, RetrievePermissionInputDTO
)
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import User
from src.infrastructure.databases import DAOInterface
from src.infrastructure.databases.daos import PermissionDAO, GroupDAO, ProfileDAO


class UserDAO(DAOInterface):
    """
    Repositorio de manipulação da entidade de usuários
    """

    async def create(
        self,
        dto: CreateUserInputDTO,
        commit: bool = True,
        close_session: bool = True) -> User:
        """
        Cria o usuário passando como argumento os dados do mesmo.
        """

        user = User(
            name=dto.name,
            email=dto.email,
            password=dto.password
        )
        permission_dao = PermissionDAO()
        group_dao = GroupDAO()
        profile_dao = ProfileDAO()

        with DBConnectionHandler.connect(close_session) as database:
            try:
                profile = await profile_dao.create(
                    dto=dto.profile,
                    close_session=False
                )
                user.profile = profile

                # Criar a empresa principal

                for permission_code in dto.permissions:
                    permission = await permission_dao.retrieve(
                        dto=RetrievePermissionInputDTO(code=permission_code),
                        close_session=False
                    )
                    if permission:
                        user.permissions.append(permission)

                for group_id in dto.groups:
                    group = await group_dao.get_by_id(_id=group_id, close_session=False)
                    if group:
                        user.groups.append(group)

                database.session.add(user)
                if commit:
                    database.session.commit()
                    logging.info("Usuário inseridado no banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar o usuário: {e}")
                database.session.rollback()
                database.close_session(True)
                raise e

        return user
