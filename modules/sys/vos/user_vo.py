#VO = Value Object（值对象）或 View Object（视图对象）
#用于封装需要返回给前端的数据结构

from typing import Optional

from pydantic import Field
from modules.sys.models.user import User



class UserVO(User):
    deptName: Optional[str] = Field(None, description="部门名称")
    deptCode: Optional[str] = Field(None, description="部门编号")
    postName: Optional[str] = Field(None, description="岗位名称")
    postCode: Optional[str] = Field(None, description="岗位编号")
    roleIds: Optional[str] = Field(None, description="角色ID集合，多个用逗号分隔")