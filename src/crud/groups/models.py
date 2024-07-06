from sqlalchemy import VARCHAR, BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.engines.databases import BaseModel


class Group(BaseModel):
    """
    Classe de grupos de usuários.
    """

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Group: {self.name}>"


class GroupsVsPermissions(BaseModel):
    """
    Relacionamento NxM entre grupos e permissões.
    """

    __tablename__ = "groups_vs_permissions"

    group_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('groups.id'), primary_key=True)
    permission_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('permissions.id'), primary_key=True)
