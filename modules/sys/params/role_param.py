from pydantic import BaseModel, Field
from typing import Optional


from App_Demo.base import BasePageParam


class RoleParam(BaseModel):
    id: Optional[str] = Field(None, title="主键", description="主键")

    
    
    appCode: Optional[str] = Field(None, title="应用编码", description="应用编码")
    
    name: str = Field(..., title="角色名称", description="角色名称")
    
    code: str = Field(..., title="唯一编码", description="唯一编码")
    
    sort: Optional[str] = Field(None, title="排序", description="排序")
    
    roleType: int = Field(..., title="角色类型<sys_role_type>", description="角色类型<sys_role_type>")
    
    enabled: int = Field(..., title="是否启用", description="是否启用")
    
    dataScope: Optional[int] = Field(None, title="数据范围(1: 全部数据权限; 2: 自定义数据权限; 3: 本部门数据权限; 4: 本部门及以下部门权限; 5: 仅本人数据权限)", description="数据范围(1: 全部数据权限; 2: 自定义数据权限; 3: 本部门数据权限; 4: 本部门及以下部门权限; 5: 仅本人数据权限)")
    
    remark: Optional[str] = Field(None, title="备注", description="备注")
    
    
    
    
    
    


class RolePageParam(BasePageParam):
    pass