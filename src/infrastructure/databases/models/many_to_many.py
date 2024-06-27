from sqlalchemy import Column, BIGINT, Table, ForeignKey
from src.infrastructure.databases import BaseModel


users_vs_groups = Table(
    "users_vs_groups",
    BaseModel.metadata,
    Column("user_id", BIGINT, ForeignKey("users.id")),
    Column("group_id", BIGINT, ForeignKey("groups.id"))
)

users_vs_permissions = Table(
    "users_vs_permissions",
    BaseModel.metadata,
    Column("user_id", BIGINT, ForeignKey("users.id")),
    Column("permission_id", BIGINT, ForeignKey("permissions.id"))
)

groups_vs_permissions = Table(
    "groups_vs_permissions",
    BaseModel.metadata,
    Column("group_id", BIGINT, ForeignKey("groups.id")),
    Column("permission_id", BIGINT, ForeignKey("permissions.id"))
)
