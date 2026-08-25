from typing import List, Optional
from pydantic import BaseModel, Field



class LoginToken(BaseModel):
    token: str = Field(..., description="登录令牌")
    userId: str = Field(..., description="用户ID")

class LoginUser(BaseModel):
    userId: str = Field(..., description="用户ID")
    userName: str = Field(..., description="用户名")
    realName:  Optional[str]  = Field(None, description="真实姓名")
    sex: Optional[int] = Field(None, description="性别")
    nickName: Optional[str] = Field(None, description="昵称")
    avatar: Optional[str] = Field(None, description="用户头像")
    mobilePhone:  Optional[str]  = Field(None, description="手机号")
    tel: Optional[str] = Field(None, description="联系电话")
    email: Optional[str] = Field(None, description="邮箱")
    permCodes: List[str] = Field([], description="权限码")
    superAdmin: bool = Field(False, description="是否是超级管理员")
    ext: dict = Field({}, description="扩展字段")
    deptId: Optional[str] = Field(None, description="所属部门")
    postId: Optional[str] = Field(None, description="所属岗位")
    deptName: Optional[str] = Field(None, description="部门名称")
    deptCode: Optional[str] = Field(None, description="部门编号")
    postName: Optional[str] = Field(None, description="岗位名称")
    postCode: Optional[str] = Field(None, description="岗位编号")
    roleIds: Optional[List[str]] = Field(None, description="角色ID集合，多个用逗号分隔")
    roleCodes: Optional[List[str]] = Field(None, description="角色编码集合")
    roleNames: Optional[List[str]] = Field(None, description="角色名称集合")
    lastLoginTime: Optional[str] = Field(None, description="最后登录时间")