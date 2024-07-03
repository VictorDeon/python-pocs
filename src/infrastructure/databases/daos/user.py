import logging
import os
from typing import Optional
from datetime import datetime
from sqlalchemy import (
    select, Select, func,
    insert, Insert,
    delete as sql_delete, Delete,
    update as sql_update, Update
)
from src.adapters.dtos import (
    CreateUserInputDTO, RetrievePermissionInputDTO, ListUserInputDTO,
    RetrieveUserInputDTO, UpdateUserInputDTO
)
from src.domains.utils.exceptions import GenericException
from src.infrastructure.databases.models import (
    User, UsersVsPermissions, UsersVsGroups, Company, Group, Profile
)
from src.infrastructure.databases import DAOInterface
from .permission import PermissionDAO
from .company import CompanyDAO
from .group import GroupDAO
from .profile import ProfileDAO


class UserDAO(DAOInterface):
    """
    Repositorio de manipulação da entidade de usuários
    """

    async def create(self, dto: CreateUserInputDTO, commit: bool = True) -> User:
        """
        Cria o usuário passando como argumento os dados do mesmo.
        """

        permission_dao = PermissionDAO(session=self.session)
        group_dao = GroupDAO(session=self.session)
        profile_dao = ProfileDAO(session=self.session)
        company_dao = CompanyDAO(session=self.session)

        try:
            if dto.work_company_cnpj:
                work_company = await company_dao.get_by_cnpj(cnpj=dto.work_company_cnpj)
                if not work_company:
                    raise GenericException(f"Empresa com cnpj {dto.work_company_cnpj} não encontrado.")

            statement: Insert = insert(User).values(
                name=dto.name,
                email=dto.email,
                password=dto.password,
                work_company_cnpj=dto.work_company_cnpj
            ).returning(User)
            user: User = await self.session.scalar(statement)

            await profile_dao.create(user_id=user.id, dto=dto.profile)

            for permission_code in dto.permissions:
                permission = await permission_dao.retrieve(
                    dto=RetrievePermissionInputDTO(code=permission_code)
                )
                if permission:
                    statement: Insert = insert(UsersVsPermissions).values(
                        user_id=user.id,
                        permission_id=permission.id
                    )
                    await self.session.execute(statement)

            for group_id in dto.groups:
                group = await group_dao.get_by_id(_id=group_id)
                if group:
                    statement: Insert = insert(UsersVsGroups).values(
                        user_id=user.id,
                        group_id=group.id
                    )
                    await self.session.execute(statement)

            if commit:
                await self.session.commit()
                logging.info("Usuário inseridado no banco.")
        except Exception as e:
            logging.error(f"Ocorreu um problema ao criar o usuário: {e}")
            await self.session.rollback()
            raise e

        return user

    async def list(self, dto: ListUserInputDTO) -> list[User]:
        """
        Pega uma lista de usuários.
        """

        statement: Select = select(User)

        if dto:
            if dto.work_company_cnpj:
                statement: Select = statement \
                    .join(Company, Company.cnpj == User.work_company_cnpj) \
                    .where(User.work_company_cnpj == dto.work_company_cnpj)

            if dto.group:
                statement: Select = statement \
                    .join(UsersVsGroups, UsersVsGroups.user_id == User.id) \
                    .join(Group, Group.id == UsersVsGroups.group_id) \
                    .where(Group.id == dto.group)

            if dto.name:
                statement: Select = statement.where(User.name.like(f"%{dto.name}%"))

            if dto.email:
                statement: Select = statement.where(User.email == dto.email)

        try:
            results = await self.session.scalars(statement=statement)
            users: list[User] = results.all()
        except Exception as e:
            logging.error(f"Ocorreu um problema ao listar os usuários: {e}")
            raise e

        return users

    async def get_by_id(self, _id: int) -> Optional[User]:
        """
        Pega os dados de um usuário pelo _id
        """

        statement: Select = select(User).where(User.id == _id)
        try:
            user: User = await self.session.scalar(statement)
        except Exception as e:
            logging.error(f"Ocorreu um problema ao pegar os dados do usuário: {e}")
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
            logging.error(f"Ocorreu um problema ao pegar os dados do usuário: {e}")
            raise e

        return user

    async def update(self, _id: int, dto: UpdateUserInputDTO, commit: bool = True) -> Optional[User]:
        """
        Pega os dados de um usuário pelo _id e atualiza
        """

        try:
            if dto.work_company_cnpj:
                company_dao = CompanyDAO(session=self.session)
                company: Company = await company_dao.get_by_cnpj(cnpj=dto.work_company_cnpj)
                if not company:
                    raise GenericException(f"Empresa com cnpj {dto.work_company_cnpj} não encontrado.")

            statement: Update = sql_update(User).values(
                name=dto.name,
                email=dto.email,
                updated_at=datetime.now(),
                work_company_cnpj=dto.work_company_cnpj
            ).where(User.id == _id).returning(User)

            user: User = await self.session.scalar(statement)
            if not user:
                raise GenericException(f"Usuário com id {_id} não encontrado.")

            if dto.profile:
                profile_dao = ProfileDAO(session=self.session)
                await profile_dao.update(
                    user_id=user.id,
                    dto=dto.profile
                )

            if dto.permissions is not None:
                permission_dao = PermissionDAO(session=self.session)
                statement: Delete = sql_delete(UsersVsPermissions).where(UsersVsPermissions.user_id == user.id)
                await self.session.execute(statement)

                for permission_code in dto.permissions:
                    permission = await permission_dao.retrieve(
                        dto=RetrievePermissionInputDTO(code=permission_code)
                    )
                    if permission:
                        statement: Update = insert(UsersVsPermissions).values(
                            user_id=user.id,
                            permission_id=permission.id
                        )
                        await self.session.execute(statement)

            if dto.groups is not None:
                group_dao = GroupDAO(session=self.session)
                statement: Delete = sql_delete(UsersVsGroups).where(UsersVsGroups.user_id == user.id)
                await self.session.execute(statement)

                for group_id in dto.groups:
                    group = await group_dao.get_by_id(_id=group_id)
                    if group:
                        statement: Update = insert(UsersVsGroups).values(
                            user_id=user.id,
                            group_id=group.id
                        )
                        await self.session.execute(statement)

            if commit:
                await self.session.commit()
                logging.info("Usuário atualizado no banco.")
        except Exception as e:
            logging.error(f"Ocorreu um problema ao atualizar o usuário: {e}")
            await self.session.rollback()
            raise e

        return user

    async def delete(self, _id: int, commit: bool = True) -> int:
        """
        Pega os dados de um usuário pelo _id e deleta o usuário,
        suas empresas que é dona e seu perfil.
        """

        try:
            statement: Delete = sql_delete(UsersVsGroups).where(UsersVsGroups.user_id == _id)
            await self.session.execute(statement)

            statement: Delete = sql_delete(UsersVsPermissions).where(UsersVsPermissions.user_id == _id)
            await self.session.execute(statement)

            if os.environ.get("APP_ENV") == "tests":
                statement: Delete = sql_delete(User).where(User.id == _id).returning(User.id)
            else:
                statement: Update = sql_update(Profile).values(is_deleted=True).where(Profile.user_id == _id)
                await self.session.execute(statement)
                statement: Update = sql_update(Company).values(is_deleted=True).where(Company.owner_id == _id)
                await self.session.execute(statement)
                statement: Update = sql_update(User).values(is_deleted=True).where(User.id == _id).returning(User.id)

            user_id: int = await self.session.scalar(statement)
            if not user_id:
                raise ValueError(f"Usuário com o id {_id} não encontrado.")

            if commit:
                await self.session.commit()
                logging.info("Usuário deletado do banco.")
        except Exception as e:
            logging.error(f"Ocorreu um problema ao deletar o usuário: {e}")
            await self.session.rollback()
            raise e

        return user_id

    async def count(self) -> int:
        """
        Pega a quantidade de usuários registradas no banco.
        """

        statement: Select = select(func.count(User.id))
        try:
            qtd: int = await self.session.scalar(statement)
        except Exception as e:
            logging.error(f"Ocorreu um problema ao realizar a contagem de usuários: {e}")
            raise e

        return qtd
