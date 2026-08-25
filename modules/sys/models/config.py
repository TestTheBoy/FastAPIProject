
from App_Demo.db_types import db_types
from pydantic import Field
from App_Demo.base import APIModel
from App_Demo.base import BaseOrmModel

from typing import Optional


# 数据库模型
class ConfigOrmModel(BaseOrmModel):
    """
    配置数据库模型
    """
    __tablename__ = 'sys_config'
    
    # 如果数据库中不存在基类字段，则设置为None（不映射到数据库列）
    
    # SQLAlchemy字段定义
    name: str = db_types.Column(db_types.String(64), name="name", nullable=False, comment="配置名称")
    code: str = db_types.Column(db_types.String(64), name="code", nullable=False, comment="唯一编码")
    groupCode: str = db_types.Column(db_types.String(64), name="group_code", nullable=False, comment="分组编码")
    content: str = db_types.Column(db_types.String(1000), name="content", nullable=True, comment="配置内容")
    isSys: int = db_types.Column(db_types.Integer, name="is_sys", nullable=True, comment="是否系统")
    enabled: int = db_types.Column(db_types.Integer, name="enabled", nullable=True, comment="是否启用")
    remark: str = db_types.Column(db_types.String(255), name="remark", nullable=True, comment="备注")

# Pydantic模型
class Config(APIModel):
    """
    配置Pydantic模型，用于API接口
    """
    # Pydantic字段定义
    name: str = Field(None, description="配置名称")
    code: str = Field(None, description="唯一编码")
    groupCode: str = Field(None, description="分组编码")
    content: Optional[str] = Field(None, description="配置内容")
    isSys: Optional[int] = Field(None, description="是否系统")
    enabled: Optional[int] = Field(None, description="是否启用")
    remark: Optional[str] = Field(None, description="备注")