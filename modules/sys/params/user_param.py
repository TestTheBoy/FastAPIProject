#用户入参
from pydantic import BaseModel, Field
from typing import List, Optional
from App_Demo.base import BasePageParam


class UserParam(BaseModel):
    id: Optional[str] = Field(None, title="主键", description="主键")

    userName: str = Field(..., title="用户名", description="用户名")

    realName: str = Field(..., title="姓名", description="姓名")

    nickName: Optional[str] = Field(None, title="昵称", description="昵称")

    avatar: Optional[str] = Field(None, title="用户头像", description="用户头像")

    password: Optional[str] = Field(None, title="用户密码", description="用户密码")

    salt: Optional[str] = Field(None, title="密码加盐", description="密码加盐")

    mobilePhone: str = Field(..., title="手机号", description="手机号")

    tel: Optional[str] = Field(None, title="联系电话", description="联系电话")

    email: Optional[str] = Field(None, title="邮箱", description="邮箱")

    adminType: Optional[int] = Field(None, title="管理员类型<sys_admin_type>", description="管理员类型<sys_admin_type>")

    sex: int = Field(..., title="性别<sys_sex>", description="性别<sys_sex>")

    isLocked: Optional[int] = Field(None, title="是否锁定", description="是否锁定")

    deptId: Optional[str] = Field(None, title="所属部门", description="所属部门")

    postId: Optional[str] = Field(None, title="所属岗位", description="所属岗位")

    remark: Optional[str] = Field(None, title="备注", description="备注")

class UserPageParam(BasePageParam):
    roleId: Optional[str] = Field(None, title="所属角色ID", description="所属角色")
    inUserIdList: Optional[List[str]] = Field([], description="包含用户id列表")
    notInUserIdList: Optional[List[str]] = Field([], description="排除用户id列表")
    keywords: Optional[str] = Field(None, title="关键字", description="关键字")
    # m_t_IN_deptId: Optional[List[str]] = Field([],title="部门id列表", description="部门id列表")
    # m_EQ_isLocked: Optional[int] = Field(None, title="是否锁定", description="是否锁定")
    # m_LIKE_mobilePhone: Optional[str] = Field(None, title="手机号", description="手机号")
    # m_LIKE_realName: Optional[str] = Field(None, title="姓名", description="姓名")
    # m_LIKE_userName: Optional[str] = Field(None, title="用户名", description="用户名")
    # m_d_LIKE_name: Optional[str] = Field(None, title="部门名称", description="部门名称")
    # m_t_LIKE_realName: Optional[str] = Field(None, title="用户姓名", description="用户姓名")

class UpdateUserInfoParam(BaseModel):
    id: str = Field(None, title="用户ID", description="用户ID")
    realName: Optional[str] = Field(None, title="姓名", description="姓名")
    sex: int = Field(..., title="性别<sys_sex>", description="性别<sys_sex>")
    nickName: Optional[str] = Field(None, title="昵称", description="昵称")
    email: Optional[str] = Field(None, title="邮箱", description="邮箱")
    tel: Optional[str] = Field(None, title="联系电话", description="联系电话")



class UpdateUserAvatarParam(BaseModel):
    id: str = Field(None, title="用户ID", description="用户ID")
    avatar: str = Field(..., title="用户头像", description="用户头像")

class UpdateUserpwdParam(BaseModel):
    id: Optional[str] = Field(None, title="用户ID", description="用户ID")
    confirmPassword: str = Field(..., title="确认密码", description="确认密码")
    password: str = Field(..., title="旧密码", description="旧密码")
    newPassword: str = Field(..., title="新密码", description="新密码")