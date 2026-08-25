from pydantic import BaseModel, Field

from App_Demo.base import BasePageParam


class RoleMenuParam(BaseModel):
    roleId: str = Field(..., title="角色ID", description="角色ID")

    menuId: str = Field(..., title="菜单ID", description="菜单ID")


class RoleMenuPageParam(BasePageParam):
    pass


class RoleIdParam(BaseModel):
    """
    角色id参数
    """
    roleId: str = Field(..., title="角色id", description="角色id")