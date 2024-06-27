from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class BaseModel(DeclarativeBase):
    """
    Model base para todas as outras models.
    """

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
