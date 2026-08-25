from typing import Optional, Union

from pydantic import Field
from sqlalchemy import Column, BigInteger, String, Integer, Boolean, DateTime

from App_Demo import db_types
from App_Demo.base import Base, APIModel, BaseOrmModel
from App_Demo.util import OrmUtil


# 数据库模型
class UserOrmModel(BaseOrmModel):
    """
    用户数据库模型
    """
    __tablename__ = 'sys_user'
    
    # 如果数据库中不存在基类字段，则设置为None（不映射到数据库列）
    
    # SQLAlchemy字段定义
    userName: str = db_types.Column(db_types.String(32), name="user_name", nullable=False, comment="用户名")
    realName: str = db_types.Column(db_types.String(32), name="real_name", nullable=False, comment="姓名")
    nickName: str = db_types.Column(db_types.String(32), name="nick_name", nullable=True, comment="昵称")
    avatar: str = db_types.Column(db_types.String(100), name="avatar", nullable=True, comment="用户头像")
    password: str = db_types.Column(db_types.String(64), name="password", nullable=True, comment="用户密码")
    salt: str = db_types.Column(db_types.String(10), name="salt", nullable=True, comment="密码加盐")
    mobilePhone: str = db_types.Column(db_types.String(11), name="mobile_phone", nullable=False, comment="手机号")
    tel: str = db_types.Column(db_types.String(20), name="tel", nullable=True, comment="联系电话")
    email: str = db_types.Column(db_types.String(32), name="email", nullable=True, comment="邮箱")
    adminType: int = db_types.Column(db_types.Integer, name="admin_type", nullable=True, comment="管理员类型<sys_admin_type>")
    sex: int = db_types.Column(db_types.Integer, name="sex", nullable=False, comment="性别<sys_sex>")
    isLocked: int = db_types.Column(db_types.Integer, name="is_locked", nullable=False, comment="是否锁定")
    deptId: str = db_types.Column(db_types.BigInteger, name="dept_id", nullable=True, comment="所属部门")
    postId: str = db_types.Column(db_types.BigInteger, name="post_id", nullable=True, comment="所属岗位")
    remark: str = db_types.Column(db_types.String(255), name="remark", nullable=True, comment="备注")

# Pydantic模型
class User(APIModel):
    '''
    对应的是pydantic定义的实体类，和数据库映射一致
    '''
    # 基础字段
    userName: Optional[str] = Field(..., description="用户名")
    realName: Optional[str] = Field(..., description="姓名")
    nickName: Optional[str] = Field(None, description="昵称")

    # 头像和认证字段
    avatar: Optional[str] = Field(None, description="用户头像")
    password: Optional[str] = Field(None, description="用户密码")  # 通常不返回密码
    salt: Optional[str] = Field(None, description="密码加盐")  # 通常不返回盐值

    # 联系信息字段
    mobilePhone: Optional[str] = Field(None, description="手机号")
    tel: Optional[str] = Field(None, description="联系电话")
    email: Optional[str] = Field(None, description="邮箱")

    # 用户属性字段
    adminType: Optional[int] = Field(None, description="管理员类型<sys_admin_type>")
    sex: Optional[int] = Field(None, description="性别<sys_sex>")
    isLocked: Optional[bool] = Field(None, description="是否锁定")

    # 组织信息字段
    deptId: Optional[Union[str, int]] = Field(None, description="所属部门")
    postId: Optional[Union[str, int]] = Field(None, description="所属岗位")

    # 其他字段
    remark: Optional[str] = Field(None, description="备注")
