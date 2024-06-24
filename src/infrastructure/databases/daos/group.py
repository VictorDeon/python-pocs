import logging
from typing import Optional
from sqlalchemy import select, Select
from src.adapters.dtos import (
    CreateGroupInputDTO, ListGroupInputDTO,
    UpdateGroupInputDTO, RetrievePermissionInputDTO
)
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import Group, Permission, group_permission_many_to_many
from src.infrastructure.databases import DAOInterface
from .permission import PermissionDAO


class GroupDAO(DAOInterface):
    """
    Repositorio de manipulação da entidade de grupos
    """

    async def create(
        self,
        dto: CreateGroupInputDTO,
        commit: bool = True,
        close_session: bool = True) -> Group:
        """
        Cria o grupo passando como argumento os dados do mesmo.
        """

        group = Group(name=dto.name)
        permission_dao = PermissionDAO()

        with DBConnectionHandler.connect(close_session) as database:
            try:
                for permission_code in dto.permissions:
                    permission = await permission_dao.retrieve(
                        dto=RetrievePermissionInputDTO(code=permission_code),
                        close_session=False
                    )
                    if permission:
                        group.permissions.append(permission)

                database.session.add(group)
                if commit:
                    database.session.commit()
                    logging.info("Grupo inseridado no banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar o grupo: {e}")
                database.session.rollback()
                database.close_session(True)
                raise e

        return group

    async def list(self, dto: ListGroupInputDTO, close_session: bool = True) -> list[Group]:
        """
        Pega uma lista de grupos.
        """

        groups: list[Group] = []
        with DBConnectionHandler.connect(close_session) as database:
            statement: Select = select(Group)

            if dto:
                if dto.name and dto.code:
                    statement: Select = statement \
                        .join(group_permission_many_to_many) \
                        .join(Permission) \
                        .where(
                            Group.name.like(f"%{dto.name}%"),
                            Permission.code == dto.code
                        )
                elif dto.name:
                    statement: Select = statement.where(Group.name.like(f"%{dto.name}%"))
                elif dto.code:
                    statement: Select = statement \
                        .join(group_permission_many_to_many) \
                        .join(Permission) \
                        .where(Permission.code == dto.code)

            try:
                groups = database.session.scalars(statement=statement).all()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao listar os grupos: {e}")
                database.close_session(True)
                raise e

        return groups

    async def get_by_id(self, _id: int, close_session: bool = True) -> Optional[Group]:
        """
        Pega os dados de um grupo pelo _id
        """

        group: Group = None
        with DBConnectionHandler.connect(close_session) as database:
            try:
                group = database.session.get(Group, _id)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao pegar os dados do grupo: {e}")
                database.close_session(True)
                raise e

        return group

    async def update(
        self,
        _id: int,
        dto: UpdateGroupInputDTO,
        commit: bool = True,
        close_session: bool = True) -> Optional[Group]:
        """
        Pega os dados de um grupo pelo _id e atualiza
        """

        group: Group = None
        with DBConnectionHandler.connect(close_session) as database:
            statement = select(Group).where(Group.id == _id)
            permission_dao = PermissionDAO()

            try:
                group = database.session.scalars(statement).one()

                permissions: list[Permission] = []
                for permission_code in dto.permissions:
                    permission = await permission_dao.retrieve(
                        dto=RetrievePermissionInputDTO(code=permission_code),
                        close_session=False
                    )
                    permissions.append(permission)

                group.name = dto.name
                group.permissions = permissions
                if commit:
                    database.session.commit()
                    logging.info("Grupos atualizadas no banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao atualizar o grupo: {e}")
                database.session.rollback()
                database.close_session()
                raise e

        return group

    async def delete(
        self,
        _id: int,
        commit: bool = True,
        close_session: bool = True) -> None:
        """
        Pega os dados de um grupo pelo _id
        """

        with DBConnectionHandler.connect(close_session) as database:
            try:
                group = database.session.get(Group, _id)
                if not group:
                    raise ValueError(f"Grupo com o id {_id} não encontrado.")

                database.session.delete(group)
                if commit:
                    database.session.commit()
                    logging.info("Grupos deletadas do banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao deletar o grupo: {e}")
                database.session.rollback()
                database.close_session()
                raise e

    async def count(self, close_session: bool = True) -> int:
        """
        Pega a quantidade de grupos registrados no banco.
        """

        qtd: int = 0
        with DBConnectionHandler.connect(close_session) as database:
            try:
                qtd = database.session.query(Group).count()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao realizar a contagem de grupos: {e}")
                database.close_session()
                raise e

        return qtd
