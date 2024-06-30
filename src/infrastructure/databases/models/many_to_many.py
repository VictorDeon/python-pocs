from sqlalchemy import ForeignKey, Table, Column, BIGINT
from src.infrastructure.databases import BaseModel

UserVsGroup = Table(
    'users_vs_groups',
    BaseModel.metadata,
    Column('user_id', BIGINT, ForeignKey('users.id')),
    Column('group_id', BIGINT, ForeignKey('groups.id'))
)

UserVsPermission = Table(
    'users_vs_permissions',
    BaseModel.metadata,
    Column('user_id', BIGINT, ForeignKey('users.id')),
    Column('permission_id', BIGINT, ForeignKey('permissions.id'))
)

GroupVsPermission = Table(
    'groups_vs_permissions',
    BaseModel.metadata,
    Column('group_id', BIGINT, ForeignKey('groups.id')),
    Column('permission_id', BIGINT, ForeignKey('permissions.id'))
)
