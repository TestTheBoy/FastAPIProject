
from App_Demo.db_types import db_types
from pydantic import Field
from App_Demo.base import APIModel
from App_Demo.base import BaseOrmModel

from typing import Optional


# 数据库模型
class MenuOrmModel(BaseOrmModel):
    """
    菜单数据库模型
    """
    __tablename__ = 'sys_menu'
    
    # 如果数据库中不存在基类字段，则设置为None（不映射到数据库列）
    
    # SQLAlchemy字段定义
    appCode: str = db_types.Column(db_types.String(32), name="app_code", nullable=True, comment="应用编码")
    parentId: str = db_types.Column(db_types.BigInteger, name="parent_id", nullable=False, comment="父ID")
    name: str = db_types.Column(db_types.String(64), name="name", nullable=False, comment="菜单名称")
    code: str = db_types.Column(db_types.String(64), name="code", nullable=False, comment="唯一编码")
    pids: str = db_types.Column(db_types.String(255), name="pids", nullable=True, comment="父ID集合")
    type: int = db_types.Column(db_types.Integer, name="type", nullable=True, comment="菜单类型<sys_menu_type>")
    sort: str = db_types.Column(db_types.BigInteger, name="sort", nullable=True, comment="排序")
    path: str = db_types.Column(db_types.String(100), name="path", nullable=True, comment="路由地址")
    component: str = db_types.Column(db_types.String(100), name="component", nullable=True, comment="组件地址")
    icon: str = db_types.Column(db_types.String(100), name="icon", nullable=True, comment="菜单图标")
    isShow: int = db_types.Column(db_types.Integer, name="is_show", nullable=True, comment="是否显示")
    isLink: int = db_types.Column(db_types.Integer, name="is_link", nullable=True, comment="是否链接")
    url: str = db_types.Column(db_types.String(255), name="url", nullable=True, comment="外部链接地址")
    enabled: int = db_types.Column(db_types.Integer, name="enabled", nullable=True, comment="是否启用")
    openType: int = db_types.Column(db_types.Integer, name="open_type", nullable=True, comment="打开方式<sys_menu_open_type>")
    isCache: int = db_types.Column(db_types.Integer, name="is_cache", nullable=True, comment="是否缓存")
    isSync: int = db_types.Column(db_types.Integer, name="is_sync", nullable=True, comment="是否同步")
    variable: str = db_types.Column(db_types.String(5000), name="variable", nullable=True, comment="额外参数JSON")

# Pydantic模型
class Menu(APIModel):
    """
    菜单Pydantic模型，用于API接口
    """
    # Pydantic字段定义
    appCode: Optional[str] = Field(None, description="应用编码")
    parentId: str = Field(None, description="父ID")
    name: str = Field(None, description="菜单名称")
    code: str = Field(None, description="唯一编码")
    pids: Optional[str] = Field(None, description="父ID集合")
    type: Optional[int] = Field(None, description="菜单类型<sys_menu_type>")
    sort: Optional[str] = Field(None, description="排序")
    path: Optional[str] = Field(None, description="路由地址")
    component: Optional[str] = Field(None, description="组件地址")
    icon: Optional[str] = Field(None, description="菜单图标")
    isShow: Optional[int] = Field(None, description="是否显示")
    isLink: Optional[int] = Field(None, description="是否链接")
    url: Optional[str] = Field(None, description="外部链接地址")
    enabled: Optional[int] = Field(None, description="是否启用")
    openType: Optional[int] = Field(None, description="打开方式<sys_menu_open_type>")
    isCache: Optional[int] = Field(None, description="是否缓存")
    isSync: Optional[int] = Field(None, description="是否同步")
    variable: Optional[str] = Field(None, description="额外参数JSON")