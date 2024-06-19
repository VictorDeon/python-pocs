from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.databases import BaseModel
from src.infrastructure.databases.models.__many_to_many import (
    user_group_many_to_many,
    user_permission_many_to_many
)
from .groups import Group
from .profiles import Profile
from .permissions import Permission


class User(BaseModel):
    """
    Classe de usuários.
    """

    __tablename__ = "users"
    __allow_unmapped__ = True

    id: int = Column(BigInteger, primary_key=True, autoincrement=True)
    email: str = Column(String(50), nullable=False, index=True, unique=True)
    password: str = Column(String(30), nullable=False)
    name: str = Column(String(30), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    updated_at: datetime = Column(DateTime, nullable=True)
    is_deleted: bool = Column(Boolean, default=False, index=True)

    profile_id = Column(BigInteger, ForeignKey('profiles.id'))
    profile: Profile = relationship(
        "Profile",
        uselist=False,
        backref='user'
    )

    groups: Optional[list[Group]] = relationship(
        "Group",
        secondary=user_group_many_to_many,
        backref='users',
        lazy='dynamic'
    )

    permissions: Optional[list[Permission]] = relationship(
        "Permission",
        secondary=user_permission_many_to_many,
        backref='users',
        lazy='dynamic'
    )


    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<User: {self.name}>"
