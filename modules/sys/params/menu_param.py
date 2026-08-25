from pydantic import BaseModel, Field
from typing import Optional


from App_Demo.base import BasePageParam


class MenuParam(BaseModel):
    id: Optional[str] = Field(None, title="主键", description="主键")

    
    
    appCode: Optional[str] = Field(None, title="应用编码", description="应用编码")
    
    parentId: str = Field(..., title="父ID", description="父ID")
    
    name: str = Field(..., title="菜单名称", description="菜单名称")
    
    code: str = Field(..., title="唯一编码", description="唯一编码")
    
    pids: Optional[str] = Field(None, title="父ID集合", description="父ID集合")
    
    type: Optional[int] = Field(None, title="菜单类型<sys_menu_type>", description="菜单类型<sys_menu_type>")
    
    sort: Optional[str] = Field(None, title="排序", description="排序")
    
    path: Optional[str] = Field(None, title="路由地址", description="路由地址")
    
    component: Optional[str] = Field(None, title="组件地址", description="组件地址")
    
    icon: Optional[str] = Field(None, title="菜单图标", description="菜单图标")
    
    isShow: Optional[int] = Field(None, title="是否显示", description="是否显示")
    
    isLink: Optional[int] = Field(None, title="是否链接", description="是否链接")
    
    url: Optional[str] = Field(None, title="外部链接地址", description="外部链接地址")
    
    enabled: Optional[int] = Field(None, title="是否启用", description="是否启用")
    
    openType: Optional[int] = Field(None, title="打开方式<sys_menu_open_type>", description="打开方式<sys_menu_open_type>")
    
    isCache: Optional[int] = Field(None, title="是否缓存", description="是否缓存")
    
    isSync: Optional[int] = Field(None, title="是否同步", description="是否同步")
    
    variable: Optional[str] = Field(None, title="额外参数JSON", description="额外参数JSON")
    
    
    
    
    
    


class MenuPageParam(BasePageParam):
    filterByUser: Optional[int] = Field(None, title="是否过滤用户权限", description="是否过滤用户权限")