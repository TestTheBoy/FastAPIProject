from App_Demo.base import BasePageParam
from pydantic import BaseModel, Field
from typing import List, Optional

class UserRoleParam(BaseModel):
    userId: str = Field(..., title="用户ID", description="用户ID")

    roleId: str = Field(..., title="角色ID", description="角色ID")


class GrantUserRoleParam(BaseModel):
    userId: str = Field(..., title="用户ID", description="用户ID")

    roleIdList: List[str] = Field(..., title="角色ID列表", description="角色ID列表")


class UserRolePageParam(BasePageParam):
    pass