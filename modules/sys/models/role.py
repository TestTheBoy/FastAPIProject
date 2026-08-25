
from App_Demo.db_types import db_types
from pydantic import Field
from App_Demo.base import APIModel
from App_Demo.base import BaseOrmModel

from typing import Optional


# 数据库模型
class RoleOrmModel(BaseOrmModel):
    """
    角色数据库模型
    """
    __tablename__ = 'sys_role'
    
    # 如果数据库中不存在基类字段，则设置为None（不映射到数据库列）
    
    # SQLAlchemy字段定义
    appCode: str = db_types.Column(db_types.String(32), name="app_code", nullable=True, comment="应用编码")
    name: str = db_types.Column(db_types.String(64), name="name", nullable=False, comment="角色名称")
    code: str = db_types.Column(db_types.String(64), name="code", nullable=False, comment="唯一编码")
    sort: str = db_types.Column(db_types.BigInteger, name="sort", nullable=True, comment="排序")
    roleType: int = db_types.Column(db_types.Integer, name="role_type", nullable=False, comment="角色类型<sys_role_type>")
    enabled: int = db_types.Column(db_types.Integer, name="enabled", nullable=False, comment="是否启用")
    dataScope: int = db_types.Column(db_types.Integer, name="data_scope", nullable=True, comment="数据范围(1: 全部数据权限; 2: 自定义数据权限; 3: 本部门数据权限; 4: 本部门及以下部门权限; 5: 仅本人数据权限)")
    remark: str = db_types.Column(db_types.String(255), name="remark", nullable=True, comment="备注")

# Pydantic模型
class Role(APIModel):
    """
    角色Pydantic模型，用于API接口
    """
    # Pydantic字段定义
    appCode: Optional[str] = Field(None, description="应用编码")
    name: str = Field(None, description="角色名称")
    code: str = Field(None, description="唯一编码")
    sort: Optional[str] = Field(None, description="排序")
    roleType: int = Field(None, description="角色类型<sys_role_type>")
    enabled: int = Field(None, description="是否启用")
    dataScope: Optional[int] = Field(None, description="数据范围(1: 全部数据权限; 2: 自定义数据权限; 3: 本部门数据权限; 4: 本部门及以下部门权限; 5: 仅本人数据权限)")
    remark: Optional[str] = Field(None, description="备注")