
from App_Demo.db_types import db_types
from pydantic import Field
from App_Demo.base import APIModel
from App_Demo.base import BaseOrmModel

from typing import Optional


# 数据库模型
class DictOrmModel(BaseOrmModel):
    """
    字典数据库模型
    """
    __tablename__ = 'sys_dict'
    
    # 如果数据库中不存在基类字段，则设置为None（不映射到数据库列）
    
    # SQLAlchemy字段定义
    name: str = db_types.Column(db_types.String(64), name="name", nullable=False, comment="字典名称")
    code: str = db_types.Column(db_types.String(64), name="code", nullable=False, comment="唯一编码")
    groupCode: str = db_types.Column(db_types.String(64), name="group_code", nullable=False, comment="分组编码")
    sort: str = db_types.Column(db_types.BigInteger, name="sort", nullable=True, comment="排序")
    enabled: int = db_types.Column(db_types.Integer, name="enabled", nullable=True, comment="是否启用")
    dataType: int = db_types.Column(db_types.Integer, name="data_type", nullable=True, comment="数据类型（1：字符串；2：整型）")
    remark: str = db_types.Column(db_types.String(255), name="remark", nullable=True, comment="备注")

# Pydantic模型
class Dict(APIModel):
    """
    字典Pydantic模型，用于API接口
    """
    # Pydantic字段定义
    name: str = Field(None, description="字典名称")
    code: str = Field(None, description="唯一编码")
    groupCode: str = Field(None, description="分组编码")
    sort: Optional[str] = Field(None, description="排序")
    enabled: Optional[int] = Field(None, description="是否启用")
    dataType: Optional[int] = Field(None, description="数据类型（1：字符串；2：整型）")
    remark: Optional[str] = Field(None, description="备注")