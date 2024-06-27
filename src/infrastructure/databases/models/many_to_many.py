from sqlalchemy import Column, BigInteger, Table, ForeignKey
from src.infrastructure.databases import BaseModel

users_vs_groups = Table(
    "users_vs_groups",
    BaseModel.metadata,
    Column("user_id", BigInteger, ForeignKey("users.id")),
    Column("group_id", BigInteger, ForeignKey("groups.id"))
)

users_vs_permissions = Table(
    "users_vs_permissions",
    BaseModel.metadata,
    Column("user_id", BigInteger, ForeignKey("users.id")),
    Column("permission_id", BigInteger, ForeignKey("permissions.id"))
)

groups_vs_permissions = Table(
    "groups_vs_permissions",
    BaseModel.metadata,
    Column("group_id", BigInteger, ForeignKey("groups.id")),
    Column("permission_id", BigInteger, ForeignKey("permissions.id"))
)
