
from App_Demo.db_types import db_types
from pydantic import Field
from App_Demo.base import APIModel
from App_Demo.base import BaseOrmModel

from typing import Optional


# 数据库模型
class DeptOrmModel(BaseOrmModel):
    """
    部门数据库模型
    """
    __tablename__ = 'sys_dept'
    
    # 如果数据库中不存在基类字段，则设置为None（不映射到数据库列）
    
    # SQLAlchemy字段定义
    parentId: str = db_types.Column(db_types.BigInteger, name="parent_id", nullable=True, comment="父ID")
    pids: str = db_types.Column(db_types.String(255), name="pids", nullable=True, comment="父ID集合")
    name: str = db_types.Column(db_types.String(64), name="name", nullable=False, comment="部门名称")
    code: str = db_types.Column(db_types.String(64), name="code", nullable=False, comment="唯一编码")
    sort: str = db_types.Column(db_types.BigInteger, name="sort", nullable=True, comment="排序")
    enabled: int = db_types.Column(db_types.Integer, name="enabled", nullable=True, comment="是否启用")
    leaderIds: str = db_types.Column(db_types.String(255), name="leader_ids", nullable=True, comment="部门负责人ID集合")
    mainLeaderId: str = db_types.Column(db_types.BigInteger, name="main_leader_id", nullable=True, comment="分管领导ID")
    remark: str = db_types.Column(db_types.String(255), name="remark", nullable=True, comment="备注")

# Pydantic模型
class Dept(APIModel):
    """
    部门Pydantic模型，用于API接口
    """
    # Pydantic字段定义
    parentId: Optional[str] = Field(None, description="父ID")
    pids: Optional[str] = Field(None, description="父ID集合")
    name: str = Field(None, description="部门名称")
    code: str = Field(None, description="唯一编码")
    sort: Optional[str] = Field(None, description="排序")
    enabled: Optional[int] = Field(None, description="是否启用")
    leaderIds: Optional[str] = Field(None, description="部门负责人ID集合")
    mainLeaderId: Optional[str] = Field(None, description="分管领导ID")
    remark: Optional[str] = Field(None, description="备注")