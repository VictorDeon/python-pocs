from datetime import datetime
from typing import Optional
from sqlalchemy import TIMESTAMP, BOOLEAN, func, false
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class BaseModel(DeclarativeBase):
    """
    Model base para todas as outras models.
    """

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
        index=True
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(
        BOOLEAN,
        server_default=false(),
        index=True
    )
