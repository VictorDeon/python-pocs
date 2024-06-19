from sqlalchemy import Column, BigInteger, Table, ForeignKey
from src.infrastructure.databases import BaseModel

user_group_many_to_many = Table(
    "users_vs_groups",
    BaseModel.metadata,
    Column("id_user", BigInteger, ForeignKey("users.id")),
    Column("id_group", BigInteger, ForeignKey("groups.id"))
)

user_permission_many_to_many = Table(
    "users_vs_permissions",
    BaseModel.metadata,
    Column("id_user", BigInteger, ForeignKey("users.id")),
    Column("id_permission", BigInteger, ForeignKey("permissions.id"))
)

group_permission_many_to_many = Table(
    "groups_vs_permissions",
    BaseModel.metadata,
    Column("id_group", BigInteger, ForeignKey("groups.id")),
    Column("id_permission", BigInteger, ForeignKey("permissions.id"))
)
