from App_Demo.db_types import db_types
from pydantic import Field
from App_Demo.base import APIModel
from App_Demo.base import BaseOrmModel


# 数据库模型
class UserRoleOrmModel(BaseOrmModel):
    """
    r_用户角色关系数据库模型
    """
    __tablename__ = 'sys_user_role'

    # 如果数据库中不存在基类字段，则设置为None（不映射到数据库列）
    createTime = None
    updateTime = None
    createUser = None
    updateUser = None
    isDeleted = None

    # SQLAlchemy字段定义
    userId: str = db_types.Column(db_types.BigInteger, name="user_id", nullable=False, comment="用户ID")
    roleId: str = db_types.Column(db_types.BigInteger, name="role_id", nullable=False, comment="角色ID")


# Pydantic模型
class UserRole(APIModel):
    """
    r_用户角色关系Pydantic模型，用于API接口
    """
    # Pydantic字段定义
    userId: str = Field(None, description="用户ID")
    roleId: str = Field(None, description="角色ID")